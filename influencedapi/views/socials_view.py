from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from influencedapi.models import User, Social
import logging
from django.shortcuts import get_object_or_404


# Define the logger
logger = logging.getLogger(__name__)

class SocialsViewSet(ViewSet):
    def retrieve(self, request, pk):
        """Handle GET requests for a single social record by its primary key"""
        try:
            logger.info(f"Retrieving social record with PK: {pk}")
            social = Social.objects.get(pk=pk)  # Querying by primary key
            serializer = SocialsSerializer(social)
            logger.info(f"Successfully retrieved social record with PK: {pk}")
            return Response(serializer.data)
        except Social.DoesNotExist:
            logger.error(f"Social record with PK: {pk} not found")
            return Response({'message': 'Social not found'}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests for all socials"""
        logger.info("Listing all social records")
        socials = Social.objects.all()
        serializer = SocialsSerializer(socials, many=True)
        logger.info(f"Successfully retrieved {len(socials)} social records")
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Handle POST requests to create a social record"""
        try:
            # Log the incoming request data
            logger.info(f"Received request data: {request.data}")

            # Ensure the user is authenticated and obtain the user object
            user = get_object_or_404(User, id=request.data["user_id"])

            # Create a new social record and associate it with the user
            social = Social.objects.create(
                user_id=user,
                facebook=request.data.get("facebook", ""),
                instagram=request.data.get("instagram", ""),
                bluesky=request.data.get("bluesky", ""),
                tiktok=request.data.get("tiktok", ""),
                twitter=request.data.get("twitter", "")
            )

            # Log the successful creation
            logger.info(f"Created social record for user: {user.id}")

            # Serialize and return the response
            serializer = SocialsSerializer(social)
            return Response({'message': 'Social created successfully!', 'data': serializer.data}, status=status.HTTP_201_CREATED)

        except KeyError as e:
            logger.error(f"Missing required field: {e}")
            return Response({'message': f'Missing required field: {e}'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        """Handle PUT requests to update an existing social record"""
        try:
            logger.info(f"Updating social record with PK: {pk}")

            # Log the incoming data
            logger.debug(f"Received data: {request.data}")

            # Fetch the existing Social record
            social = get_object_or_404(Social, pk=pk)

            # Update the fields
            social.facebook = request.data.get("facebook", social.facebook)
            social.instagram = request.data.get("instagram", social.instagram)
            social.bluesky = request.data.get("bluesky", social.bluesky)
            social.tiktok = request.data.get("tiktok", social.tiktok)
            social.twitter = request.data.get("twitter", social.twitter)
            social.save()

            logger.info(f"Successfully updated social record with PK: {pk}")

            # Serialize and return the response
            serializer = SocialsSerializer(social)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Social.DoesNotExist:
            logger.error(f"Social record with PK: {pk} not found")
            return Response({'message': 'Social not found'}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk):
        """Handle DELETE requests to delete a social"""
        try:
            logger.info(f"Attempting to delete social record with PK: {pk}")
            social = Social.objects.get(pk=pk)
            social.delete()
            logger.info(f"Successfully deleted social record with PK: {pk}")
            return Response({'message': 'Social deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Social.DoesNotExist:
            logger.error(f"Social record with PK: {pk} not found")
            return Response({'message': 'Social not found'}, status=status.HTTP_404_NOT_FOUND)


class SocialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Social
        fields = ['id', 'facebook', 'instagram', 'bluesky', 'tiktok', 'twitter', 'user_id']
