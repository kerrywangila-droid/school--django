from django.contrib import messages
from django.db.models import Avg
from django.shortcuts import get_object_or_404, redirect, render

from .forms import StudentForm
from .models import Student


def dashboard(request):
    students = Student.objects.order_by('-enrollment_date')[:8]
    average_age = Student.objects.aggregate(average_age=Avg('age'))['average_age']
    return render(request, 'dashboard.html', {
        'students': students,
        'student_count': Student.objects.count(),
        'average_age': round(average_age, 1) if average_age else 0,
        'recent_count': students.count(),
    })


def theme_generator(request):
    return redirect('/static/adminlte/generate/theme.html')


def student_list(request):
    search = request.GET.get('search', '').strip()
    students = Student.objects.all()
    if search:
        students = students.filter(name__icontains=search) | students.filter(email__icontains=search)
    return render(request, 'student_list.html', {
        'students': students.order_by('name'),
        'search': search,
    })


def addstudent(request):
    form = StudentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Student added successfully.')
        return redirect('student_list')
    return render(request, 'addstudent.html', {'form': form})


def edit_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    form = StudentForm(request.POST or None, instance=student)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Student updated successfully.')
        return redirect('student_list')
    return render(request, 'edit_student.html', {'form': form, 'student': student})


def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student deleted successfully.')
        return redirect('student_list')
    return render(request, 'delete_student.html', {'student': student})
