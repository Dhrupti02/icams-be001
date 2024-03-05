from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken
from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse

# local imports 
from . import serializers, models

# from .models import Course
from .forms import CourseForm 

# Create your views here.

def home(request):
    return HttpResponse("Hello")

@api_view(['POST']) 
def user_login(request):    
    username = request.data.get('username')  # Assuming we're using username for login
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)  # Use username as username
    if user:
        try:
            user_profile = models.UserProfile.objects.get(user=user)
            if not user_profile.is_approved:
                return Response({'message': 'User is not approved'}, status=status.HTTP_401_UNAUTHORIZED)
        except models.UserProfile.DoesNotExist:
            # Handle case where user does not have an associated UserProfile
            return Response({'message': 'User profile not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        token = AccessToken.for_user(user)
        return Response({'message': 'Login Successful', 'token': str(token)}, status=status.HTTP_200_OK)
        
    else:
        return Response({'message': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def user_registration(request):
    if request.method == 'POST':
        serializer = serializers.UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            user_profile = serializer.save()
            return Response({'message': 'User registered successfully, pending approval.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"message":"BAD METHOD REQUEST ERROR"}, status=status.HTTP_400_BAD_REQUEST)
 # Assuming you have created a form for Course model


#### Dashboard

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def dashboard(request):
    enrolled_user_info = models.EnrolledUsers.objects.filter(enrolled_user=request.user)[:5]

    course_ids = enrolled_user_info.values_list('course', flat=True)

    courses_of_user = models.Course.objects.filter(pk__in=course_ids)
    tasks_of_user = models.Task.objects.filter(course__in=courses_of_user, assigned_user=request.user)

    course = []
    tasks = []
    course_task = {}

    for obj in courses_of_user:
        course_data = {}
        course_data['image'] = str(obj.images)
        course_data['title'] = obj.course_name
        course_data['time_duration'] = obj.time_duration
        # course_task['course'] = course_data
        course.append(course_data) 


    for obj in tasks_of_user:
        data = {}
        data['task_name'] = obj.task_name
        data['course'] = obj.course.course_name
        data['deadline'] = obj.deadline_date
        # course_task['task'] = data
        tasks.append(data)

    course_task = {"course":course, "tasks":tasks} 

    return Response(course_task)



#### My courses

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def show_course(request):
    enrolled_user_info = models.EnrolledUsers.objects.filter(enrolled_user=request.user)

    course_ids = enrolled_user_info.values_list('course', flat=True)
    courses_of_user = models.Course.objects.filter(pk__in=course_ids)
    # tasks_of_user = models.Task.objects.filter(course__in=courses_of_user, assigned_user=request.user)
    
    course_datas = []

    for obj in courses_of_user:
        course_data = {}
        id = obj.pk
        print(id)
        course_data['image'] = str(obj.images)
        course_data['title'] = obj.course_name
        course_data['time_duration'] = obj.time_duration
        course_data['description'] = obj.description
        

        c = 0
        task = models.Task.objects.filter(course=id, assigned_user=request.user)
        total_tasks = task.count()
        for i in task:
            if i.complete == True:
                c += 1
            else:
                c = 0   
        course_data['total_tasks'] = total_tasks
        course_data['tasks_completed'] = c
        course_datas.append(course_data) 

    return Response(course_datas)


#### Course detail

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def show_course_detail(request,pk):
    ### of a particular course
    
    courses_of_user = models.Course.objects.filter(id=pk)
    tasks_of_user = models.Task.objects.filter(course__in=courses_of_user)
    
    course_data = {}

    for obj in courses_of_user:
        id = obj.pk
        course_data['image'] = str(obj.images)
        course_data['title'] = obj.course_name
        course_data['time_duration'] = obj.time_duration
        course_data['description'] = obj.description
        course_data['created_date'] = obj.created_date
        course_data['last_update_date'] = obj.last_update_date
        course_data['instructor'] = obj.instructor
        ### add task completed
        for obj1 in tasks_of_user:
            if obj1.course.id == id:
                course_data['task_name'] = obj1.task_name
                course_data['task_completed'] = obj1.complete
            else:
                Response("Records not found")
                
    return JsonResponse(course_data)

#### Task: add: user, task, answer, rating
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_task_data(request,pk):
    obj = models.Course.objects.get(id=pk)
    course = obj.id

    users = models.UserProfile.objects.get(user=request.user)
    userss = users.id

    serializer = serializers.TaskSerializer(data={'task_name': request.data['task_name'], 'course':course, 'assigned_user':userss,
                                                        'question':request.data['question'], 'answer':request.data['answer'],'rating':request.data['rating'],
                                                        'deadline_date':request.data['deadline_date'], 'complete':request.data['complete'], 'remarks_by_admin':request.data['remarks_by_admin'], 
                                                        'remarks_by_executive':request.data['remarks_by_executive'], 'remarks_by_hr':request.data['remarks_by_hr'], 'remarks_by_manager':request.data['remarks_by_manager']})

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#### Courses

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def course_create(request):
#     if request.method == 'POST':
#         serializer = serializers.CourseSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def course_update(request, pk):
#     course = get_object_or_404(models.Course, pk=pk)
#     serializer = serializers.CourseSerializer(course, data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def course_delete(request, pk):
#     course = get_object_or_404(models.Course, pk=pk)
#     if request.method == 'POST':
#         course.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def course_list(request):
#     courses = models.Course.objects.all()
#     serializer = models.CourseSerializer(courses, many=True)
#     return Response(serializer.data)

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def course_detail(request, pk):
#     course = get_object_or_404(models.Course, pk=pk)
#     serializer = serializers.CourseSerializer(course)
#     return Response(serializer.data)



# #### Documents

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def upload_document(request,pk):
#     if request.method == 'POST':
        
#         obj = models.Course.objects.get(id=pk)
#         course = obj.id

#         users = models.UserProfile.objects.get(user=request.user)
#         userss = users.id

#         serializer = serializers.DocumentSerializer(data={'document_name': request.data['document_name'], 'can_upload':request.data['can_upload'], 
#                                                           'can_download':request.data['can_download'], 'course':course,'history':request.data['history']})

#         if serializer.is_valid():
#             serializer.save()
            
#             obj1 = models.Document.objects.first()
#             doc_name = obj1.id
#             serializer1 = serializers.DocumentFilesSerializer(data={'document':doc_name,'document_file': request.data['document_file'],
#                                                                     'uploaded_by':userss})
            
#             if serializer1.is_valid():
#                 serializer1.save()
#                 return Response({"message": "Data saved successfully"}, status=201)
#             errors = {}
#             errors.update(serializer1.errors)
#             return Response({"message": errors}, status=201)
#         # else:
#         #     errors = {}
#         #     errors.update(serializer.errors)
#         #     return Response(errors, status=400)
        
#         else:
#             errors = {}
#             errors.update(serializer.errors)
#             return Response(errors, status=400)


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def download_file(request, pk):
#     doc_files = models.DocumentFiles.objects.get(id=pk)
#     document_data = doc_files.document
    
#     # Get the file path
#     file_path = doc_files.document_file.path
#     # print(file_path)
#     if document_data.can_download:
#         try:
#             with open(file_path, 'rb') as f:
#                 file_content = f.read()
#             response = HttpResponse(file_content)
            
#             # Set the content type header
#             response['Content-Type'] = 'application/json'
            
#             # Set the content disposition header to force download
#             response['Content-Disposition'] = f'attachment; filename="{doc_files.document_file.name}"'
            
#             return response
#         except FileNotFoundError:
#             return HttpResponse("File not found", status=404)

    
#     return HttpResponse("successful")