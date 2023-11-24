from .. import views

def run():
    views.import_services_data()
    views.import_users_data()
    views.import_customers_data()
    views.create_temp_administrators()