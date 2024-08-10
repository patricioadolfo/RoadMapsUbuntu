#from django.conf.urls import url
from django.urls import path, include
from . import views



urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.index, name='index'),
    path('route/<int:pk>/edit/', views.update_status, name='route-edit'),
    path('route/', views.RoutesListView.as_view(), name='routes'),
    path('route/<int:pk>', views.RouteDetailView.as_view(), name='route-detail'),
    path('new-route/', views.route_create, name='route-create'),
    path('route/<int:pk>/delete/', views.RouteDelete.as_view(), name='route-delete'),
    path('nodes-destin/', views.NodeDestinationListView.as_view(), name='nodes-destin'),
    path('nodes/destination/create/', views.destination_create, name='destin-create'),
    path('nodes-origin/', views.NodeOriginListView.as_view(), name='nodes-origin'),
    path('nodes/origin/create/', views.origin_create, name='origin-create'),
]


