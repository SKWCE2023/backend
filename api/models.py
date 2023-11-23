from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class Service(models.Model):
    code = models.IntegerField()
    service = models.TextField()
    price = models.FloatField()

class Users(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    login = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    ip = models.GenericIPAddressField()
    last_login = models.DateField()
    role = models.IntegerField()
    services_offered = models.JSONField()

class Company(models.Model):
    name = models.CharField(max_length=254)
    address = models.TextField()
    tin = models.IntegerField()
    rs = models.CharField(max_length=50)
    bic = models.CharField(max_length=50)

class Customers(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    login = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    guid = models.CharField(max_length=50, null = True)
    email = models.EmailField(max_length=254)
    ip = models.GenericIPAddressField(null = True)
    social_sec_number = models.CharField(max_length=30, null = True)
    ein = models.CharField(max_length=50, null = True)
    social_type = models.CharField(max_length=50, null = True)
    country = models.CharField(max_length=50, null = True)
    phone = PhoneNumberField()
    passport_series = models.IntegerField()
    passport_number = models.IntegerField()
    dob_timestamp = models.CharField(max_length=50, null=True)
    insurance_name = models.CharField(max_length=50, null = True)
    insurance_address = models.TextField(null = True)
    insurance_inn = models.CharField(max_length=50, null = True)
    insurance_policy = models.CharField(max_length=50, null = True)
    insurance_bik = models.CharField(max_length=50, null = True)
    user_agent = models.TextField(null = True)
    company_name = models.CharField(max_length=254, null = True)

class Order(models.Model):
    bar_code = models.CharField(max_length=50, null=True)
    cost = models.FloatField(null=True)
    creation_date = models.DateTimeField(auto_now=True)
    service = models.ForeignKey("Service", on_delete=models.CASCADE)
    order_status = models.CharField(max_length=30, default="")
    service_status = models.CharField(max_length=30)
    order_completion_time = models.IntegerField(null=True)
    user = models.ForeignKey("Users", on_delete=models.CASCADE)
    customer = models.ForeignKey("Customers", on_delete=models.CASCADE, null=True)

class LoginHistory(models.Model):
    user_login = models.CharField(max_length=50)
    user_name = models.CharField(max_length=50, null=True)
    ip_address = models.GenericIPAddressField()
    login_time = models.DateTimeField(auto_now=True)
    successful = models.BooleanField()

class ServiceRendered(models.Model):
    service = models.ForeignKey('Service', on_delete=models.CASCADE)
    platform = models.CharField(max_length=100)
    performed_by = models.ForeignKey('Users', on_delete=models.CASCADE)
    performed_at = models.DateTimeField(auto_now=True)
    completion_date = models.DateTimeField(null=True)
    avg_deviation = models.FloatField(null=True)

class UtilizerOperation(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    order_received_at = models.DateTimeField(auto_now_add=True)
    service_rendered = models.ForeignKey(Service, on_delete=models.CASCADE)
    execution_completed_at = models.DateTimeField(null=True, blank=True)
