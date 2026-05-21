from .decorators import role_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Patient, Test

# 🔐 AUTH
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# 🔥 DRF
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PatientSerializer, TestSerializer


# =====================================================
# 🔐 LOGIN
# =====================================================
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            # ✅ ROLE BASED REDIRECT
            if user.groups.filter(name='Lab_Technician').exists():
                return redirect('tests')
            elif user.groups.filter(name='Receptionist').exists():
                return redirect('patients')
            elif user.groups.filter(name='Patient').exists():
                return redirect('reports')
            else:
                return redirect('dashboard')

        messages.error(request, "Invalid username or password")

    return render(request, 'login.html')


# =====================================================
# 🔓 LOGOUT
# =====================================================
def logout_view(request):
    logout(request)
    return redirect('login')


# =====================================================
# 🏠 DASHBOARD
# =====================================================
@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {
        'total_patients': Patient.objects.count(),
        'total_tests': Test.objects.count()
    })


# =====================================================
# 🏠 HOME
# =====================================================
@login_required
def home(request):
    return render(request, 'index.html')


# =====================================================
# 👨‍⚕️ PATIENTS
# =====================================================
@login_required
def patients_page(request):
    query = request.GET.get('q', '')
    patients = Patient.objects.all().order_by('-id')

    if query:
        patients = patients.filter(name__icontains=query)

    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        disease = request.POST.get('disease')

        if name and age and disease:
            Patient.objects.create(
                name=name,
                age=age,
                disease=disease
            )

        return redirect('patients')

    return render(request, 'patients.html', {
        'patients': patients,
        'query': query
    })


# =====================================================
# ✏️ EDIT PATIENT
# =====================================================
@login_required
def edit_patient(request, id):
    patient = get_object_or_404(Patient, id=id)

    if request.method == 'POST':
        patient.name = request.POST.get('name')
        patient.age = request.POST.get('age')
        patient.disease = request.POST.get('disease')
        patient.save()
        return redirect('patients')

    return render(request, 'edit_patient.html', {'patient': patient})


# =====================================================
# ❌ DELETE PATIENT
# =====================================================
@login_required
def delete_patient(request, id):
    patient = get_object_or_404(Patient, id=id)
    patient.delete()
    return redirect('patients')


# =====================================================
# 🧪 TESTS
# =====================================================
@login_required
def tests_page(request):
    patients = Patient.objects.all()

    if request.method == 'POST':
        patient_id = request.POST.get('patient')
        test_name = request.POST.get('test_name')

        if patient_id and test_name:
            Test.objects.create(
                patient_id=patient_id,
                test_name=test_name,
                status='Pending'
            )

        return redirect('tests')

    tests = Test.objects.all().order_by('-id')

    return render(request, 'tests.html', {
        'tests': tests,
        'patients': patients
    })


# =====================================================
# 🧪 UPDATE RESULT
# =====================================================
@login_required
def update_result(request, id):
    test = get_object_or_404(Test, id=id)

    if request.method == 'POST':
        result = request.POST.get('result')

        if result:
            test.result = result
            test.status = 'Completed'
            test.save()

        return redirect('tests')

    return render(request, 'update_result.html', {
        'test': test
    })


# =====================================================
# 📊 REPORTS
# =====================================================
@login_required
def reports_page(request):
    tests = Test.objects.filter(status='Completed').order_by('-id')

    return render(request, 'reports.html', {
        'tests': tests
    })


# =====================================================
# 📞 CONTACT
# =====================================================
@login_required
def contact_page(request):
    if request.method == 'POST':
        return render(request, 'contact.html', {'success': True})

    return render(request, 'contact.html')


# =====================================================
# 🔥 API - PATIENTS (GET + POST)
# =====================================================
@api_view(['GET', 'POST'])
def api_patients(request):
    if request.method == 'GET':
        patients = Patient.objects.all().order_by('-id')
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


# =====================================================
# 🔥 API - TESTS (GET + POST)
# =====================================================
@api_view(['GET', 'POST'])
def api_tests(request):
    if request.method == 'GET':
        tests = Test.objects.all().order_by('-id')
        serializer = TestSerializer(tests, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


# =====================================================
# 🔥 API - TEST DETAIL
# =====================================================
@api_view(['GET'])
def api_test_detail(request, id):
    test = get_object_or_404(Test, id=id)
    serializer = TestSerializer(test)
    return Response(serializer.data)