from django.contrib import admin
from . import models

# Register your models here.
class CustomAdmin(admin.AdminSite):
    site_header= "Custom Admin Area"
    login_template= "custom_login/admin/admin_login.html"

custom_site = CustomAdmin(name='CustomAdmin')
custom_site.register(models.User)
