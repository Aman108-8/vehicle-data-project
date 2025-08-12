import mysql.connector
from mysql.connector import Error
import pandas as pd
import streamlit as st  # ✅ Add this line


def create_connection():
    """Create a database connection with fixed credentials"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='your database',
            user='your user_name',
            password='yourpassword.',
            port='your port',
            auth_plugin='mysql_native_password',
            connect_timeout=5
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            cursor.close()
            print("✅ MySQL connection successful!")
            return connection
            
    except Error as e:
        error_details = {
            "errno": e.errno,
            "sqlstate": e.sqlstate,
            "msg": e.msg
        }
        print(f"❌ MySQL Connection Failed: {error_details}")
        st.error(f"Database connection failed: {e}")
        return None

def execute_query(connection, query, params=None):
    """Execute a query and return DataFrame"""
    if not connection or not connection.is_connected():
        st.error("No active database connection")
        return None
        
    try:
        cursor = connection.cursor()
        cursor.execute(query, params or ())
        
        if cursor.with_rows:
            result = cursor.fetchall()
            columns = [i[0] for i in cursor.description]
            return pd.DataFrame(result, columns=columns)
        return None
        
    except Error as e:
        error_details = {
            "query": query,
            "params": params,
            "errno": e.errno,
            "sqlstate": e.sqlstate,
            "msg": e.msg
        }
        print(f"❌ Query Failed: {error_details}")
        st.error(f"Query failed: {str(e)}")
        return None
        
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()

create_connection()





'''import mysql.connector
from mysql.connector import Error
import pandas as pd
import streamlit as st

def create_connection():
    """Create a database connection with absolute values"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='vehicle',  # Your exact database name
            user='root',        # Your exact username
            password='ay704321.',  # Your exact password
            port=3306,
            auth_plugin='mysql_native_password',
            connect_timeout=5  # Add timeout to prevent hanging
        )
        
        # Test the connection immediately
        if connection.is_connected():
            test_query = "SELECT 1"
            cursor = connection.cursor()
            cursor.execute(test_query)
            cursor.fetchone()  # Should return (1,)
            cursor.close()
            
            print("✅ MySQL connection successful!")
            return connection
            
    except Error as e:
        error_details = {
            "errno": e.errno,
            "sqlstate": e.sqlstate,
            "msg": e.msg
        }
        print(f"❌ MySQL Connection Failed: {error_details}")
        st.error(f"Database connection failed: {e}")
        return None

def execute_query(connection, query, params=None):
    """Execute a query with error handling"""
    if not connection or not connection.is_connected():
        st.error("No active database connection")
        return None
        
    try:
        cursor = connection.cursor()
        cursor.execute(query, params or ())
        
        if cursor.with_rows:
            result = cursor.fetchall()
            columns = [i[0] for i in cursor.description]
            return pd.DataFrame(result, columns=columns)
        return None
        
    except Error as e:
        error_details = {
            "query": query,
            "params": params,
            "errno": e.errno,
            "sqlstate": e.sqlstate,
            "msg": e.msg
        }
        print(f"❌ Query Failed: {error_details}")
        st.error(f"Query failed: {str(e)}")
        return None
        
    finally:
        if 'cursor' in locals() and cursor:

            cursor.close()'''
