from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from influencedapi.models import Job, User
from django.shortcuts import get_object_or_404

class JobView(ViewSet):
    def retrieve(self, request, pk):
        """Handle GET requests for a single job"""
        try:
            user = Job.objects.get(pk=pk)
            serializer =JobSerializer(user)
            return Response(serializer.data)
        except Job.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND) 
          
    def list(self, request):
        """Handle GET requests for all jobs"""
        jobs = Job.objects.all()
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)
      
    def create(self, request):
        """Handle POST requests to create a new job"""
        try:
            # Validate foreign key references
            client = get_object_or_404(User, id=request.data["client_id"])
            accepted_by = get_object_or_404(User, id=request.data["acceptedBy"])
            
            # Create a new Job object
            job = Job.objects.create(
                description=request.data["description"],
                client_id=client,
                accepted=request.data["accepted"],
                pay=request.data["pay"],
                acceptedBy=accepted_by,
                complete=request.data["complete"]
            )
            
            # Serialize the created job and return the response
            serializer = JobSerializer(job)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except KeyError as e:
            return Response({'message': f'Missing required field: {e}'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        """Handle PUT/PATCH requests to update a job"""
        job = get_object_or_404(Job, pk=pk)

        # Validate foreign key references
        client_id = request.data.get("client_id")
        accepted_by_id = request.data.get("acceptedBy")
        if client_id:
            client = get_object_or_404(User, id=client_id)
        else:
            client = job.client_id
        if accepted_by_id:
            accepted_by = get_object_or_404(User, id=accepted_by_id)
        else:
            accepted_by = job.acceptedBy

        # Update job instance
        job.description = request.data.get("description", job.description)
        job.client_id = client
        job.accepted = request.data.get("accepted", job.accepted)
        job.pay = request.data.get("pay", job.pay)
        job.acceptedBy = accepted_by
        job.complete = request.data.get("complete", job.complete)
        
        job.save()

        serializer = JobSerializer(job)
        return Response(serializer.data, status=status.HTTP_200_OK)      
    
    def destroy(self, request, pk=None):
        """Handle DELETE requests to delete a job"""
        job = get_object_or_404(Job, pk=pk)
        job.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)               
          
class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'description', 'created_on', 'client_id', 'accepted', 'pay', 'acceptedBy', 'complete','client_rating']
        # add client_rating from user/client view via serializer
        depth = 2          
