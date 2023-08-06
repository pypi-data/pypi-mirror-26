from __future__ import absolute_import, division, print_function, unicode_literals

import os

import pandas.io.sql as psql

from ..tools.connection import MyDB


# split execution into three part (execute from config files,
# execute csv files if they respect olapy's start schema model,
# and execute data base tables if they respect olapy's start schema model)
def load_table_config_file(executor_instance, cube_obj):
    """
    Load tables from config file.

    :param cube_obj: cubes object
    :return: tables dict with table name as key and DataFrame as value
    """
    tables = {}
    # just one facts table right now
    executor_instance.facts = cube_obj.facts[0].table_name
    db = MyDB(
        db_config_file_path=os.path.dirname(executor_instance.cube_path),
        db=executor_instance.cube)

    for dimension in cube_obj.dimensions:

        df = psql.read_sql_query(
            "SELECT * FROM {0}".format(dimension.name),
            db.engine,)
        # only certain columns
        if dimension.columns.keys():
            df = df[dimension.columns.keys()]

        # change table display name
        if dimension.displayName:
            table_name = dimension.displayName
        else:
            table_name = dimension.name

        # rename columns if value not None
        df.rename(
            columns=(dict((k, v) for k, v in dimension.columns.items() if v)),
            inplace=True,)

        tables[table_name] = df[[
            col for col in df.columns if col.lower()[-2:] != 'id'
        ]]

    return tables


# excel client
def construct_star_schema_config_file(executor_instance, cubes_obj):
    """Construct star schema DataFrame from configuration file for excel client.

    :param cube_name:  cube name (or database name)
    :param cubes_obj: cubes object
    :return: star schema DataFrame
    """
    executor_instance.facts = cubes_obj.facts[0].table_name
    db = MyDB(db_config_file_path=os.path.dirname(executor_instance.cube_path), db=executor_instance.cube)
    # load facts table

    fusion = psql.read_sql_query(
        "SELECT * FROM {0}".format(executor_instance.facts),
        db.engine,)

    for fact_key, dimension_and_key in cubes_obj.facts[0].keys.items():
        df = psql.read_sql_query(
            "SELECT * FROM {0}".format(dimension_and_key.split('.')[0]),
            db.engine,)

        for dimension in cubes_obj.dimensions:
            if dimension_and_key.split('.')[0] == dimension.name:
                df.rename(columns=dimension.columns, inplace=True)

        fusion = fusion.merge(
            df,
            left_on=fact_key,
            right_on=dimension_and_key.split('.')[1],
            how='left',
            # remove suffixe from dimension and keep the same column name for facts
            suffixes=('', '_y'),)

    # measures in config-file only
    if cubes_obj.facts[0].measures:
        executor_instance.measures = cubes_obj.facts[0].measures

    return fusion


def get_columns_n_tables(tables_cubes_obj, connector):

    all_columns = []
    tables = {}

    for table in tables_cubes_obj:

        tab = psql.read_sql_query(
            "SELECT * FROM {0}".format(table.name),
            connector,)

        try:
            if table.columns:
                tab = tab[table.columns]

        except BaseException:
            print("table columns doesn't exist")
            print('pass with all columns')

        try:
            if table.new_names:
                tab = tab.rename(columns=table.new_names)

        except BaseException:
            print("verify your old and new columns names")
            print('pass with no change')

        all_columns += list(tab.columns)
        tables.update({table.name: tab})

    return all_columns, tables


# web client
def construct_web_star_schema_config_file(executor_instance, cubes_obj):
    """Construct star schema DataFrame from configuration file for web client.

    :param cube_name:  cube name (or database name)
    :param cubes_obj: cubes object
    :return: star schema DataFrame
    """

    executor_instance.facts = cubes_obj.facts[0].table_name
    db = MyDB(
        db_config_file_path=os.path.dirname(executor_instance.cube_path),
        db=executor_instance.cube,)

    # load facts table
    fusion = psql.read_sql_query(
        "SELECT * FROM {0}".format(executor_instance.facts),
        db.engine,)

    all_columns, tables = get_columns_n_tables(cubes_obj.tables, db.engine)

    # load facts table columns
    if cubes_obj.facts[0].columns:
        all_columns += cubes_obj.facts[0].columns

    # measures in config-file only
    if cubes_obj.facts[0].measures:
        executor_instance.measures = cubes_obj.facts[0].measures
        all_columns += cubes_obj.facts[0].measures

    for fact_key, dimension_and_key in cubes_obj.facts[0].keys.items():
        dimension_name = dimension_and_key.split('.')[0]
        if dimension_name in tables.keys():
            df = tables[dimension_name]
        else:
            df = psql.read_sql_query(
                "SELECT * FROM {0}".format(dimension_and_key.split('.')[0]),
                db.engine,)

        fusion = fusion.merge(
            df,
            left_on=fact_key,
            right_on=dimension_and_key.split('.')[1],
            how='left',
            # remove suffixe from dimension and keep the same column name for facts
            suffixes=('', '_y'),)

    return fusion[[column for column in all_columns if 'id' != column[-2:]]]
