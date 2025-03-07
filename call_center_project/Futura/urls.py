from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('trace_results/', views.trace_results, name='trace_results'),
    path('agent_overview/', views.agent_overview, name='agent_overview'), # Add this line
    path('client_information/', views.client_information, name='client_information'), # Add this line
    path('client_details/', views.client_details, name='client_details'), # Add this line
    path('client_list/', views.client_list, name='client_list'), # Add this line
    path('arrangements/', views.arrangements, name='arrangements'), # Add this line
    path('create_call/', views.create_call, name='create_call'),
    path('create_call/', views.create_call, name='create_call'),
    path('get_client_details/', views.get_client_details, name='get_client_details'),
    path('get_phone_numbers/', views.get_phone_numbers, name='get_phone_numbers'),
    path('viewcalled/<str:id_number>/', views.viewcalled, name='viewcalled'),
    path('call_list/', views.call_list, name='call_list'),
    path('client_list_for_client/<str:id_number>/', views.client_list_for_client, name='client_list_for_client'),
    path('arrangements_for_client/<str:id_number>/', views.arrangements_for_client, name='arrangements_for_client'),
    path('create_call_for_client/<str:id_number>/', views.create_call_for_client, name='create_call_for_client'),
    path('call_list_for_client/<str:id_number>/', views.call_list_for_client, name='call_list_for_client'),
    path('recon/', views.recon_view, name='recon'),  # Corrected name here
    path('arrangement_graph/', views.arrangement_graph, name='arrangement_graph'),
]