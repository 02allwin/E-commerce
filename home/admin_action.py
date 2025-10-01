                
from home.database import *


# Register your models here.
def display_servicers():
    try:
        conn,cursor =connect()
        cursor.execute("SELECT servicers_user_id, servicers_name, servicers_mobile, servicers_email, servicers_address ,created_at FROM servicers_details")
        data = cursor.fetchall()
        # Convert tuples to list of dictionaries
        servicers = [
            {
                'servicer_id': row[0],
                'servicer_name': row[1],
                'servicer_mobile': row[2],
                'servicer_email': row[3], # Ensure this matches the column name in DB
                'servicer_address': row[4],
                'servicer_created_at': row[5]
            } for row in data
        ]
        count = len(servicers)
        
        return servicers ,count
    except Exception as e:
        print(e)
              
def add_category(name):
    try:
        conn,cursor =connect()
        sql= "insert into services_category (category_name) values (%s)"
        cursor.execute(sql,(name,))
        conn.commit()
        
        if cursor.rowcount:
            return True
        else:
            return False

    except Exception as e:
        print(e)

def display_category():
    try:
        conn,cursor =connect()
        sql= "select * from services_category"
        cursor.execute(sql)
        data = cursor.fetchall()
        
        categories = [
            {
                'id': row[0],
                'name': row[1],
                'created_at': row[2],
            } for row in data
        ]

        return categories
    
    except Exception as e:
        print(e)

def delete_category(id):
    try:
        conn,cursor =connect()
        sql= "delete from services_category where category_id=%s"
        cursor.execute(sql,(id,))
        conn.commit()
    except Exception as e:
        print(e)
             
def update_category(id,name):
    try:
        conn,cursor =connect()
        sql= "update services_category set category_name=%s where category_id=%s"
        cursor.execute(sql,(name,id))
        conn.commit()
    except Exception as e:
        print(e)    
        
def add_city(pincode,name):
    try:
        conn,cursor =connect()
        sql= "insert into service_city (city_pincode,city_name) values (%s,%s)"
        cursor.execute(sql,(pincode,name))
        conn.commit()
        
        if cursor.rowcount:
            return True
        else:
            return False

    except Exception as e:
        print(e)
 

def display_city():
    try:
        conn,cursor =connect()
        sql= "select * from service_city"
        cursor.execute(sql)
        data = cursor.fetchall()
        
        categories = [
            {
                'id': row[0],
                'name': row[1],
                'pincode': row[2],
            } for row in data
        ]

        return categories
    
    except Exception as e:
        print(e)