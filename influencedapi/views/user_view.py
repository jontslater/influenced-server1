from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from influencedapi.models import User

class UserView(ViewSet):
    def retrieve(self, request, pk):
        """Handle GET requests for a single user"""
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
          
    def list(self, request):
        """Handle GET requests for all users"""
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)   
      
    def create(self, request):
        """Handle POST requests to create a new user"""
        try:
            user = User.objects.create(
                userName=request.data["userName"],
                rating=request.data["rating"],
                client=request.data["client"],
                bio=request.data["bio"],
                uid=request.data["uid"]
            )
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except KeyError as e:
            return Response({'message': f'Missing required field: {e}'}, status=status.HTTP_400_BAD_REQUEST)
      
    def update(self, request, pk):
        """Handle PUT/PATCH requests to update an existing user"""
        try:
            user = User.objects.get(pk=pk)
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
        
    def destroy(self, request, pk):
        """Handle DELETE requests to delete a user"""
        try:
            user = User.objects.get(pk=pk)
            user.delete()
            return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'userName', 'rating', 'client', 'bio', 'uid']
