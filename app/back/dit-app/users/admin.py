from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from . import models  as usr_mdl


admin.site.register(get_user_model(), UserAdmin)
admin.site.register(usr_mdl.Invitation)