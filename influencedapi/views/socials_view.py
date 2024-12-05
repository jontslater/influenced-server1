from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from influencedapi.models import User, Social
from django.shortcuts import get_object_or_404

class SocialsViewSet(ViewSet):
    def retrieve(self, request, pk):
        """Handle GET requests for a single social"""
        try:
            social = Social.objects.get(pk=pk)
            serializer = SocialsSerializer(social)
            return Response(serializer.data)
        except Social.DoesNotExist:
            return Response({'message': 'Social not found'}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests for all socials"""
        socials = Social.objects.all()
        serializer = SocialsSerializer(socials, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST requests to create a new social"""
        try:
            print("Request Data:", request.data)
            user = get_object_or_404(User, id=request.data["user_id"])
            social = Social.objects.create(
                facebook=request.data.get("facebook", ""),
                instagram=request.data.get("instagram", ""),
                bluesky=request.data.get("bluesky", ""),
                tiktok=request.data.get("tiktok", ""),
                twitter=request.data.get("twitter", ""),
                user=user  # Assign the actual User instance
            )
            serializer = SocialsSerializer(social)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except KeyError as e:
            return Response({'message': f'Missing required field: {e}'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        """Handle PUT requests to update a social"""
        try:
            social = Social.objects.get(pk=pk)
            social.facebook = request.data.get("facebook", social.facebook)
            social.instagram = request.data.get("instagram", social.instagram)
            social.bluesky = request.data.get("blueSky", social.bluesky)
            social.tiktok = request.data.get("tikTok", social.tiktok)
            social.twitter = request.data.get("twitter", social.twitter)
            social.save()
            serializer = SocialsSerializer(social)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Social.DoesNotExist:
            return Response({'message': 'Social not found'}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk):
        """Handle DELETE requests to delete a social"""
        try:
            social = Social.objects.get(pk=pk)
            social.delete()
            return Response({'message': 'Social deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Social.DoesNotExist:
            return Response({'message': 'Social not found'}, status=status.HTTP_404_NOT_FOUND)
          
          
class SocialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Social
        fields = ['id', 'facebook', 'instagram', 'bluesky', 'tiktok', 'twitter', 'user_id']
        depth = 1          
