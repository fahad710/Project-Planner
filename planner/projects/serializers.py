from rest_framework import serializers

from .models import Project,AssignedProjects,Task

from authentication.serializers import ProfileSerializers

from authentication.models import Profile



class ProjectSerializer(serializers.ModelSerializer):

    class Meta:

        model= Project

        fields='__all__'

        read_only_fields=['active_status']



class ProjectField(serializers.PrimaryKeyRelatedField):

    def get_attribute(self, instance):

        return getattr(instance,self.source_attrs[0]) 

    def to_representation(self, value):

        return ProjectSerializer(value).data  
    
class ProfileField(serializers.PrimaryKeyRelatedField):

    def get_attribute(self, instance):

        return getattr(instance,self.source_attrs[0]) 

    def to_representation(self, value):

        return ProfileSerializers(value).data  

class AssignedProjectSerializer(serializers.ModelSerializer):

    project = ProjectField(
        queryset=Project.objects.all()
    )

    coordinator = ProfileField(
        queryset=Profile.objects.filter(
            role='Project Coordinator'
        )
    )

    developer = ProfileField(
        queryset=Profile.objects.filter(
            role='Developer'
        ),
        many=True
    )

    class Meta:
        model = AssignedProjects

        fields = '__all__'

        read_only_fields = ['active_status']


class AssignedProjectField(serializers.PrimaryKeyRelatedField):

    def get_attribute(self, instance):

        return getattr(instance,self.source_attrs[0]) 

    def to_representation(self, value):

        return AssignedProjectSerializer(value).data  


class TaskSerializer(serializers.ModelSerializer):

    assigned_project= AssignedProjectField(
    queryset=AssignedProjects.objects.all()
        .select_related('project', 'coordinator')
        .prefetch_related('developer'))

    assigned_to=ProfileField(queryset=Profile.objects.filter(role='developer'))

    class Meta :

        model= Task

        fields = '__all__'

        read_only_fields=['active_status']