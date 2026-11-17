
from django.urls import path

from . import views
urlpatterns=[

    path('projects/',views.ProjectListCreateView.as_view()),

    path('projects/<str:uuid>/',views.ProjectRetrieveUpdateView.as_view()),

    path('assignedprojects/',views.AssignedProjectListCreateView.as_view()),

    path('assignedprojects/<str:uuid>/',views.AssignedProjectRetrieveUpdateDestroyview.as_view()),

    path('tasks/',views.TaskListCreateView.as_view()),

    path('tasks/<str:uuid>/',views.TasktRetrieveUpdateDestroyview.as_view()),

    path('create-tasks-ai/<str:uuid>/',views.TaskCreateWithAI.as_view())

    

]