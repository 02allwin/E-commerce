from home.database import *
import pandas as pd 
import matplotlib.pyplot as plt
import calplot
import os
from django.conf import settings

servicer_user_id=None

def findServicer(email ,password):
    try:
        con ,cur = connect()
        query = "SELECT servicers_user_id , servicers_name FROM servicers_details where servicers_email = %s and servicers_password = %s"
        cur.execute(query , (email,password))
        data = cur.fetchone()
        print(data)
        return data
    except Exception as e:
        print(f"Error: {e}")

def registerServicer(serName,serMobile,serEmail,serPassword,serAddress):
    try:
        con,cur = connect()
        query = """INSERT INTO servicers_details(
            servicers_name,
            servicers_mobile,
            servicers_email,
            servicers_password,
            servicers_address
        )values(%s,%s,%s,%s,%s)"""
        print((serName,serMobile,serEmail,serPassword,serAddress))
        cur.execute(query , (serName,serMobile,serEmail,serPassword,serAddress))
        con.commit()
        if cur.rowcount >0:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error: {e}")

def availableCategory():
    try:
        con,cur = connect()
        query = "SELECT  category_name FROM services_category"
        cur.execute(query)
        data = [row[0] for row in cur.fetchall()]  # Extracting actual city 

        return data
    except Exception as e:
        print(f"Error: {e}")
        
def availableCity():
    try:
        con,cur = connect()
        query = "SELECT city_pincode  FROM service_city"
        cur.execute(query)
        data = [row[0] for row in cur.fetchall()]  # Extracting actual city
        return data
    except Exception as e:
        print(f"Error: {e}")
        
def inserService(sername,serDesc,serPrice,serImage,cityPin,serAdd,categoryId,serUserId):
    try:
        con,cur = connect()
        query = """INSERT INTO service(
            service_name,
            service_description,
            service_price,
            service_image,
            city_pincode,
            service_address,
            category_id,
            servicers_user_id
            )values(%s,%s,%s,%s,%s,%s,%s,%s)
        """
        val=(sername,serDesc,serPrice,serImage,cityPin,serAdd,categoryId,serUserId)
        print(val)
        cur.execute(query , val)
        con.commit()
        if cur.rowcount >0:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error: {e}")

def delete_service(service_id):
    try:
        con,cur = connect()

        sql = "delete  from service where service_id=%s"
        val=(service_id,)
        cur.execute(sql,val)
        con.commit()
        return True

    except Exception as e:
        print("Error ",e)
        return False

def getPineCode_ID(pincode):
    try:
        con,cur = connect()
        query = "SELECT city_pincode_id FROM service_city WHERE city_pincode = %s"
        cur.execute(query,(pincode,))
        data = cur.fetchone()
        return data[0]
    except Exception as e:
        print(f"Error: {e}")
        
def getCategoryId(categoryName):
    try:
        con,cur = connect()
        query = "SELECT category_id FROM services_category WHERE category_name = %s"
        cur.execute(query,(categoryName,))
        data = cur.fetchone()
        return data[0]
    except Exception as e:
        print(f"Error: {e}")
                
def view_bookings_from_servicer(servicer_id):
    print('kk')
    try:
        print("hello")
        con,cur = connect()
        print("hello")
        query = """
        SELECT b.booking_id , 
                b.user_id,
                b.booker_name,
                b.email,
                b.mobile,
                b.address,
                b.category_name,
                b.date,
                b.time
        FROM bookings b INNER JOIN 
        booking_status bs ON bs.booking_id=b.booking_id WHERE bs.status='PENDING' and b.servicer_user_id=%s
        """
        val=(servicer_id ,)
        print(val)
        cur.execute(query,val)
        data = cur.fetchall()
        return data
    except Exception as e:
        print(f"Error: {e}")
        
def collect_date(servicer_id):
    con ,cur =connect()
    sql="""
        SELECT b.date,b.time ,bs.status FROM bookings b INNER JOIN
        booking_status bs ON b.booking_id = bs.booking_id WHERE b.servicer_user_id =%s and bs.status="ACCEPT" """
    val=(servicer_id,)
    cur.execute(sql,val)
    data = cur.fetchall()
    return data

def change_booking_status(booking_id,status):
    try:
        print(status,booking_id)
        con,cur = connect()
        sql = """UPDATE booking_status SET status = %s WHERE booking_id = %s"""
        val = (status,booking_id)
        cur.execute(sql, val)
        con.commit()
    except Exception as e:
        print(f"Error: {e}")