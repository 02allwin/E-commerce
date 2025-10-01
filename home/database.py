import mysql.connector as con

def connect():
    try:
        # Connect to the database
        cnx = con.connect(
            user='root',
            password='root',
            host='127.0.0.1',
            database='ecommerse',
            charset='utf8'
        )
        cnx_cur = cnx.cursor()
        return cnx, cnx_cur

    except con.Error as err:
        print(f"Error: {err}")
        return None, None
