from django.shortcuts import render
from home.database import *
import mysql.connector
from mysql.connector import Error
# Create your views here.
from home.user_action import *
from home.servicers_action import *
from home.admin_action import *
import re
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseBadRequest
from home.chatbot import *

username = None
url =None
def index(request):
    return render(request,"index.html",{})


#User Action

def home(request):
    return render(request,"Users/home.html",{})

def login_view(request):
    user_id = request.session.get('user_id')
    if  user_id:
        return render(request, 'Users/home.html')
    
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['pwd']
        try:
            userid = findUser(email , password)
            if userid == None:
                return render(request,"Users/login.html",{'error': 'Invalid username or password'})
            else:
                request.session['user_id'] = userid
                return render(request,"Users/home.html",{})

        except Exception as  e:
            return render(request,"Users/login.html",{'error': e})
    else:
        return render(request,"Users/login.html",{})

def signup_view(request):
    global username
    if request.method == 'POST':
       try:
            un = request.POST['username']
            email = request.POST['email']
            mobile = request.POST['mobile']
            password = request.POST['password']
            confirm_password = request.POST['confirm_password']
            if password == confirm_password:
                conn,cur = connect()
                val =(un,email,password,mobile)
                cur.execute("INSERT INTO users (user_name,user_email,user_password,user_mobile) VALUES (%s,%s,%s,%s)",val)
                conn.commit()
                if cur.rowcount:
                    username = un
                    request.session['user_name'] = username
                    return render(request, 'Users/login.html')
                else:
                    return render(request, 'Users/signup.html', {'error': 'Username already exists.'})
                conn.close()
            else:
                return render(request, 'Users/signup.html', {'error': 404}) #203 - password does not match 
       except mysql.connector.IntegrityError as e:
            if e.errno == 1062:
                return render(request, 'Users/signup.html', {'error': "allready exist email"}) #allready exist email - 1062
            else:
                return render(request, 'Users/signup.html', {'error': e}) 
    else:
        return render(request, 'Users/signup.html')

def service_details(request, service_id):
    user_id = request.session.get('user_id')
    if  not user_id:
        return render(request, 'Users/login.html')
    
    service_data ,reviews ,avg,count = get_service_details(service_id)
    return render(request, 'Users/services_details.html', {'service': service_data ,'reviews':reviews,'avg_rating':avg,'total_reviews':count})


def submit_review(request, service_id):
    # Fetch service details
    service_data, reviews, avg, count = get_service_details(service_id)
    
    # Check if user is logged in
    user_id = request.session.get('user_id')
    if not user_id:
        return render(request, 'Users/login.html')

    if request.method == "POST":
        try:
            review = request.POST.get('review', '').strip()
            rating = request.POST.get('rating', '').strip()

            # Validate rating (ensure it is a number)
            if not rating.isdigit():
                messages.error(request, "Invalid rating. Please enter a number.")
                return render(request, 'Users/services_details.html', {'service': service_data, 'reviews': reviews, 'avg_rating': avg, 'total_reviews': count})
            
            print(rating)
            rating = int(rating)

            # Add review
            valBool = add_review(service_id, user_id, review=review, rating=rating)
            if valBool:
                service_data, reviews, avg, count = get_service_details(service_id)
                messages.success(request, "Review submitted successfully!")
                return render(request, 'Users/services_details.html', {'service': service_data, 'reviews': reviews, 'avg_rating': avg, 'total_reviews': count})
            else:
                messages.error(request, "Review already exists.")
                return render(request, 'Users/services_details.html', {'service': service_data, 'reviews': reviews, 'avg_rating': avg, 'total_reviews': count})

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return render(request, 'Users/services_details.html', {'service': service_data, 'reviews': reviews, 'avg_rating': avg, 'total_reviews': count})

    # If request is GET, show the service details page
    return render(request, 'Users/services_details.html', {'service': service_data, 'reviews': reviews, 'avg_rating': avg, 'total_reviews': count})

