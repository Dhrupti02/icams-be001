from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    contact_number = models.CharField(max_length=15)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    company_name = models.CharField(max_length=255)
    is_approved = models.BooleanField(default=False)
    manager = models.ForeignKey(User, related_name='manager_profiles', on_delete=models.SET_NULL, null=True, blank=True)
    hr = models.ForeignKey(User, related_name='hr_profiles', on_delete=models.SET_NULL, null=True, blank=True)
    ceo = models.ForeignKey(User, related_name='ceo_profiles', on_delete=models.SET_NULL, null=True, blank=True)
    ROLE_CHOICES = [
        ('employee', 'Employee'),
        ('manager', 'Manager'),
        ('hr', 'HR'),
        ('ceo', 'CEO'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username}'s profile"

class Course(models.Model):
    course_name = models.CharField(max_length=100)
    time_duration = models.CharField(max_length=50)
    description = models.TextField()
    created_date = models.DateField(auto_now_add=True)
    last_update_date = models.DateField(auto_now=True)
    instructor = models.CharField(max_length=100)
    images = models.ImageField(upload_to='images/')  
    
class EnrolledUsers(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_user = models.ForeignKey(User, on_delete=models.CASCADE)
    starting_date = models.DateField()

class Document(models.Model):
    document_name = models.CharField(max_length=255)
    can_upload = models.BooleanField(default=False)
    can_download = models.BooleanField(default=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    history  = models.TextField()

    def __str__(self):
        return self.document_name

class DocumentFiles(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='files')
    document_file = models.FileField(upload_to='uploads/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.document.document_name + ' - ' + str(self.id)

class Task(models.Model):
    task_name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    assigned_user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    rating = models.IntegerField(default=0)
    deadline_date = models.DateField()
    complete = models.BooleanField(default=False)
    remarks_by_admin = models.TextField(blank=True, null=True)
    remarks_by_executive = models.TextField(blank=True, null=True)
    remarks_by_hr = models.TextField(blank=True, null=True)
    remarks_by_manager = models.TextField(blank=True, null=True)