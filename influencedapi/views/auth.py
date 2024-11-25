
from rest_framework.decorators import api_view
from rest_framework.response import Response

from influencedapi.models.user import User


@api_view(['POST'])
def check_user(request):
    '''Checks to see if user exists

    Method arguments:
      request -- The full HTTP request object
    '''
    uid = request.data['uid']

    # Use the built-in authenticate method to verify
    # authenticate returns the user object or None if no user is found
    user = User.objects.filter(uid=uid).first()

    # If authentication was successful, respond with their token
    if user is not None:
        data = {
            'id': user.id,
            'name': '',
            'uid': user.uid,
        }
        return Response(data)
    else:
        # Bad login details were provided. So we can't log the user in.
        data = { 'valid': False }
        return Response(data)


@api_view(['POST'])
def register_user(request):
    '''Handles the creation of a new user for authentication'''

    user = User.objects.create(
        bio=request.data['bio'],
        userName=request.data['userName'],
        client=request.data['client'],
        uid=request.data['uid'],
        rating=0  # Set default rating to 0 or null if preferred
    )

    # Return the user info to the client
    data = {
        'id': user.id,
        'uid': user.uid,
        'userName': user.userName,
        'bio': user.bio,
        'client': user.client,
        'rating': user.rating,  # The rating will be returned as 0
    }
    return Response(data)
