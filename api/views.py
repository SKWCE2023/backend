from django.shortcuts import render
from .models import *
import csv
from django.http import HttpResponse
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from phonenumber_field.phonenumber import PhoneNumber

def import_services_data():
    Service.objects.all().delete()
    try:
        with open('./import_files/services.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader, None)
            # Ensure that the order of columns in the CSV file matches the order of fields in Services model
            for row in csv_reader:
                service = Service(
                    code = row[0],
                    service = row[1],
                    price = row[2]
                )
                service.save()
        print('Services data imported successfully')
    except Exception as e:
        print(f'Error importing Services data: {e}')

def import_users_data():
    Users.objects.all().delete()
    try:
        with open('./import_files/users.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader, None)
            # Ensure that the order of columns in the CSV file matches the order of fields in Users model
            for row in csv_reader:
                full_name = row[1].split()
                user = Users(
                    first_name = full_name[0],
                    last_name = full_name[1],
                    login = row[2],
                    password = row[3],
                    ip = row[4],
                    lastLogin = datetime.strptime(row[5], '%m/%d/%Y').strftime('%Y-%m-%d'),
                    services_offered = row[6],
                    role = row[7],
                )
                user.save()
        print('Users data imported successfully')
    except Exception as e:
        print(f'Error importing Users data: {e}')

def import_customers_data():
    Customers.objects.all().delete()
    try:
        tree = ET.parse('./import_files/clients.xml')
        root = tree.getroot()
        for item in root.findall('record'):
            full_name = item.find('fullname').text.split() 
            customer = Customers(
                first_name = full_name[0],
                last_name = full_name[1],
                login = item.find('login').text,
                password = item.find('pwd').text,
                email = item.find('email').text,
                guid = item.find('guid').text,
                ip = item.find('ipadress').text,
                social_sec_number = item.find('social_sec_number').text,
                ein = item.find('ein').text,
                social_type = item.find('social_type').text,
                country = item.find('country').text,
                phone = item.find('phone').text,
                passport_series = item.find('passport_s').text,
                passport_number = item.find('passport_n').text,
                dob_timestamp = item.find('birthdate_timestamp').text,
                insurance_name = item.find('insurance_name').text,
                insurance_address = item.find('insurance_address').text,
                insurance_inn = item.find('insurance_inn').text,
                insurance_policy = item.find('insurance_pc').text,
                insurance_bik = item.find('insurance_bik').text,
                user_agent = item.find('ua').text
            )
            customer.save()
        print('Customers data imported successfully')
    except Exception as e:
        print(f'Error importing customers data: {e}')

def user_logout(request):
    time = datetime.now() + timedelta(minutes=15)
    request.session['login_blocked_until'] = time.strftime('%m/%d/%Y, %H:%M:%S')
    return JsonResponse({'status': 'success'}, status = 200)

@csrf_exempt 
def user_login(request):
    try:
        # Check if login is blocked
        login_blocked_until = request.session.get('login_blocked_until')
        if login_blocked_until and datetime.strptime(login_blocked_until, '%m/%d/%Y, %H:%M:%S') > datetime.now():
            res = {
                'status': 'error',
                'message': 'Login is blocked for 15 minutes. Please try again later.',
                'error_type': 'LoginBlockedException'
            }
            return JsonResponse(res, status = 503)

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = Users.objects.filter(login=username, password=password)
        ip_address = request.META.get('REMOTE_ADDR')
        LoginHistory.objects.create(user_login=username, user_name=username, ip_address=ip_address, successful=user.exists())
        if user.exists():
            user.update(lastLogin = datetime.now().strftime('%Y-%m-%d'))
            res = {
                'status': 'success',
                'data': list(user.values()),
            }
            return JsonResponse(res, status = 200)
        else:
            res = {
                'status': 'error',
                'message': 'Invalid username or password. Please try again.',
                'error_type': 'InputException'
            }
            return JsonResponse(res, status = 404)
    except Exception as e:
        res = {
            'status': 'error',
            'message': 'Internal Server Error',
            'error_type': 'DatabaseException'
        }
        return JsonResponse(res, status = 500)

def login_history(request):
    try:
        data = []
        search = request.GET.get('search')
        ordering = request.GET.get('ordering')
        order_by = 'login_time'
        if ordering == 'descending':
            order_by = '-login_time'
        if search:
            data = LoginHistory.objects.filter(user_name__startswith=search).order_by(order_by)
        else:
            data = LoginHistory.objects.all().order_by(order_by)
        res = {
            'status': 'success',
            'message': None,
            'data': list(data.values()),
            'error_type': None
        }
        return JsonResponse(res, status = 200)
    except Exception as e:
        res = {
            'status': 'error',
            'message': 'Internal Server Error',
            'error_type': 'DatabaseException'
        }
        return JsonResponse(res, status = 500)

@csrf_exempt        
def create_order(request):
    try:
        if request.method == 'POST':
            service_id = request.POST.get('service_id')
            order_completion_time = request.POST.get('order_completion_time')
            user_id = request.POST.get('user_id')
            order = Order.objects.create(
                service_id=service_id,
                order_status=order_status,
                service_status=service_status,
                order_completion_time=order_completion_time,
                user_id=user_id
            )
            return JsonResponse({'status': 'success', 'message': 'Order created successfully'}, 200)
    except Exception as e:
        res = {
            'status': 'error',
            'message': 'Internal Server Error',
            'data': None,
            'error_type': 'DatabaseException'
        }
        return JsonResponse(res, status = 500)

def get_last_order_id(request):
    try:
        last_order = Order.objects.latest('creation_date')
        res = {
            'status': 'success',
            'data': last_order.id,
        }
        return JsonResponse(res, 200)
    except Order.DoesNotExist:
        res = {
            'status': 'error',
            'message': 'No orders found',
            'error_type': 'DoesNotExistException'
        }
        return JsonResponse(res, 404)

@csrf_exempt
def create_customer(request):
    try:
        if request.method == 'POST':
            data = request.POST
            customer = Customers.objects.create(
                first_name = data.get('first_name'),
                last_name = data.get('last_name'),
                login = data.get('login'),
                password = data.get('password'),
                passport_series = data.get('passport_series'),
                passport_number = data.get('passport_number'),
                dob_timestamp = int(datetime.strptime(data.get('date_of_birth'), '%d/%m/%Y').timestamp()),
                phone = PhoneNumber.from_string(data.get('phone_number')),
                email = data.get('email'),
                guid = data.get('guid', None),
                ip = data.get('ip', None),
                social_sec_number = data.get('social_sec_number', None),
                ein = data.get('ein', None),
                social_type = data.get('social_type', None),
                country = data.get('country', None),
                insurance_name = data.get('insurance_name', None),
                insurance_address = data.get('insurance_address', None),
                insurance_inn = data.get('insurance_inn', None),
                insurance_policy = data.get('insurance_policy', None),
                insurance_bik = data.get('insurance_bik', None),
                user_agent = data.get('user_agent', None)
                )
            return JsonResponse({'message': 'Customer created successfully'}, status = 201)
    except Exception as e:
        res = {
            'status': 'error',
            'message': 'Internal Server Error',
            'error_type': 'DatabaseException'
        }
        return JsonResponse(res, status = 500)

def create_company(request):
    try:
        # Retrieve data from the POST request
        data = request.POST
        new_company = Company(
            name=data.get('name'),
            address=data.get('address'),
            tin=int(data.get('tin')),
            rs=data.get('rs'),
            bic=data.get('bic')
        )
        new_company.save()
        return JsonResponse({'message': 'Company created successfully'}, status = 201)

    except Exception as e:
        res = {
            'status': 'error',
            'message': 'Internal Server Error',
            'error_type': 'DatabaseException'
        }
        return JsonResponse(res, status = 500)