def service_list(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return render(request, 'Users/login.html')

    available_data = available_datas()
    choose = {
        "service_type": available_data["categories"],
    }

    services = []
    responses = None
    user_message = None

    # GET request → load all services
    if request.method == 'GET':
        conn, cursor = connect()
        cursor.execute(
            "SELECT service_id, service_name, service_description, service_price, service_image, city_pincode FROM service"
        )
        data = cursor.fetchall()
        services = [
            {
                'service_id': row[0],
                'service_name': row[1],
                'service_description': row[2],
                'service_price': row[3],
                'serimage': row[4],
                'city_pincode': row[5]
            }
            for row in data
        ]

    # POST request
    elif request.method == "POST":
        # Case 1: Chatbot message
        if "user" in request.POST:
            user_message = request.POST['user']
            model = ChatBot(user_message)
            run_query = RunQuery()
            sql, val = model.get_query()
            print(sql, val)
            responses = run_query.run_chatbot_query(sql, val)

        # Case 2: Filters
        else:
            try:
                category = request.POST.get('category', '')
                city = request.POST.get('city', '')

                filtered_data = apply_filter(city, category)
                if filtered_data:
                    services = [
                        {
                            'service_id': row[0],
                            'service_name': row[1],
                            'service_description': row[2],
                            'service_price': row[3],
                            'serimage': row[4],
                            'city_pincode': row[5]
                        }
                        for row in filtered_data
                    ]
                else:
                    services = []

            except Exception as e:
                return render(request, 'Users/services.html', {'error': str(e)})

    return render(
        request,
        'Users/services.html',
        {
            'services': services,
            'choose': choose,
            'responses': responses,
            'user_message': user_message
        }
    )

def book_service(request):
    return render(request, 'Users/book_service.html')

def booking_success(request):
    return render(request, 'Users/booking_success.html')

def booking(request,service_id,servicer_user_id):
    user_id = request.session.get('user_id')
    if  not user_id:
        return render(request, 'User/user_login.html')
    
    print(service_id,servicer_user_id)
    if request.method == 'POST':
        try:
            service_id = service_id
            booking_date = request.POST['booking_date']
            booking_time = request.POST['booking_time']
            address= request.POST['address']
            contact_number = request.POST['contact_number']
            booker_name=request.POST['booker_name']
            booker_email=request.POST['booker_email']
            category_name = request.POST['category_name']
            price = request.POST['price']
            
            print(service_id,servicer_user_id ,user_id,booker_name,
                                       booker_email,contact_number,address,
                                       category_name,price,booking_date,booking_time)
            
            valBool = booking_category(service_id,servicer_user_id ,user_id,booker_name,
                                       booker_email,contact_number,address,
                                       category_name,price,booking_date,booking_time)
            if valBool:
                return render(request, 'Users/booking_success.html')
            else:
                return render(request, 'Users/booking.html')
        except Exception as e:
            print("Eror ",e)
            return render(request, 'Users/booking.html', {'error': e})
    
    else:
        try:
            con,cur = connect()
            sql="""
            SELECT s.service_price ,sc.category_name FROM service s INNER JOIN services_category sc ON
            sc.category_id = s.category_id WHERE s.service_id=%s;
            """
            val=(service_id,)
            cur.execute(sql,val)
            data = cur.fetchone()
            if data:
                category_name = data[1]
                price = data[0]
                return render(request, 'Users/booking.html', {
                'category_name': category_name,
                'price':price,
                'service_id': service_id,
                'servicer_user_id': servicer_user_id
            })

            else:
                category_name = "No Category"
                price ="No price"
                return render(request, 'Users/booking.html', {
                'category_name': category_name,
                'price':price,
                'service_id': service_id,
                'servicer_user_id': servicer_user_id
            })
        except Exception as e:
            print("Error ",e)
            return render(request, 'Users/booking.html')

def view_bookings(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return render(request, 'User/user_login.html')
    bookings_data = retrive_bookings(user_id)
    return render(request, 'Users/view_booking_list.html', {'bookings': bookings_data})


def delete_booking(request,booking_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return render(request, 'User/user_login.html')
    try:
        con,cur = connect()
        sql = "delete from bookings where booking_id=%s"
        val = (booking_id,)
        cur.execute(sql, val)
        con.commit()
        
        bookings_data = retrive_bookings(user_id)
        return render(request, 'Users/view_booking_list.html', {'bookings': bookings_data})
    
    except Exception as e:
        print("Error ",e)
        return render(request, 'Users/view_booking_list.html')
    
    

def chatBot(request):
    if request.method=="POST":

        message = request.POST['user']

        model = ChatBot(message)
        run_query = RunQuery()
        sql,val =model.get_query()
        print(sql,val)
        responses =  run_query.run_chatbot_query(  sql,val )
        
        return render(request,"Users/chatbot.html",{'responses':responses})
    else:
        return render(request ,'Users/chatbot.html')
    

# Servicer Action

def servicer_login_view(request):
    servicer_user_id = request.session.get('servicer_user_id')
    if  servicer_user_id:
        return render(request, 'Servicer/servicer_dashbord.html')
    
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        print(email,password)
        try:
            data = findServicer(email , password)
            print(data)
            if data == None:
                return render(request,"Servicer/servicer_login.html",{'error': 'Invalid username or password'})
            else:
                #username = data[0][0]
                servicer_user_id=data[0]
                request.session['servicer_user_id'] = servicer_user_id
                return render(request,"Servicer/servicer_dashbord.html",{})

        except Exception as  e:
            return render(request,"Servicer/servicer_login.html",{'error': e})
    else:
        
        return render(request,"Servicer/servicer_login.html",{})

def servicer_signup_view(request):
    #global admin_username
    if request.method == 'POST':
            un = request.POST['fullname']
            email = request.POST['email']
            mobile = request.POST['mobile']
            password = request.POST['password']
            confirm_password = request.POST['confirm_password']
            address =None
            if password == confirm_password:
                boolVal= registerServicer(un,mobile,email,password,address)
                if boolVal:
                    username = un
                    request.session['servicer_user_id'] = servicer_user_id
                    return render(request, 'Servicer/servicer_login.html')
                else:
                    return render(request, 'Servicer/servicer_signup.html', {'error': 'Username already exists.'})
            else:
                return render(request, 'Servicer/servicer_signup.html', {'error': 404}) #203 - password does not match 
    else:
        return render(request, 'Servicer/servicer_signup.html')
    
def servicer_dashbord(request):
    
    servicer_user_id = request.session.get('servicer_user_id')
    if not servicer_user_id:
        return render(request,'Servicer/servicer_login.html') 
    return render(request, 'Servicer/servicer_dashbord.html')

def logout_view(request):
    request.session.flush()  # Clears the session
    return render(request, 'Servicer/servicer_login.html')

def services(request):
    servicer_user_id = request.session.get('servicer_user_id')
    if not servicer_user_id:
        return render(request,'Servicer/servicer_login.html') 
    if request.method == "GET":
        try:
           
            con, cur = connect()
            cur = con.cursor()  # Fetch as dictionary
              # Replace with `servicer_id` if it's set properly
            
            sql ="""
            SELECT s.service_id, s.service_name, s.service_description, s.service_price,  s.service_image, s.city_pincode, s.service_address ,sc.category_name 
            FROM service s INNER JOIN  services_category sc on
            s.category_id = sc.category_id
            WHERE servicers_user_id =%s
            """
            print("Executing SQL:", sql, "with parameter:", servicer_user_id)
            
            cur.execute(sql, (servicer_user_id,))
            data = cur.fetchall()
           
            if data:
                services = [
                {
                'service_id': row[0],
                'service_name': row[1],
                'service_description': row[2],
                'service_price': row[3],
                'serimage': row[4],  # Ensure this matches the column name in DB
                'city_pincode': row[5],
                'service_address':row[6],
                'category_name':row[7]
                } for row in data]
                return render(request, "Servicer/services.html", {'services': services})
            else:
                print("No services found for servicer_user_id =", servicer_user_id)
                return render(request, "Servicer/services.html", {'error': 'No services available'})

        except Exception as e:
            print("Error:", str(e))
            return render(request, 'Servicer/services.html', {'error': str(e)})
    else:
        return render(request, 'Servicer/servicer_dashbord.html')

def add_service(request):
    servicer_user_id = request.session.get('servicer_user_id')
    if not servicer_user_id:
        return render(request, 'Servicer/servicer_login.html')

    if request.method == "POST":
        try:
            service_name = request.POST['service_name']
            service_description = request.POST['service_description']
            service_price = request.POST['service_price']
            city_pincode = request.POST['city_pincode']
            service_address = request.POST['service_address']
            category_name = request.POST['category_id']
            category_id = getCategoryId(category_name)

            # Handle file upload properly
            service_image = request.FILES.get('service_image')
            if service_image:
                fs = FileSystemStorage()
                filename = fs.save(service_image.name, service_image)
                service_image = fs.url(filename)  # Store the path

            valBool = inserService(service_name, service_description, service_price,
                                   service_image, city_pincode, service_address,
                                   category_id, servicer_user_id)

            if valBool:
                message = "<div class='alert alert-success'>Added successfully!</div>"
            else:
                message = "<div class='alert alert-danger'>Failed to add</div>"

            return render(request, 'Servicer/add_service.html', {'message': message})
        
        except Exception as e:
            print("Error:", str(e))
            return render(request, 'Servicer/add_service.html', {'message': str(e)})

    else:
        try:
            available_category = availableCategory()
            available_pincodes = availableCity()
            choose = {
                "categories": available_category,
                "pinecodes": available_pincodes,
            }
            return render(request, 'Servicer/add_service.html', {'choose': choose})
        except Exception as e:
            print("Error:", str(e))
            return render(request, 'Servicer/add_service.html', {'message': str(e)})

def delete_service_request(request,service_id):
    servicer_user_id = request.session.get('servicer_user_id')
    if not servicer_user_id:
        return render(request, 'Servicer/servicer_login.html')
  
    try:
        flag = delete_service(service_id)
        if flag:
            return redirect("services")
        else:
            return render(request ,"Servicer/services.html",{"error_msg":1})
        
    except Exception as e:
        print("Error 2",e)
        return render(request ,'Servicer/services.html')
    
def request_bookings(request):
    servicer_user_id = request.session.get('servicer_user_id')
    if not servicer_user_id:
        return render(request, 'Servicer/servicer_login.html')
  
    try:
        if request.method == "GET":
            print("hi")
            print(servicer_user_id)
            
            
            bookings= view_bookings_from_servicer(servicer_user_id)
            
            if bookings:
                booking_list=[
                    {
                        "booking_id":booking[0],
                        "user_id":booking[1],
                        "booker_name":booking[2],
                        "booker_email":booking[3],
                        "booker_mobile":booking[4],
                        "booker_address":booking[5],
                        "category":booking[6],
                        "booking_date":booking[7],
                        "booking_time":booking[8],
                    } for booking in bookings 
                ]
                print(booking_list)
                return render(request, 'Servicer/view_bookings.html', {'booking_list': booking_list})
            else:
                return render(request, 'Servicer/view_bookings.html',{"booking_list":0})
        else:
            return render(request, 'Servicer/view_bookings.html',{"booking_list":0})
    except Exception as e:
        print("Error:", str(e))
        return render(request, 'Servicer/view_bookings.html',{"booking_list":0,'image_url':url})

         
def accept_booking(request , booking_id):
    global url
    servicer_user_id = request.session.get('servicer_user_id')
    if not servicer_user_id:
        return render(request, 'Servicer/servicer_login.html')
    try:
        change_booking_status(booking_id,"ACCEPT")
        return render (request, 'Servicer/view_bookings.html', {'url': url})
    except Exception as e:
        print("Error:", str(e))
        return render(request, 'Servicer/view_bookings.html',{"url":0})
     
def cancel_booking(request , booking_id):
    servicer_user_id = request.session.get('servicer_user_id')
    if not servicer_user_id:
        return render(request, 'Servicer/servicer_login.html')
    global url
    try:
        change_booking_status(booking_id,"CANCEL")
        return render (request, 'Servicer/view_bookings.html', {'url': url})
    except Exception as e:
        print("Error:", str(e))
        return render(request, 'Servicer/view_bookings.html',{"url":0})
    
    
#Admin 

def admin_login(request):
    return render(request,'Admin/admin_login.html')

def admin_dashboard(request):
    
    if request.method == "GET":
        conn,cursor =connect()
        cursor.execute("SELECT service_id, service_name, service_description, service_price, service_image, city_pincode FROM service")
        data = cursor.fetchall()
        # Convert tuples to list of dictionaries
        services = [
            {
                'service_id': row[0],
                'service_name': row[1],
                'service_description': row[2],
                'service_price': row[3],
                'serimage': row[4],  # Ensure this matches the column name in DB
                'city_pincode': row[5]
            } for row in data
        ]
        count = len(services)
        return render(request, 'Admin/admin_dashboard.html', {'services': services,'count':count})

    return render(request,'Admin/admin_dashboard.html')

def list_servicer_details(request):
    if request.method =="GET":
        servicers,count = display_servicers()
        return render(request, 'Admin/view_servicers.html', {'servicers': servicers,'count':count})
    

def city_management(request):
    
    cities =  display_city()
    if request.method=="POST":
        name = request.POST['city_name']
        pincode = request.POST['city_pincode']
        bo = add_city(pincode,name)
       
        if bo:
            return render(request, 'Admin/city_management.html',{'result':"Success" ,"cities":cities})
        else:
            return render(request, 'Admin/city_management.html',{'result':'failure'})
    
    else:
       
        cities =  display_city()
        return render(request, 'Admin/city_management.html',{'cities':cities})
   
def update_city( request, id,name):
    try:
        conn,cursor =connect()
        sql= "update service_city set city_name=%s, city_pincode =%s  where service_city_id=%s"
        cursor.execute(sql,(name,id))
        conn.commit()
    except Exception as e:
        print(e)
          
def delete_city(request,id):
    cities =  display_city()
    try:
        conn,cursor =connect()
        sql= "delete from service_city where service_city_id=%s"
        cursor.execute(sql,(id,))
        conn.commit()
        return render(request, 'Admin/city_management.html',{'result':"Success" ,"cities":cities})
    except Exception as e:
        print(e)
        return render(request, 'Admin/city_management.html',{'result':"Success" ,"cities":cities})

def category_management(request):
    
    categories =  display_category()
    if request.method=="POST":
        name = request.POST['category_name']
        bo = add_category(name)
        if bo:
            return render(request, 'Admin/category_management.html',{'result':"Success",'categories':categories})
        else:
            return render(request, 'Admin/category_management.html',{'result':'failure'})
    
    else:
        
        return render(request, 'Admin/category_management.html',{'categories':categories})

def delete_category(request,id):
    categories =  display_category()
    try:
        conn,cursor =connect()
        sql= "delete from services_category where category_id=%s"
        cursor.execute(sql,(id,))
        conn.commit()
        return render(request, 'Admin/category_management.html',{'result':"Success",'categories':categories})
    except Exception as e: 
        print(e)
        return render(request, 'Admin/category_management.html',{'result':"Success",'categories':categories})
   
