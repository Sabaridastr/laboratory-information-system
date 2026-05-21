from django.urls import path
from . import views

urlpatterns = [

    # =====================================================
    # 🔐 AUTHENTICATION
    # =====================================================
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # ✅ Django default login fix
    path('accounts/login/', views.login_view, name='accounts_login'),

    # =====================================================
    # 🏠 DASHBOARD
    # =====================================================
    path('', views.dashboard, name='dashboard'),

    # =====================================================
    # 🏠 HOME
    # =====================================================
    path('home/', views.home, name='home'),

    # =====================================================
    # 👨‍⚕️ PATIENT MODULE
    # =====================================================
    path('patients/', views.patients_page, name='patients'),
    path('patients/edit/<int:id>/', views.edit_patient, name='edit_patient'),
    path('patients/delete/<int:id>/', views.delete_patient, name='delete_patient'),

    # =====================================================
    # 🧪 TEST MODULE
    # =====================================================
    path('tests/', views.tests_page, name='tests'),
    path('tests/update/<int:id>/', views.update_result, name='update_result'),

    # =====================================================
    # 📊 REPORTS
    # =====================================================
    path('reports/', views.reports_page, name='reports'),

    # =====================================================
    # 📞 CONTACT
    # =====================================================
    path('contact/', views.contact_page, name='contact'),

    # =====================================================
    # 🔥 API (FINAL CLEAN)
    # =====================================================
    path('api/patients/', views.api_patients, name='api_patients'),
    path('api/tests/', views.api_tests, name='api_tests'),
    path('api/tests/<int:id>/', views.api_test_detail, name='api_test_detail'),
]