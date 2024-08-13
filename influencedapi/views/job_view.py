# views.py
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from influencedapi.models import Job, User
from rest_framework import serializers, status

class JobView(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        """Handle GET requests for a single job"""
        job = get_object_or_404(Job, pk=pk)
        serializer = JobSerializer(job)
        return Response(serializer.data)

    # def list(self, request):
    #     """Handle GET requests for all jobs or filtered jobs"""
    #     accepted_by_id = request.query_params.get('acceptedBy')

    #     if accepted_by_id is not None:
    #         try:
    #             jobs = Job.objects.filter(acceptedBy=accepted_by_id)
    #         except ValueError:
    #             # If `accepted_by_id` is not a valid integer, return a bad request
    #             return Response({'message': 'Invalid user ID'}, status=status.HTTP_400_BAD_REQUEST)
    #     else:
    #         jobs = Job.objects.all()

    #     serializer = JobSerializer(jobs, many=True)
    #     return Response(serializer.data)
    def list(self, request):
        """Handle GET requests for all jobs or filtered jobs"""
        accepted_by_id = request.query_params.get('acceptedBy')
        client_id = request.query_params.get('client')  # Use the query parameter 'client'

        print(f"Accepted By ID: {accepted_by_id}")  # Debugging line for acceptedBy
        print(f"Client ID: {client_id}")  # Debugging line for client

        # Filter jobs based on the provided parameters
        if accepted_by_id and client_id:
            jobs = Job.objects.filter(acceptedBy_id=accepted_by_id, client_id=client_id)
        elif accepted_by_id:
            jobs = Job.objects.filter(acceptedBy_id=accepted_by_id)
        elif client_id:
            jobs = Job.objects.filter(client_id=client_id)  # Filter by client_id
        else:
            jobs = Job.objects.all()

        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)





    def create(self, request):
        """Handle POST requests to create a new job"""
        try:
            # Validate foreign key references
            client = get_object_or_404(User, id=request.data.get("client_id"))
            accepted_by = get_object_or_404(User, id=request.data.get("acceptedBy"))

            # Create a new Job object
            job = Job.objects.create(
                description=request.data.get("description"),
                client_id=client,
                accepted=request.data.get("accepted", False),
                pay=request.data.get("pay"),
                acceptedBy=accepted_by,
                complete=request.data.get("complete", False)
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
              
          
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'userName', 'rating', 'client', 'bio', 'uid']
class JobSerializer(serializers.ModelSerializer):
    client = UserSerializer(read_only=True)
    acceptedBy = UserSerializer(read_only=True)

    class Meta:
        model = Job
        fields = ['id', 'description', 'created_on', 'client_id', 'accepted', 'pay', 'acceptedBy', 'complete','client']
        depth = 2
         
