from datetime import timedelta
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.task_group import TaskGroup
from airflow.models import Connection
import os

from airflow.operators.mysql_operator import MySqlOperator
from airflow.hooks.mysql_hook import MySqlHook

from airflow.operators.postgres_operator import PostgresOperator
from airflow.hooks.postgres_hook import PostgresHook

CREATE_SQL = "CREATE TABLE IF NOT EXISTS t1 (id int);"
SELECT_SQL = "SELECT  TABLE_SCHEMA, TABLE_NAME, TABLE_TYPE FROM information_schema.tables LIMIT 10"

DAG_ID = os.path.basename(__file__).replace('_dag.py', '')
default_args = {
    'depends_on_past': False,
    'start_date': days_ago(2),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(seconds=5)
}

dag = DAG(f'{DAG_ID}',
          default_args=default_args,
          description='DEMO: Usage of credentials stored in AWS Secrets Manager',
          schedule_interval=None,
          catchup=False,
          max_active_runs=1
          )

def execute_sql_uri():
    """
    Execute SQL statement and return results
    :param conn_id: redshift connection id
    :param sql: Redshift SQL code to execute
    :return: results of statement execution (list of tuples)
    """
    conn_id = "aurora_mysql_uri" # so it'll look for connection secret in <connection_prefix>/aurora
    sql = SELECT_SQL

    result = []
    mysql_hook = MySqlHook(mysql_conn_id=conn_id)
    connection = mysql_hook.get_conn()
    cursor = connection.cursor()
    cursor.execute(sql)
    if cursor.description:
        result = cursor.fetchall()
        print(result)
    return result

def execute_sql_json():
    """
    Execute SQL statement and return results
    :param conn_id: redshift connection id
    :param sql: Redshift SQL code to execute
    :return: results of statement execution (list of tuples)
    """
    conn_id = "aurora_mysql_json" # so it'll look for connection secret in <connection_prefix>/aurora
    sql = SELECT_SQL

    result = []
    mysql_hook = MySqlHook(mysql_conn_id=conn_id)
    connection = mysql_hook.get_conn()
    cursor = connection.cursor()
    cursor.execute(sql)
    if cursor.description:
        result = cursor.fetchall()
        print(result)
    return result

def execute_pgsql_uri():
    conn_id = "aurora_postgresql_uri" # so it'll look for connection secret in <connection_prefix>/aurora
    sql = SELECT_SQL

    result = []
    mysql_hook = PostgresHook(postgres_conn_id=conn_id)
    connection = mysql_hook.get_conn()
    cursor = connection.cursor()
    cursor.execute(sql)
    if cursor.description:
        result = cursor.fetchall()
        print(result)
    return result

def execute_pgsql_json():
    conn_id = "aurora_postgresql_json" # so it'll look for connection secret in <connection_prefix>/aurora
    sql = SELECT_SQL

    result = []
    mysql_hook = PostgresHook(postgres_conn_id=conn_id)
    connection = mysql_hook.get_conn()
    cursor = connection.cursor()
    cursor.execute(sql)
    if cursor.description:
        result = cursor.fetchall()
        print(result)
    return result

def get_connection():
    conn_ids = ["aurora_mysql_uri", "aurora_mysql_uri" ] #, "aurorapg", "aurorapg2"]

    for conn_id in conn_ids:
        #connection = Connection(conn_id=conn_id)
        print(f"**************** Processing connections = {conn_id}")
        try:
            connection = Connection.get_connection_from_secrets(conn_id)
            print(connection)
            print(f"URI: {connection.get_uri()}")
            print(f"Props: {connection.host}, {connection.login}, {connection.password}, {connection.extra}")

            print('testing connection - begin')
            connection.test_connection()
            print('testing connection - end')

            print('hook connection - begin')
            hook = connection.get_hook()
            print(type(hook))
            print('hook connection - end')
        except Exception as ex:
            print("Error while processing")
            print(str(ex))

# DAG definition
with dag as dag:
    dummy_operator = DummyOperator(
        task_id='dummy_task'
    )

    with TaskGroup(group_id="MySQLOperator") as dag_group_mysql:
        mysql_uri_operator = MySqlOperator(
            task_id='mysql_uri',
            mysql_conn_id = 'aurora_mysql_uri',
            sql="CREATE TABLE IF NOT EXISTS t1 (id int);"
        )

        mysql_json_operator = MySqlOperator(
            task_id='mysql_json',
            mysql_conn_id = 'aurora_mysql_json',
            sql="CREATE TABLE IF NOT EXISTS t1 (id int);"
        )


    with TaskGroup(group_id="PythonOperator_MySQL") as dag_group_mysqlPy:
        execute_sql_uri_operator = PythonOperator(
            task_id='execute_sql_uri',
            python_callable=execute_sql_uri,
            trigger_rule='all_done'
        )

        execute_sql_json_operator = PythonOperator(
            task_id='execute_sql_json',
            python_callable=execute_sql_json,
            trigger_rule='all_done'
        )


    with TaskGroup(group_id="PostgreSQLOperator") as dag_group_pg:
        mysql_operator = PostgresOperator(
            task_id='pgsql',
            postgres_conn_id = 'aurora_postgresql_uri',
            sql="CREATE TABLE IF NOT EXISTS turi (id int);"
        )

        mysql_operator2 = PostgresOperator(
            task_id='pgsql2',
            postgres_conn_id = 'aurora_postgresql_json',
            sql="CREATE TABLE IF NOT EXISTS tjson (id int);"
        )

    with TaskGroup(group_id="PythonOperator_PostgreSQL") as dag_group_pgPy:
        execute_pgsql_uri_operator = PythonOperator(
            task_id='execute_pgsql_uri',
            python_callable=execute_pgsql_uri,
            trigger_rule='all_done'
        )

        execute_pgsql_json_operator = PythonOperator(
            task_id='execute_pgsql_json',
            python_callable=execute_pgsql_json,
            trigger_rule='all_done'
        )


    get_connection_operator = PythonOperator(
        task_id='get_connection',
        python_callable=get_connection,
        trigger_rule='all_done'
    )

    dummy_operator  >> [dag_group_mysql, dag_group_mysqlPy, get_connection_operator, dag_group_pg, dag_group_pgPy]
    