from django.shortcuts import render

from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView

from .serializers import ProjectSerializer,AssignedProjectSerializer,TaskSerializer

from .models import Project,AssignedProjects,Task

from authentication.models import Profile

from rest_framework.views import APIView

from rest_framework.response import Response

from planner.utils import generate_tasks

from django.db import transaction

from planner.paginations import CustomPagination
# Create your views here.

class ProjectListCreateView(ListCreateAPIView):

    pagination_class=CustomPagination

    queryset = Project.objects.filter(active_status=True)

    serializer_class = ProjectSerializer

    


class ProjectRetrieveUpdateView(RetrieveUpdateDestroyAPIView):

    lookup_field='uuid'

    queryset=Project.objects.filter(active_status=True)

    serializer_class=ProjectSerializer


    def perform_destroy(self, instance):

        instance.active_status=False

        instance.save()



class AssignedProjectListCreateView(ListCreateAPIView):

    pagination_class=CustomPagination

    queryset = AssignedProjects.objects.all().select_related('project','coordinator').prefetch_related('developer')

    serializer_class = AssignedProjectSerializer


class AssignedProjectRetrieveUpdateDestroyview(RetrieveUpdateDestroyAPIView):

    queryset = AssignedProjects.objects.filter(active_status=True).select_related('project','coordinator').prefetch_related('developer')
   
    serializer_class = AssignedProjectSerializer

    lookup_field = 'uuid'

    def perform_destroy(self, instance):
    
        instance.active_status=False
    
        instance.save()

class TaskListCreateView(ListCreateAPIView):

    pagination_class=CustomPagination

    def get_queryset(self):

        uuid=self.request.query_params.get('project')

        if uuid:
            # Task.objects.filter(assigned_project__uuid=uuid)

            assigned_project=AssignedProjects.objects.get(uuid=uuid)

            tasks= assigned_project.task_set.filter(active_status=True).select_related('assigned_project','assigned_to')

            return tasks

        return Task.objects.none()

    serializer_class=TaskSerializer



class TasktRetrieveUpdateDestroyview(RetrieveUpdateDestroyAPIView):
    
    lookup_field = 'uuid'

    queryset = Task.objects.filter(active_status=True).select_related('assigned_project','assigned_to')
   
    serializer_class = TaskSerializer   


class TaskCreateWithAI(APIView):

    def post(self,request,*args,**kwargs):

        uuid=kwargs.get('uuid')

        try:

            assigned_project=AssignedProjects.objects.get(project__uuid=uuid)

            result = generate_tasks(assigned_project)

            tasks=[Task(title=task.title,
                        description=task.description,
                        assigned_project=assigned_project,
                        assigned_to_id=task.developer_id,
                        priority=task.priority) for task in result.tasks]     

            with transaction.atomic():

                Task.objects.bulk_create(tasks)

                data={'msg':'Tasks assigned succesfully'}

                return Response(data,status=200)
        except Exception as e:

            print(e)

            data={'msg':'Failed to create tasks'}

            return Response(data,status=400)



        

        
        print(result.tasks)

        return Response(status=200)