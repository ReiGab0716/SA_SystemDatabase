from django.contrib import admin
from django.urls import path
from clinic import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),

    # -----------------------
    # AUTHENTICATION
    # -----------------------
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('login-redirect/', views.login_redirect, name='login_redirect'),

    # -----------------------
    # PATIENT
    # -----------------------
    path('dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('book-appointment/', views.book_appointment, name='book_appointment'),
    path('set-appointment/', views.book_appointment, name='set_appointment'),  # alias (optional)
    path('my-sessions/', views.patient_sessions, name='patient_sessions'),
    path('profile/', views.patient_profile, name='patient_profile'),
    path('check-availability/', views.check_availability, name='check_availability'),
    path('sessions/cancel/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),

    # -----------------------
    # DOCTOR
    # -----------------------
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('doctor/manage-users/', views.doctor_manage_users, name='doctor_manage_users'),
    path('doctor/set-appointment/', views.doctor_set_appointment, name='doctor_set_appointment'),
    path('doctor/manage-sessions/', views.doctor_manage_sessions, name='doctor_manage_sessions'),
    path('doctor/sales/', views.doctor_sales, name='doctor_sales'),
    path('schedule-appointment/', views.create_appointment, name='schedule_appointment'),

    
    path(
        'doctor/appointments/confirm/<int:appointment_id>/',
        views.doctor_confirm_appointment,
        name='doctor_confirm_appointment'
    ),

    path(
    'doctor/appointments/cancel/<int:appointment_id>/',
    views.doctor_cancel_appointment,
    name='doctor_cancel_appointment'
),

    path(
    'doctor/appointments/complete/<int:appointment_id>/',
    views.doctor_complete_appointment,
    name='doctor_complete_appointment'
),
    
    path('doctor/change-role/<int:user_id>/', views.change_user_role, name='change_user_role'),
        
        
    # -----------------------
    # SECRETARY / STAFF
    # -----------------------

    path('secretary/dashboard/', views.secretary_dashboard, name='secretary_dashboard'),
    path('secretary/set-appointment/', views.secretary_set_appointment, name='secretary_set_appointment'),
    path('secretary/manage-sessions/', views.secretary_manage_sessions, name='secretary_manage_sessions'),
    
    path(
    "secretary/appointment/<int:pk>/cancel/", views.secretary_cancel_appointment, name="secretary_cancel_appointment"),

    path(
    "secretary/appointment/<int:pk>/complete/", views.secretary_complete_appointment, name="secretary_complete_appointment"),
    
    path(
        "secretary/appointment/<int:pk>/confirm/", 
        views.secretary_confirm_appointment, 
        name="secretary_confirm_appointment"
    ),

    # Doctor-specific API endpoints
    path('api/patient/<int:patient_id>/', views.get_patient_details, name='get_patient_details'),
    path('api/doctor-notes/<int:appointment_id>/get/', views.get_doctor_notes, name='get_doctor_notes'),
    path('api/doctor-notes/<int:appointment_id>/save/', views.save_doctor_notes, name='save_doctor_notes'),

    # Patients Management (Doctor & Secretary)
    path('patients/', views.all_patients, name='all_patients'),
    path('patient/<int:patient_id>/', views.patient_detail, name='patient_detail'),

    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    
    # Appointment Scheduling APIs
    path('api/search-patients/', views.search_patients, name='search_patients'),
    path('api/quick-register-patient/', views.quick_register_patient, name='quick_register_patient'),
    path('api/service/<int:service_id>/', views.get_service_details, name='service_details'),
    path('api/notifications/poll/', views.notification_poll, name='notification_poll'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
