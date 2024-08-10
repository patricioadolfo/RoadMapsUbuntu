from django.contrib import admin

from .models import Route, RouteInstance, NodeDestination, NodeOrigin, Perfil

admin.site.register(NodeDestination)
admin.site.register(NodeOrigin)
admin.site.register(Perfil)

class RouteInstanceInline(admin.TabularInline):
    model = RouteInstance

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    
    list_display = ('user', 'origin', 'destination', 'preparation_date',)
    
    inlines = [RouteInstanceInline]
    


    