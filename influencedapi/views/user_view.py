from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from influencedapi.models import User, Social

class UserView(ViewSet):
    def retrieve(self, request, pk=None):
        """Handle GET requests for a single user by UID or ID"""
        try:
            if pk.isdigit():  # Check if pk is numeric
                user = User.objects.get(id=pk)  # Fetch by ID
            else:
                user = User.objects.get(uid=pk)  # Fetch by UID
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
          
    def list(self, request):
        """Handle GET requests for all users"""
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)   
      
    # def create(self, request):
    #     """Handle POST requests to create a new user"""
    #     try:
    #         user = User.objects.create(
    #             userName=request.data["userName"],
    #             rating=request.data["rating"],
    #             client=request.data["client"],
    #             bio=request.data["bio"],
    #             uid=request.data["uid"]
    #         )
    #         serializer = UserSerializer(user)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     except KeyError as e:
    #         return Response({'message': f'Missing required field: {e}'}, status=status.HTTP_400_BAD_REQUEST)
    
    def create(self, request):
        """Handle POST requests to create a new user and associated social record"""
        try:
            user = User.objects.create(
                userName=request.data["userName"],
                rating=request.data["rating"],
                client=request.data["client"],
                bio=request.data["bio"],
                uid=request.data["uid"]
            )

            # Automatically create a Social record
            Social.objects.create(user=user)

            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except KeyError as e:
            return Response({'message': f'Missing required field: {e}'}, status=status.HTTP_400_BAD_REQUEST)

      
    def update(self, request, pk=None, uid=None):
        """Handle PUT/PATCH requests to update an existing user by id or uid"""
        try:
            if pk:
                user = User.objects.get(pk=pk)
            elif uid:
                user = User.objects.get(uid=uid)
            else:
                return Response({'message': 'User ID or UID must be provided'}, status=status.HTTP_400_BAD_REQUEST)
                
            user.userName = request.data.get("userName", user.userName)
            user.rating = request.data.get("rating", user.rating)
            user.client = request.data.get("client", user.client)
            user.bio = request.data.get("bio", user.bio)
            user.uid = request.data.get("uid", user.uid)
            user.save()
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
    def destroy(self, request, pk=None, uid=None):
        """Handle DELETE requests to delete a user by id or uid"""
        try:
            if pk:
                user = User.objects.get(pk=pk)
            elif uid:
                user = User.objects.get(uid=uid)
            else:
                return Response({'message': 'User ID or UID must be provided'}, status=status.HTTP_400_BAD_REQUEST)
                
            user.delete()
            return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class SocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Social
        fields = ['id', 'facebook', 'instagram', 'bluesky', 'tiktok', 'twitter']

class UserSerializer(serializers.ModelSerializer):
    social = SocialSerializer(many=True)  # Add many=True here

    class Meta:
        model = User
        fields = ['id', 'userName', 'bio', 'social']
