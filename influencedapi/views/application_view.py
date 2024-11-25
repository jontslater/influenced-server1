from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from influencedapi.models import Application, Job
from rest_framework import serializers

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['id', 'applicant', 'poster', 'job', 'applied_on']

class ApplicationViewSet(ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

    def create(self, request, *args, **kwargs):
        """Handle POST requests to apply for a job."""
        applicant = request.user
        job_id = request.data.get('job_id')
        
        # Ensure job and poster exist
        job = get_object_or_404(Job, id=job_id)
        poster = job.client_id
        
        # Check if the applicant is trying to apply to their own job
        if applicant.id == poster.id:
            return Response({"error": "You cannot apply to your own job."},
                            status=status.HTTP_400_BAD_REQUEST)
        
        # Create application
        application, created = Application.objects.get_or_create(
            applicant=applicant,
            job=job,
            poster=poster
        )

        if created:
            serializer = self.get_serializer(application)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "You have already applied for this job."},
                            status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        """List applications for a particular job or applicant."""
        job_id = request.query_params.get('job_id')
        applicant_id = request.query_params.get('applicant_id')

        if job_id:
            applications = Application.objects.filter(job_id=job_id)
        elif applicant_id:
            applications = Application.objects.filter(applicant_id=applicant_id)
        else:
            applications = self.get_queryset()
        
        serializer = self.get_serializer(applications, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """Handle PUT/PATCH requests to update an application."""
        application = self.get_object()  # Fetch the application object
        job_id = request.data.get('job_id')
        
        # Check if the job is valid
        if job_id:
            job = get_object_or_404(Job, id=job_id)
            application.job = job  # Update the job for the application
        
        # Check if applicant or poster is trying to update (optional check)
        if application.applicant != request.user:
            return Response({"error": "You can only update your own application."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Save the updated application object
        application.save()

        serializer = self.get_serializer(application)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """Handle DELETE requests to remove an application."""
        application = self.get_object()  # Fetch the application object
        
        # Check if applicant is trying to delete their own application
        if application.applicant != request.user:
            return Response({"error": "You can only delete your own application."},
                            status=status.HTTP_400_BAD_REQUEST)
        
        # Delete the application
        application.delete()
        return Response({"message": "Application deleted successfully."},
                        status=status.HTTP_204_NO_CONTENT)
