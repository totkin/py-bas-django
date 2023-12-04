from django.contrib import admin

from .models import (Title,
                     Department,
                     Subscription,
                     Manager)


# admin.site.register(Title)
# admin.site.register(Department)
# admin.site.register(Subscription)
# admin.site.register(Manager)


@admin.register(Title)
class Title(admin.ModelAdmin):
    list_display = ('short_name', 'name')


@admin.register(Department)
class Department(admin.ModelAdmin):
    pass


@admin.register(Subscription)
class Subscription(admin.ModelAdmin):
    pass


@admin.register(Manager)
class Manager(admin.ModelAdmin):
    list_display = ('full_name', 'title', 'display_subcriptions')
    fieldsets = (('ФИО', {'fields': ("last_name", "first_name", "middle_name")}),
                 ('Оргструктрура', {'fields': ("title", "department", "system_name")}),
                 ('Подписки', {'fields': ("email", "subscription")}),
                 ('Дополнительная информация', {'fields': ("gender", "birthday")})
                 )
