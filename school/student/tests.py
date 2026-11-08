from django.test import TestCase
from django.urls import reverse

from .models import Student


class StudentCrudTests(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            name='Ada Lovelace',
            age=22,
            email='ada@example.com',
        )

    def test_dashboard_and_list_pages_load(self):
        self.assertEqual(self.client.get(reverse('dashboard')).status_code, 200)
        self.assertEqual(self.client.get(reverse('student_list')).status_code, 200)

    def test_add_student(self):
        response = self.client.post(reverse('addstudent'), {
            'name': 'Grace Hopper',
            'age': 30,
            'email': 'grace@example.com',
        })
        self.assertRedirects(response, reverse('student_list'))
        self.assertTrue(Student.objects.filter(email='grace@example.com').exists())

    def test_edit_student(self):
        response = self.client.post(reverse('edit_student', args=[self.student.pk]), {
            'name': 'Ada Byron',
            'age': 23,
            'email': 'ada@example.com',
        })
        self.assertRedirects(response, reverse('student_list'))
        self.student.refresh_from_db()
        self.assertEqual(self.student.name, 'Ada Byron')

    def test_delete_student(self):
        response = self.client.post(reverse('delete_student', args=[self.student.pk]))
        self.assertRedirects(response, reverse('student_list'))
        self.assertFalse(Student.objects.filter(pk=self.student.pk).exists())

    def test_student_search(self):
        response = self.client.get(reverse('student_list'), {'search': 'Ada'})
        self.assertContains(response, 'Ada Lovelace')
