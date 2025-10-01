"""local_event_finder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from home import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
     path("",views.index,name=""),
     
    path('Users/home.html', views.home, name='home'),
    path('Users/login.html', views.login_view, name='login_view'),
    path('Users/signup.html', views.signup_view, name='signup_view'),
    path('Users/services.html', views.service_list, name='services_list'),
    path("Users/book_service.html",views.book_service,name='book_service'),
    path("Users/booking_success.html",views.booking_success,name='booking_success'),
    path('Users/services/<int:service_id>/', views.service_details, name='service_details'),
    path('Users/booking/<int:service_id>/<int:servicer_user_id>/', views.booking, name='booking'),
    path('Users/view_booking_list.html',views.view_bookings,name="view_bookings"),
    path('Users/delete_booking/<int:booking_id>/',views.delete_booking,name="delete_booking"),
    path("Users/chatbot.html",views.chatBot ,name='chatBot'),
    
    path('services/<int:service_id>/submit_review/', views.submit_review, name='submit_review'),
    path('Servicer/servicer_login.html', views.servicer_login_view, name='servicer_login_view'),
    path('Servicer/servicer_signup.html', views.servicer_signup_view, name='servicer_signup_view'),
    path('Servicer/servicer_dashbord.html', views.servicer_dashbord, name='servicer_dashbord'),
    path("Servicer/add_service.html",views.add_service,name="add_service"),
    path("Servicer/services.html",views.services,name="services"),
    path('add_service/', views.add_service, name='add_service'),
    path('delete_service_request/<int:service_id>',views.delete_service_request ,name="delete_service_request"),
    
    path('Servicer/view_bookings.html',views.request_bookings,name="request_bookings"),
    path('Servicer/logout.html', views.logout_view, name='logout'),
    
    path('Servicer/cancel_booking/<int:booking_id>',views.cancel_booking,name='cancel_booking'),
    path('Servicer/accept_booking/<int:booking_id>',views.accept_booking,name='accept_booking'),
    
    #path('edit_service/<int:service_id>/', views.edit_service, name='edit_service'),
    #path('delete_service/<int:service_id>/', views.delete_service, name='delete_service'),
    #admin
    path('Admin/admin_login.html',views.admin_login,name='admin_login'),
    path('Admin/admin_dashboard.html',views.admin_dashboard,name='admin_dashboard'),
    path('Admin/view_servicers.html',views.list_servicer_details,name='list_servicer_details'),
    path('Admin/category_management.html',views.category_management,name='category_managemen'),
    path('Admin/city_management.html',views.city_management,name='city_management'),
    path('Admin/delete_city/<int:id>',views.delete_city,name='delete_city'),
  
    path('Admin/delete_category/<int:id>',views.delete_category,name='delete_category'),
  
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
