from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # Core Pages
    path('', views.home_view, name='home'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Services
    path('services/', views.available_services, name='available_services'),
    path('offer/', views.offer_service, name='offer_service'),
    path('request-list/', views.request_service_list, name='request_service_list'),
    path('request/<int:offer_id>/', views.request_service, name='request_service'),
    path('request/delete/<int:request_id>/', views.delete_request, name='delete_request'),
    path('respond-request/<int:request_id>/', views.respond_request, name='respond_request'),
    path('request/<int:request_id>/detail/', views.view_request_detail, name='view_request_detail'),
    
    # Service Management
    path('service/<int:service_id>/detail/', views.service_detail_view, name='service_detail'),
    path('my-services/', views.my_services_view, name='my_services'),
    path('service/<int:service_id>/edit/', views.edit_service_view, name='edit_service'),
    path('service/<int:service_id>/delete/', views.delete_service_view, name='delete_service'),
    
    # Categories
    path('categories/', views.categories_view, name='categories'),
    path('category/<int:category_id>/', views.category_detail_view, name='category_detail'),
    
    # User Profile
    path('profile/', views.user_profile_view, name='user_profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('profile/user/<int:user_id>/', views.public_user_profile_view, name='public_user_profile'),
    
    # Transactions & History
    path('transactions/', views.transaction_history_view, name='transaction_history'),
    path('statistics/', views.statistics_view, name='statistics'),
    
    # User Directory
    path('users/', views.user_directory_view, name='user_directory'),
    
    # Messaging
    path('send-message/<int:receiver_id>/', views.send_message, name='send_message'),
    path('inbox/', views.inbox, name='inbox'),
    
    # Notifications
    path('notifications/', views.notifications_view, name='notifications'),
    path('notification/<int:notification_id>/read/', views.mark_notification_read, name='mark_notification_read'),
    
    # Reviews
    path('review/add/<int:request_id>/', views.add_review_view, name='add_review'),
    
    # Help
    path('help/', views.help_faq_view, name='help_faq'),
]

handler404 = 'mainapp.views.page_not_found'
handler500 = 'mainapp.views.server_error'
