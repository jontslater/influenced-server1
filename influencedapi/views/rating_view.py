from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from influencedapi.models import Rating, Job, User
from django.shortcuts import get_object_or_404

class RatingViewSet(ViewSet):
    """
    A simple ViewSet for viewing and editing ratings.
    """
    def list(self, request):
        """Handle GET requests to list all ratings"""
        queryset = Rating.objects.all()
        serializer = RatingSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Handle GET requests to retrieve a specific rating"""
        rating = get_object_or_404(Rating, pk=pk)
        serializer = RatingSerializer(rating)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """Handle POST requests to create a new rating"""
        try:
            job = get_object_or_404(Job, id=request.data["job"])
            user = get_object_or_404(User, id=request.data["user"])
            client = get_object_or_404(User, id=request.data["client"])

            rating = Rating.objects.create(
                job=job,
                user_rating=request.data["user_rating"],
                client_rating=request.data["client_rating"],
                user=user,
                client=client
            )
            serializer = RatingSerializer(rating)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except KeyError as e:
            return Response({'message': f'Missing required field: {e}'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Handle PUT/PATCH requests to update a rating"""
        rating = get_object_or_404(Rating, pk=pk)

        try:
            job = get_object_or_404(Job, id=request.data.get("job", rating.job.id))
            user = get_object_or_404(User, id=request.data.get("user", rating.user.id))
            client = get_object_or_404(User, id=request.data.get("client", rating.client.id))
        except KeyError as e:
            return Response({'message': f'Missing required field: {e}'}, status=status.HTTP_400_BAD_REQUEST)

        rating.job = job
        rating.user_rating = request.data.get("user_rating", rating.user_rating)
        rating.client_rating = request.data.get("client_rating", rating.client_rating)
        rating.user = user
        rating.client = client
        
        rating.save()
        serializer = RatingSerializer(rating)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        """Handle DELETE requests to delete a rating"""
        rating = get_object_or_404(Rating, pk=pk)
        rating.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'user_rating','client_rating', 'job','user','client']
        depth = 2
