from django.contrib import admin
from django.contrib.auth.models import Group

admin.site.unregister(Group)

from app.models import AddPublication, Admin, Group, Settings


@admin.register(Admin)
class Admin(admin.ModelAdmin):
    fields = ("name", "tgid", "password", "user_permissions")


admin.site.register(Settings)

admin.site.register(Group)

admin.site.register(AddPublication)
