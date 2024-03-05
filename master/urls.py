from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('register', views.user_registration),
    path('login', views.user_login),
    path('dashboard', views.dashboard),
    path('show_course', views.show_course),
    path('show_course_detail/<int:pk>', views.show_course_detail),
    path('add_task_data/<int:pk>', views.add_task_data),
    
    # path('course/create', views.course_create, name='course_create'),
    # path('course/<int:pk>/update', views.course_update, name='course_update'),
    # path('course/<int:pk>/delete', views.course_delete, name='course_delete'),
    # path('course/list', views.course_list, name='course_list'),
    # path('course/<int:pk>', views.course_detail, name='course_detail'),
    # path('upload_document/<int:pk>', views.upload_document, name='upload_document'),
    # path('download_file/<int:pk>', views.download_file, name='download_file'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
