                
from home.database import *


def findUser(email, pwd):
    cnx , cnx_cur = connect()
    sql ="select user_id from users where user_email=%s and user_password=%s"
    val= (email,pwd)
    cnx_cur.execute(sql,val)
    result = cnx_cur.fetchone()
    cnx.close()
    if result:
        return result[0]
    else:
        return None

def available_datas():
    try:
        con, cursor = connect()
        cursor.execute("SELECT city_name FROM service_city")
        cities = [row[0] for row in cursor.fetchall()]  # Extracting actual city names
        cursor.execute("SELECT category_name FROM services_category")
        categories = [row[0] for row in cursor.fetchall()]  # Extracting actual category names

        return {'cities': cities, 'categories': categories}
    except Exception as e:
        print(e)
        return {'cities': [], 'categories': []}

def apply_filter(cities ,category):
    # This function is used to filter services based on user input
    try:
        con, cursor = connect()
        # Fetch all services
        query = """
            SELECT 
                s.service_id, 
                s.service_name, 
                s.service_description, 
                s.service_price, 
                s.service_image,
                s.city_pincode
            FROM service s
            INNER JOIN services_category sc ON s.category_id = sc.category_id
            INNER JOIN service_city ci ON s.city_pincode = ci.city_pincode
            WHERE ci.city_name = %s or sc.category_name = %s
        """
        cursor.execute(query, (cities, category))

        filtered_data = cursor.fetchall()
        if filtered_data:
            return filtered_data
        else:
            return None
    except Exception as e:
        print(e)

def add_review(service_id ,user_id ,rating,review):
    try:
        con, cursor = connect()
        query = """
        INSERT INTO reviews (service_id, user_id,  rating,review)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query,(service_id,user_id,rating,review))
        con.commit()
        if cursor.rowcount:
            return True
        else:
            return False
    except Exception as e:
        print(e)

def count_and_avg(service_id):
    try:
        con, cursor = connect()
        
        query = "SELECT AVG(rating), COUNT(review) FROM reviews WHERE service_id = %s"
        cursor.execute(query, (service_id,))  # Tuple must have a comma

        data = cursor.fetchone()
        
        return data  # Returns (avg_rating, total_reviews)
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()

def view_review(service_id):
    try:
        con, cursor = connect()
        query = """
        SELECT users.user_name, reviews.rating, reviews.review, reviews.created_at FROM reviews 
        JOIN users ON reviews.user_id = users.user_id 
        WHERE reviews.service_id = %s
        ORDER BY reviews.created_at DESC
        """
        cursor.execute(query, (service_id,))
        reviews = cursor.fetchall()
        return reviews
    except Exception as e:
        print(e)
        
def get_service_details(service_id):
    try:
        con ,cursor = connect()
            # Fetch service details
        cursor.execute("""
                SELECT s.service_id, s.service_name, s.service_description, s.service_price, 
                    s.service_image, s.city_pincode, s.service_address, 
                    sd.servicers_name, sd.servicers_mobile, sd.servicers_email, sd.servicers_address ,
                    s.servicers_user_id
                FROM service s
                JOIN servicers_details sd ON s.servicers_user_id = sd.servicers_user_id
                WHERE s.service_id = %s
            """, [service_id])

        service = cursor.fetchone()
        datas= view_review(service_id)
        counts = count_and_avg(service_id)
        if counts[0]:
            avg = float(counts[0])
            count = counts[1]
        else:
            avg = 0
            count = 0
        if datas:
            reviews=[
                {
                'user_name':data[0],
                'rating':data[1],
                'review':data[2],
                'date':data[3],
                } for data in datas
            ]
        else:
            reviews = None
            
        if service :
            service_data = {
                'service_id': service[0],
                'service_name': service[1],
                'service_description': service[2],
                'service_price': service[3],
                'service_image': service[4],
                'city_pincode': service[5],
                'service_address': service[6],
                'owner_name': service[7],
                'owner_mobile': service[8],
                'owner_email': service[9],
                'owner_address': service[10],
                'servicer_user_id':service[11]
            }
    
        else:
            service_data = None
        
        return (service_data,reviews,avg,count)
    except Exception as e:
        print(e)

def booking_category(service_id,service_user_id , user_id, booker_name, email, mobile, address, category_name,price, date, time, other_value):
    try:
        con, cursor = connect()  # Ensure this function returns a valid DB connection
        
        print(category_name)
        set1 = {"Hall", "Conference Rooms", "Private Party Venues"}
        
        # Define query and data dynamically
        if category_name in set1:
            query = """
                INSERT INTO bookings (service_id,servicer_user_id, user_id, booker_name, email, mobile, address, category_name,price, date, time, guests)
                VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s)
            """
            data = (service_id,service_user_id , user_id, booker_name, email, mobile, address, category_name,price, date, time, other_value)
        
        elif category_name == "DJ Services":
            query = """
                INSERT INTO bookings (service_id,servicer_user_id, user_id, booker_name, email, mobile, address, category_name,price, date, time, dj_name)
                VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s)
            """
            data = (service_id,service_user_id , user_id, booker_name, email, mobile, address, category_name,price, date, time, other_value)

        elif category_name == "Wedding & Stage Decoration":
            query = """
                INSERT INTO bookings (service_id,servicer_user_id, user_id, booker_name, email, mobile, address, category_name,price, date, time, theme)
                VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s)
            """
            data = (service_id,service_user_id , user_id, booker_name, email, mobile, address, category_name,price, date, time, other_value)

        elif category_name == "Birthday Party":
            query = """
                INSERT INTO bookings (service_id,servicer_user_id,  user_id,booker_name, email, mobile, address, category_name,price, date, time, birthday_age)
                VALUES (%s, %s,%s, %s, %s, %s, %s, %s, %s, %s,%s,%s)
            """
            data = (service_id,service_user_id , user_id, booker_name, email, mobile, address, category_name,price, date, time, other_value)
        
        else:
            print("Invalid category!")
            return False

        cursor.execute(query, data)
        print(data)
        con.commit()

        if cursor.rowcount:
            return True
        else:
            return False

    except Exception as e:
        print("Error:", e)
        return False

    finally:
        cursor.close()
        con.close()


def retrive_bookings(user_id):
    
    try:
        con,cur = connect()
        sql = """
        SELECT b.booking_id,b.service_id,s.service_image,b.date,b.time,b.address,b.mobile,b
            .booker_name,b.email,b.category_name,b.price,bs.status,s.service_name FROM bookings b
            INNER JOIN booking_status bs ON b.booking_id = bs.booking_id        
            Inner join service s on s.service_id = b.service_id 
            WHERE b.user_id = %s ORDER BY b.booking_id DESC;
            """
        val = (user_id,)
        cur.execute(sql, val)
        datas = cur.fetchall()
        print(datas)
            
        if datas:
            bookings_data=[
                {
                    "booking_id":data[0],
                    "service_id":data[1],
                    "service_image":data[2],
                    "booking_date":data[3],
                    "booking_time":data[4],
                    "booking_location":data[5],
                    "booking_mobile":data[6],
                    "booker_name":data[7],
                    "booker_email":data[8],
                    "category_name":data[9],
                    "booking_price":data[10],
                    "booking_status":data[11],
                    "service_name":data[12],
                } for data in datas
                ]
            return bookings_data
        else:
            return None
    except Exception as e:
        print("Error ",e)