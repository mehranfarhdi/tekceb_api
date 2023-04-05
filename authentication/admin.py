from django.contrib import admin

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'auth_provider', 'created_at']


class CounselingAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'done']


admin.site.register(User, UserAdmin)
admin.site.register(Counseling, CounselingAdmin)
