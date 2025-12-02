from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),  # ✅ use correct function
    path('services/', views.available_services, name='available_services'),
    path('offer/', views.offer_service, name='offer_service'),
    path('request-list/', views.request_service_list, name='request_service_list'),
path('request/<int:offer_id>/', views.request_service, name='request_service'),
# mainapp/urls.py
path('request/delete/<int:request_id>/', views.delete_request, name='delete_request'),
path('respond-request/<int:request_id>/', views.respond_request, name='respond_request'),
path('profile/', views.user_profile_view, name='user_profile'),
path('profile/edit/', views.edit_profile_view, name='edit_profile'),
# urls.py

path('request/<int:request_id>/detail/', views.view_request_detail, name='view_request_detail'),
path('send-message/<int:receiver_id>/', views.send_message, name='send_message'),
path('inbox/', views.inbox, name='inbox'),



]

handler404 = 'mainapp.views.page_not_found'
handler500 = 'mainapp.views.server_error'
