from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import custom_logout  # Add this line to import custom_logout

urlpatterns = [  # Add this line if it is missing
    path('', views.login_view, name='login'),
    path('trace_results/', views.trace_results, name='trace_results'),
    path('agent_overview/', views.agent_overview, name='agent_overview'),
    path('client_information/', views.client_information, name='client_information'),
    path('client_details/', views.client_details, name='client_details'),
    path('client_list/', views.client_list, name='client_list'),
    path('arrangements/', views.arrangements, name='arrangements'),
    path('create_call/', views.create_call, name='create_call'),
    path('get_client_details/', views.get_client_details, name='get_client_details'),
    path('get_phone_numbers/', views.get_phone_numbers, name='get_phone_numbers'),
    path('viewcalled/<str:id_number>/', views.viewcalled, name='viewcalled'),
    path('call_list/', views.call_list, name='call_list'),
    path('client_list_for_client/<str:id_number>/', views.client_list_for_client, name='client_list_for_client'),
    path('arrangements_for_client/<str:id_number>/', views.arrangements_for_client, name='arrangements_for_client'),
    path('create_call_for_client/<str:id_number>/', views.create_call_for_client, name='create_call_for_client'),
    path('call_list_for_client/<str:id_number>/', views.call_list_for_client, name='call_list_for_client'),
    path('recon/', views.recon_view, name='recon'),
    path('arrangement_graph/', views.arrangement_graph, name='arrangement_graph'),
    path('logout/', custom_logout, name='logout'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('password_reset_sent/', views.password_reset_sent, name='password_reset_sent'),
    path('password_reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('dashboard/', views.dashboard, name='dashboard'),  # Add this line
     path('agent_overview/bulk-sms/', views.bulk_sms, name='bulk_sms'),
    path('agent_overview/bulk-email/', views.bulk_email, name='bulk_email'),
]