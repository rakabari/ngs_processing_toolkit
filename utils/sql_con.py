#!/home/sbsuser/venv/bin/python3.11
import pandas as pd
import os
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


def sql_con(db: str, host: str = 'localhost') -> create_engine:
    """
    Connects to a MySQL database usin the hostname and returns create_engine object
    """
    user = os.getenv('mysqluser')
    pw = os.getenv('mysqlpw')

    if user is None or pw is None:
        raise EnvironmentError(
            "Environment variables 'mysqluser' or 'mysqlpw' are not set.")

    sql_engine = create_engine(
        f'mysql+pymysql://{user}:{pw}@{host}/{db}', pool_recycle=3306)

    return sql_engine


def execute_sql_file(sql_file: str, db_con: Engine) -> None:
    """
    Splits SQL statements from an SQL file and executes them.
    """
    with open(sql_file, 'r') as sql_obj:
        statements = sql_obj.read().split(';')
        executed = False  # boolean flag indicating whether any statements have been executed
        for sql_statement in statements:
            if len(sql_statement.strip()) > 0:  # use strip to remove leading/trailing whitespace
                db_con.execute(sql_statement)
                executed = True
        if executed:
            print(f'INFO: Executed: {os.path.basename(sql_file)}')


def get_distinct_values(table: str, columns: list, db_con: Engine) -> list:
    """
    Returns a list of unique items from a specified column of a database table.
    """
    return pd.read_sql_table(table,
                             columns=columns,
                             con=db_con)[columns[0]].drop_duplicates().tolist()


def drop_sort(df: pd.DataFrame, table: str, db_con, drop: list = [], sort: list = []) -> None:
    """
    Drops duplicate rows based on `drop` columns and sorts the DataFrame based on `sort` columns, then
    writes the result back to the SQL table specified by `table` using the SQLAlchemy engine `db_con`.

    Args:
    df (pd.DataFrame): The DataFrame to modify.
    table (str): The name of the SQL table to write the modified DataFrame to.
    db_con (sqlalchemy.engine.Engine): The SQLAlchemy engine object used to connect to the SQL database.
    drop (list, optional): A list of column names to use to identify duplicate rows. Default is an empty list.
    sort (list, optional): A list of column names to use to sort the DataFrame. Default is an empty list.

    Returns:
    None
    """
    # Load the data from the SQL table
    df = pd.read_sql_table(table, con=db_con)

    # Drop duplicate rows based on `drop` columns
    df.drop_duplicates(subset=drop, inplace=True)

    # Sort the DataFrame based on `sort` columns
    df.sort_values(sort, inplace=True)

    # Write the modified DataFrame back to the SQL table
    df.to_sql(table, db_con, if_exists='replace', index=False)
