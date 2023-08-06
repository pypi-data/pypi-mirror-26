# -*- encoding: utf8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import itertools
import os
import re
import sys
from collections import OrderedDict
from os.path import expanduser
from traceback import print_tb

import numpy as np
import pandas as pd

from ..tools.config_file_parser import ConfigParser
from ..tools.connection import MyDB
from .execute_config_file import construct_star_schema_config_file, \
    construct_web_star_schema_config_file, load_table_config_file
from .execute_csv_files import construct_star_schema_csv_files, \
    load_tables_csv_files
from .execute_db import construct_star_schema_db, load_tables_db

RUNNING_TOX = 'RUNNING_TOX' in os.environ


class MdxEngine(object):
    """The main class for executing a query.

    :param cube_name: It must be under home_directory/olapy-data/CUBE_FOLDER
        (example : home_directory/olapy-data/cubes/sales)
    :param cube_folder: parent cube folder name
    :param mdx_query: query to execute
    :param sep: separator in the csv files
    """

    # french characters
    # or use new regex 2017.02.08
    regex = "(\[[\w+\d ]+\](\.\[[\w+\d\.\,\s\_\-\:\é\ù\è\ù\û\ü\ÿ\€\’\à\â\æ\ç\é\è\ê\ë\ï\î" \
            "\ô\œ\Ù\Û\Ü\Ÿ\À\Â\Æ\Ç\É\È\Ê\Ë\Ï\Î\Ô\Œ\& ]+\])*\.?((Members)|(\[Q\d\]))?)"

    # DATA_FOLDER useful for olapy web (flask instance_path)
    # get olapy-data path with instance_path instead of 'expanduser'
    DATA_FOLDER = None
    CUBE_FOLDER = "cubes"
    # (before instantiate MdxEngine I need to access cubes information)
    csv_files_cubes = []
    from_db_cubes = []

    def __init__(
            self,
            cube_name,
            client_type='excel',
            cubes_path=None,
            mdx_query=None,
            cube_folder=CUBE_FOLDER,
            sep=';',
            fact_table_name="Facts"):

        self.cube_folder = cube_folder
        self.cube = cube_name
        self.sep = sep
        self.facts = fact_table_name
        self._mdx_query = mdx_query
        if cubes_path is None:
            self.cube_path = os.path.join(self._get_default_cube_directory(), self.cube_folder)
        else:
            self.cube_path = cubes_path

        # to get cubes in db
        self._ = self.get_cubes_names()
        self.client = client_type
        self.tables_loaded = self.load_tables()
        # all measures
        self.measures = self.get_measures()
        self.load_star_schema_dataframe = self.get_star_schema_dataframe()
        self.tables_names = self._get_tables_name()
        # default measure is the first one
        self.selected_measures = [self.measures[0]]

    @property
    def mdx_query(self):
        return self._mdx_query

    @mdx_query.setter
    def mdx_query(self, value):
        self._mdx_query = value.replace('\n', '').replace('\t', '')

    @classmethod
    def _get_db_cubes_names(cls, olapy_data_location):
        """
        Get databases cubes names
        :param olapy_data_location:
        :return:
        """
        # surrounded with try, except and pass so we continue getting cubes
        # from different sources (db, csv...) without interruption
        try:
            db = MyDB(db_config_file_path=olapy_data_location)
            if db.sgbd.upper() == 'ORACLE':
                # You can think of a mysql "database" as a schema/user in Oracle.
                MdxEngine.from_db_cubes = [db.username]
            else:
                all_db_query = cls._gett_all_databeses_query(db.sgbd)
                result = db.engine.execute(all_db_query)
                available_tables = result.fetchall()
                MdxEngine.from_db_cubes = [
                    database[0] for database in available_tables if
                    database[0] not in ['mysql', 'information_schema', 'performance_schema', 'sys']
                ]

        except Exception:
            type, value, traceback = sys.exc_info()
            print(type)
            print(value)
            print_tb(traceback)
            print('no database connexion')
            pass

    @staticmethod
    def _get_csv_cubes_names(cubes_location):
        try:
            MdxEngine.csv_files_cubes = [
                file for file in os.listdir(cubes_location)
                if os.path.isdir(os.path.join(cubes_location, file))
            ]
        except Exception:
            type, value, traceback = sys.exc_info()
            print('Error opening %s' % (value))
            print('no csv folders')
            pass

    @classmethod
    def get_cubes_names(cls):
        """
        :return: list cubes name that exist in cubes folder
            (under ~/olapy-data/cubes) and postgres database (if connected).
        """

        olapy_data_location = MdxEngine._get_default_cube_directory()
        cubes_location = os.path.join(olapy_data_location, cls.CUBE_FOLDER)

        MdxEngine._get_csv_cubes_names(cubes_location)
        MdxEngine._get_db_cubes_names(olapy_data_location)

        return MdxEngine.csv_files_cubes + MdxEngine.from_db_cubes

    @staticmethod
    def _get_default_cube_directory():

        # toxworkdir does not expanduser properly under tox
        if 'OLAPY_PATH' in os.environ:
            home_directory = os.environ.get('OLAPY_PATH')
        elif MdxEngine.DATA_FOLDER is not None:
            home_directory = MdxEngine.DATA_FOLDER
        elif RUNNING_TOX:
            home_directory = os.environ.get('HOME_DIR')
        else:
            home_directory = expanduser("~")

        if 'olapy-data' not in home_directory:
            home_directory = os.path.join(home_directory, 'olapy-data')

        return home_directory

    @classmethod
    def _gett_all_databeses_query(cls, sgbd):
        """

        :param sgbd: postgres | mysql | oracle | mssql
        :return: all databases in the sgbd
        """
        if sgbd.upper() == 'POSTGRES':
            return 'SELECT datname FROM pg_database WHERE datistemplate = false;'
        elif sgbd.upper() == 'MYSQL':
            return 'SHOW DATABASES'
        elif sgbd.upper() == 'MSSQL':
            return "select name FROM sys.databases where name not in ('master','tempdb','model','msdb');"
        elif sgbd.upper() == 'ORACLE':
            return 'select username from dba_users;'

    def _get_tables_name(self):
        """Get all tables names.

        :return: list tables names
        """
        return self.tables_loaded.keys()

    def hierarchized_tuples(self):
        """Check if hierarchized mdx query.

        :return: True | False
        """
        return 'Hierarchize' in self.mdx_query

    def load_tables(self):
        """Load all tables { Table name : DataFrame } of the current cube instance.

        :return: dict with key as table name and DataFrame as value
        """

        config_file_parser = ConfigParser(self.cube_path)
        tables = {}
        if self.client == 'excel' and config_file_parser.config_file_exist(client_type=self.client) \
                and self.cube in config_file_parser.get_cubes_names(client_type=self.client):

            # for web (config file) we need only star_schema_dataframes, not all tables
            for cubes in config_file_parser.construct_cubes():
                if cubes.source.upper() in ['POSTGRES', 'MYSQL', 'MSSQL', 'ORACLE']:
                    tables = load_table_config_file(self, cubes)

        elif self.cube in self.from_db_cubes:
            tables = load_tables_db(self)

        elif self.cube in self.csv_files_cubes:
            tables = load_tables_csv_files(self)

        return tables

    def get_measures(self):
        """:return: all numerical columns in facts table."""

        # if web, get measures from config file
        # from postgres and oracle databases , all tables names are lowercase
        config_file_parser = ConfigParser(self.cube_path)
        if self.client == 'web' and config_file_parser.config_file_exist('web'):
            for cubes in config_file_parser.construct_cubes(self.client):

                # update facts name
                self.facts = cubes.facts[0].table_name

                # if measures are specified in the config file
                if cubes.facts[0].measures:
                    return cubes.facts[0].measures

        # col.lower()[-2:] != 'id' to ignore any id column
        return [
            col
            for col in self.tables_loaded[self.facts].select_dtypes(
                include=[np.number],).columns if col.lower()[-2:] != 'id'
        ]

    def _construct_star_schema_from_config(self, config_file_parser):
        fusion = None
        for cubes in config_file_parser.construct_cubes(self.client):
            if cubes.source.upper() in ['POSTGRES', 'MYSQL', 'MSSQL', 'ORACLE']:
                if self.client == 'web':
                    fusion = construct_web_star_schema_config_file(self, cubes)
                else:
                    fusion = construct_star_schema_config_file(self, cubes)
        return fusion

    def get_star_schema_dataframe(self):
        """Merge all DataFrames as star schema.

        :return: star schema DataFrame
        """
        fusion = None
        config_file_parser = ConfigParser(self.cube_path)
        if config_file_parser.config_file_exist(self.client) and self.cube in config_file_parser.get_cubes_names(
                client_type=self.client):
            fusion = self._construct_star_schema_from_config(config_file_parser)

        elif self.cube in self.from_db_cubes:
            fusion = construct_star_schema_db(self)

        elif self.cube in self.csv_files_cubes:
            fusion = construct_star_schema_csv_files(self)

        return fusion[[
            col for col in fusion.columns if col.lower()[-3:] != '_id'
        ]]

    def get_all_tables_names(self, ignore_fact=False):
        """
        Get list of tables names of the cube.

        :param ignore_fact: return all table name with facts table name
        :return: all tables names
        """
        if ignore_fact:
            return [tab for tab in self.tables_names if self.facts not in tab]
        return self.tables_names

    def get_cube(self):
        """
        Get path to the cube (example /home_directory/olapy-data/cubes).

        :return: path to the cube
        """
        if MdxEngine.DATA_FOLDER is not None:
            return os.path.join(
                MdxEngine.DATA_FOLDER,
                MdxEngine.CUBE_FOLDER,
                self.cube,)
        return os.path.join(self.cube_path, self.cube)

    @staticmethod
    def get_tuples(query, start=None, stop=None):
        """Get all tuples in the mdx query.

        Example::


            SELECT  {
                    [Geography].[Geography].[All Continent].Members,
                    [Geography].[Geography].[Continent].[Europe]
                    } ON COLUMNS,

                    {
                    [Product].[Product].[Company]
                    } ON ROWS

                    FROM {sales}

        It returns ::

            [
                ['Geography','Geography','Continent'],
                ['Geography','Geography','Continent','Europe'],
                ['Product','Product','Company']
            ]


        :param query: mdx query
        :param start: keyword in the query where we start (examples start = SELECT)
        :param stop:  keyword in the query where we stop (examples start = ON ROWS)

        :return:  nested list of tuples (see the example)
        """

        if start is not None:
            start = query.index(start)
        if stop is not None:
            stop = query.index(stop)

        # clean the query (remove All, Members...)
        return [
            [
                tup_att.replace('All ', '').replace('[', "").replace("]", "")
                for tup_att in tup[0].replace('.Members', '').replace('.MEMBERS', '', ).split('].[') if tup_att
            ]
            for tup in re.compile(MdxEngine.regex).findall(
                query[start:stop], )
            if len(tup[0].split('].[')) > 1
            # for tup in re.compile(MdxEngine.regex).findall(
            #     query.encode("utf-8", 'replace')[start:stop],)
            # if len(tup[0].split('].[')) > 1
        ]

    @staticmethod
    def split_tuple(tupl):
        """
        Split Tuple (String) into items.

            example : input : '[Geography].[Geography].[Continent].[Europe]'
                      output : ['Geography','Geography','Continent','Europe']

        :param tupl: MDX Tuple as String
        :return: Tuple items in list
        """
        splitted_tupl = tupl.strip(' \t\n').split('].[')
        splitted_tupl[0] = splitted_tupl[0].replace('[', '')
        splitted_tupl[-1] = splitted_tupl[-1].replace(']', '')
        return splitted_tupl

    def decorticate_query(self, query):
        """Get all tuples that exists in the MDX Query by axes.

        :param query: MDX Query
        :return: dict of axis as key and tuples as value
        """

        # Hierarchize -> ON COLUMNS , ON ROWS ...
        # without Hierarchize -> ON 0

        tuples_on_mdx_query = self.get_tuples(query)
        on_rows = []
        on_columns = []
        on_where = []

        try:
            # ON ROWS
            if 'ON ROWS' in query:
                stop = 'ON ROWS'
                if 'ON COLUMNS' in query:
                    start = 'ON COLUMNS'
                else:
                    start = 'SELECT'
                on_rows = self.get_tuples(query, start, stop)

            # ON COLUMNS
            if 'ON COLUMNS' in query:
                start = 'SELECT'
                stop = 'ON COLUMNS'
                on_columns = self.get_tuples(query, start, stop)

            # ON COLUMNS (AS 0)
            if 'ON 0' in query:
                start = 'SELECT'
                stop = 'ON 0'
                on_columns = self.get_tuples(query, start, stop)

            # WHERE
            if 'WHERE' in query:
                start = 'FROM'
                on_where = self.get_tuples(query, start)

        except BaseException:
            raise SyntaxError('Please check your MDX Query')

        return {
            'all': tuples_on_mdx_query,
            'columns': on_columns,
            'rows': on_rows,
            'where': on_where,
        }

    @staticmethod
    def change_measures(tuples_on_mdx):
        """Set measures to which exists in the query.

        :param tuples_on_mdx: List of tuples:


            example : [ '[Measures].[Amount]' , '[Geography].[Geography].[Continent]' ]


        :return: measures column's names (Amount)
        """

        list_measures = []
        for tple in tuples_on_mdx:
            if tple[0].upper() == "MEASURES" and tple[-1] not in list_measures:
                list_measures.append(tple[-1])

        return list_measures

    def get_tables_and_columns(self, tuple_as_list):
        """Get used dimensions and columns in the MDX Query (useful for DataFrame -> xmla response transformation).

        :param tuple_as_list: list of tuples

            example : [ '[Measures].[Amount]',
                        '[Product].[Product].[Crazy Development]',
                        '[Geography].[Geography].[Continent]' ]

        :return: dimension and columns dict

            example :
            {
            Geography : ['Continent','Country'],
            Product : ['Company']
            Facts :  ['Amount','Count']
            }
        """
        axes = {}
        for axis, tuples in tuple_as_list.items():
            measures = []
            tables_columns = OrderedDict()
            # if we have measures in columns or rows axes like :
            # SELECT {[Measures].[Amount],[Measures].[Count]} ON COLUMNS
            # we have to add measures directly to tables_columns
            for tupl in tuples:
                if tupl[0].upper() == 'MEASURES':
                    if tupl[-1] not in measures:
                        measures.append(tupl[-1])
                        tables_columns.update({self.facts: measures})
                    else:
                        continue
                else:
                    tables_columns.update({
                        tupl[0]:
                            self.tables_loaded[tupl[0]].columns[:len(
                                tupl[2:None if self.hierarchized_tuples() else -1], )],
                    })

            axes.update({axis: tables_columns})
        return axes

    def execute_one_tuple(self, tuple_as_list, Dataframe_in, columns_to_keep):
        """
        Filter a DataFrame (Dataframe_in) with one tuple.

            Example ::


                tuple = ['Geography','Geography','Continent','Europe','France','olapy']

                Dataframe_in in :

                +-------------+----------+---------+---------+---------+
                | Continent   | Country  | Company | Article | Amount  |
                +=============+==========+=========+=========+=========+
                | America     | US       | MS      | SSAS    | 35150   |
                +-------------+----------+---------+---------+---------+
                | Europe      |  France  | AB      | olapy   | 41239   |
                +-------------+----------+---------+---------+---------+
                |  .....      |  .....   | ......  | .....   | .....   |
                +-------------+----------+---------+---------+---------+

                out :

                +-------------+----------+---------+---------+---------+
                | Continent   | Country  | Company | Article | Amount  |
                +=============+==========+=========+=========+=========+
                | Europe      |  France  | AB      | olapy   | 41239   |
                +-------------+----------+---------+---------+---------+


        :param tuple_as_list: tuple as list
        :param Dataframe_in: DataFrame in with you want to execute tuple
        :param columns_to_keep: (useful for executing many tuples, for instance execute_mdx)
        other columns to keep in the execution except the current tuple
        :return: Filtered DataFrame
        """
        df = Dataframe_in
        #  tuple_as_list like ['Geography','Geography','Continent']
        #  return df with Continent column non empty
        if len(tuple_as_list) == 3:
            df = df[(df[tuple_as_list[-1]].notnull())]

        # tuple_as_list like['Geography', 'Geography', 'Continent' , 'America','US']
        # execute : df[(df['Continent'] == 'America')] and
        #           df[(df['Country'] == 'US')]
        elif len(tuple_as_list) > 3:
            for idx, tup_att in enumerate(tuple_as_list[3:]):
                # df[(df['Year'] == 2010)]
                # 2010 must be as int, otherwise , pandas generate exception
                if tup_att.isdigit():
                    tup_att = int(tup_att)

                df = df[(df[self.tables_loaded[tuple_as_list[0]].columns[idx]]
                         == tup_att)]
        cols = list(itertools.chain.from_iterable(columns_to_keep))
        return df[cols + self.selected_measures]

    @staticmethod
    def add_missed_column(dataframe1, dataframe2):
        """
        Solution to fix BUG : https://github.com/pandas-dev/pandas/issues/15525

        if you want to concat two dataframes with different columns like :

        +-------------+---------+
        | Continent   | Amount  |
        +=============+=========+
        | America     | 35150   |
        +-------------+---------+
        | Europe      | 41239   |
        +-------------+---------+

        and :

        +-------------+---------------+---------+
        | Continent   | Country_code  | Amount  |
        +=============+===============+=========+
        | America     | 1111          | 35150   |
        +-------------+---------------+---------+

        result :

        +-------------+--------------+---------+
        | Continent   | Country_code | Amount  |
        +=============+==============+=========+
        | America     | 1111.0       |35150    |
        +-------------+--------------+---------+
        | Europe      | NaN          |41239    |
        +-------------+--------------+---------+

        Country_code is converted to float,

        so the solution is to add a column to the fist DataFrame filled with -1, thus

        +-------------+---------------+---------+
        | Continent   | Country_code  | Amount  |
        +=============+===============+=========+
        | America     | -1            | 35150   |
        +-------------+---------------+---------+
        | Europe      | -1            | 41239   |
        +-------------+---------------+---------+

        and :

        +-------------+---------------+---------+
        | Continent   | Country_code  | Amount  |
        +=============+===============+=========+
        | America     | 1111          | 35150   |
        +-------------+---------------+---------+

        result :

        +-------------+--------------+---------+
        | Continent   | Country_code | Amount  |
        +=============+==============+=========+
        | America     | 1111         |35150    |
        +-------------+--------------+---------+
        | Europe      | -1           |41239    |
        +-------------+--------------+---------+


        :return: Two DataFrames with same columns
        """
        df_with_less_columns = dataframe1
        df_with_more_columns = dataframe2
        if len(list(dataframe1.columns)) != len(list(dataframe2.columns)):
            if len(list(dataframe1.columns)) > len(list(dataframe2.columns)):
                df_with_more_columns = dataframe1
                df_with_less_columns = dataframe2
            missed_columns = [
                col for col in list(df_with_more_columns.columns)
                if col not in list(df_with_less_columns.columns)
            ]
            for missed_column in missed_columns:
                df_with_less_columns[missed_column] = -1

        return [df_with_less_columns, df_with_more_columns]

    def update_columns_to_keep(self, tuple_as_list, columns_to_keep):
        """
        If we have multiple dimensions, with many columns like:

            columns_to_keep :

                Geo  -> Continent,Country

                Prod -> Company

                Time -> Year,Month,Day


        we have to use only dimension's columns of current dimension that exist
        in tuple_as_list and keep other dimensions columns

        so if tuple_as_list = ['Geography','Geography','Continent']

        columns_to_keep will be:

            columns_to_keep :

                Geo  -> Continent

                Prod -> Company

                Time -> Year,Month,Day


        we need columns_to_keep for grouping our columns in the DataFrame

        :param tuple_as_list:  example : ['Geography','Geography','Continent']
        :param columns_to_keep:

            example :

                {

                'Geography':

                    ['Continent','Country'],

                'Time':

                    ['Year','Month','Day']
                }

        :return: updated columns_to_keep
        """

        columns = 2 if self.hierarchized_tuples() else 3
        if len(tuple_as_list) == 3 \
                and tuple_as_list[-1] in self.tables_loaded[tuple_as_list[0]].columns:
            # in case of [Geography].[Geography].[Country]
            cols = [tuple_as_list[-1]]
        else:
            cols = self.tables_loaded[tuple_as_list[0]].columns[:len(
                tuple_as_list[columns:],)]

        columns_to_keep.update({tuple_as_list[0]: cols})

    @staticmethod
    def _uniquefy_tuples(tuples):
        """
        Remove redundant tuples.
        :param tuples: list of string of tuples.
        :return: list of string of unique tuples.
        """
        uniquefy = []
        for tup in tuples:
            if tup not in uniquefy:
                uniquefy.append(tup)

        return uniquefy

    def tuples_to_dataframes(self, tuples_on_mdx_query, columns_to_keep):
        """
        Construct DataFrame of many groups mdx query.
        :param tuples_on_mdx_query: list of string of tuples.
        :param columns_to_keep: (useful for executing many tuples, for instance execute_mdx).
        :return: Pandas DataFrame.
        """
        # get only used columns and dimensions for all query
        start_df = self.load_star_schema_dataframe
        df_to_fusion = []
        table_name = tuples_on_mdx_query[0][0]
        # in every tuple
        for tupl in tuples_on_mdx_query:
            # if we have measures in columns or rows axes like :
            # SELECT {[Measures].[Amount],[Measures].[Count], [Customers].[Geography].[All Regions]} ON COLUMNS
            # we use only used columns for dimension in that tuple and keep
            # other dimension's columns
            self.update_columns_to_keep(tupl, columns_to_keep)
            # a tuple with new dimension
            if tupl[0] != table_name:
                # if we change dimension , we have to work on the
                # exection's result on previous DataFrames

                df = df_to_fusion[0]
                for next_df in df_to_fusion[1:]:
                    df = pd.concat(self.add_missed_column(df, next_df))

                table_name = tupl[0]
                df_to_fusion = []
                start_df = df

            df_to_fusion.append(
                self.execute_one_tuple(
                    tupl,
                    start_df,
                    columns_to_keep.values(), ), )

        return df_to_fusion

    def fusion_dataframes(self, df_to_fusion):
        """
        Concat chunks of DataFrames.
        :param df_to_fusion: List of Pandas DataFrame.
        :return: Pandas DataFrame.
        """

        df = df_to_fusion[0]
        for next_df in df_to_fusion[1:]:
            df = pd.concat(self.add_missed_column(df, next_df))
        return df

    @staticmethod
    def add_tuple_brackets(tupl):
        """
        After splitting tuple (with splited_group), you got some tuple like aa].[bb].[cc].[dd
        so add_tuple_brackets fix this by adding missed brackets [aa].[bb].[cc].[dd].

        :param tupl: Tuple as string exple  'aa].[bb].[cc].[dd'.
        :return: [aa].[bb].[cc].[dd].
        """
        tupl = tupl.strip()
        if tupl[0] != '[':
            tupl = '[' + tupl
        if tupl[-1] != ']':
            tupl = tupl + ']'
        return tupl

    def split_group(self, group):
        """
        Split group of tuples example '[Geo].[Geo].[Continent],[Prod].[Prod].[Name],[Time].[Time].[Day]'.
        :param group: Group of tuple as string '[Geo].[Geo].[Continent],[Prod].[Prod].[Name],[Time].[Time].[Day]'.
        :return: Separated tuples as list ['[Geo].[Geo].[Continent]','[Prod].[Prod].[Name]','[Time].[Time].[Day]'].
        """
        splited_group = group.replace('\n', '').replace('\t', '').split('],')
        return list(map(lambda tupl: self.add_tuple_brackets(tupl), splited_group))

    def get_nested_select(self):
        """
        Get tuples groups in query like :

                Select {
                    ([Time].[Time].[Day].[2010].[Q2 2010].[May 2010].[May 19,2010],
                    [Geography].[Geography].[Continent].[Europe],
                    [Measures].[Amount]),

                    ([Time].[Time].[Day].[2010].[Q2 2010].[May 2010].[May 17,2010],
                    [Geography].[Geography].[Continent].[Europe],
                    [Measures].[Amount])
                    }

        :return: All groups as list of strings : example:


                    ['[Time].[Time].[Day].[2010].[Q2 2010].[May 2010].[May 19,2010],
                    [Geography].[Geography].[Continent].[Europe],
                    [Measures].[Amount]',

                    '[Time].[Time].[Day].[2010].[Q2 2010].[May 2010].[May 17,2010],
                    [Geography].[Geography].[Continent].[Europe],
                    [Measures].[Amount]'

        """
        return re.findall(r'\(([^()]+)\)', self.mdx_query)

    def check_nested_select(self):
        """
        Check if the MDX Query is Hierarchized and contains many tuples groups.

        :return: True | False
        """
        return not self.hierarchized_tuples() and len(self.get_nested_select()) >= 2

    def nested_tuples_to_dataframes(self, columns_to_keep):
        """
        Construct DataFrame of many groups.
        :param columns_to_keep: (useful for executing many tuples, for instance execute_mdx).
        :return: Pandas DataFrame.
        """
        dfs = []
        grouped_tuples = self.get_nested_select()
        for tuple_groupe in grouped_tuples:
            transformed_tuple_groups = []
            for tuple in self.split_group(tuple_groupe):
                tuple = tuple.split('].[')
                tuple[0] = tuple[0].replace('[', '')
                tuple[-1] = tuple[-1].replace(']', '')
                if tuple[0].upper() != 'MEASURES':
                    transformed_tuple_groups.append(tuple)

            dfs.append(self.tuples_to_dataframes(transformed_tuple_groups, columns_to_keep)[0])

        return dfs

    def execute_mdx(self):
        """Execute an MDX Query.

        Usage ::

            executor = MdxEngine('sales')
            executor.mdx_query = "SELECT  FROM [sales] WHERE ([Measures].[Amount])"
            executor.execute_mdx()

        :return: dict with DataFrame execution result and (dimension and columns used as dict)

            {
            'result' : DataFrame result
            'columns_desc' : dict of dimension and columns used
            }

        """

        # use measures that exists on where or insides axes
        query_axes = self.decorticate_query(self.mdx_query)
        if self.change_measures(query_axes['all']):
            self.selected_measures = self.change_measures(query_axes['all'])

        tables_n_columns = self.get_tables_and_columns(query_axes)

        columns_to_keep = OrderedDict(
            (table, columns)
            for table, columns in tables_n_columns['all'].items()
            if table != self.facts)

        tuples_on_mdx_query = [
            tup for tup in query_axes['all'] if tup[0].upper() != 'MEASURES'
        ]

        if not self.hierarchized_tuples():
            tuples_on_mdx_query = self._uniquefy_tuples(tuples_on_mdx_query)
            tuples_on_mdx_query.sort(key=lambda x: x[0])

        # if we have tuples in axes
        # to avoid prob with query like this: SELECT  FROM [Sales] WHERE ([Measures].[Amount])
        if tuples_on_mdx_query:

            if self.check_nested_select():
                df_to_fusion = self.nested_tuples_to_dataframes(columns_to_keep)
            else:
                df_to_fusion = self.tuples_to_dataframes(tuples_on_mdx_query, columns_to_keep)

            df = self.fusion_dataframes(df_to_fusion)

            cols = list(itertools.chain.from_iterable(columns_to_keep.values()))

            sort = self.hierarchized_tuples()
            # margins=True for columns total !!!!!
            return {
                'result':
                    df.groupby(cols, sort=sort).sum()[self.selected_measures],
                'columns_desc':
                    tables_n_columns,
            }

        else:
            return {
                'result': self.load_star_schema_dataframe[self.selected_measures].sum().to_frame().T,
                'columns_desc': tables_n_columns,
            }
