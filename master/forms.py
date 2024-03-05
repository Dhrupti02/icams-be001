from django import forms
from . import models



class CourseForm(forms.ModelForm):
    class Meta:
        model = models.Course
        fields = '__all__'