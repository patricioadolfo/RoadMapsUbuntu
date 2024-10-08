from django.contrib import admin

from .models import Route, RouteInstance, NodeDestination, NodeOrigin, Perfil, States, PrinterNode, PrintJob


admin.site.register(NodeDestination)
admin.site.register(NodeOrigin)


@admin.register(PrinterNode)
class PrinterNodeAdmin(admin.ModelAdmin):

    list_display= ('id', 'name', 'node', 'psw', 'state')

@admin.register(PrintJob)
class PrintJobAdmin(admin.ModelAdmin):

    list_display= ('id', 'job', 'printer', 'state')

class RouteInstanceInline(admin.TabularInline):
    model = RouteInstance

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    
    list_display = ('id', 'user', 'origin', 'destination', 'preparation_date',)
    
    inlines = [RouteInstanceInline]
    
@admin.register(States)
class StatesAdmin(admin.ModelAdmin):

    list_display= ('id', 'state', 'descriptions')

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):

    list_display= ('id', 'user', 'nodo', 'dealer')
    