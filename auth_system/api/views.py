from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


# this is responsible to show information about the user after decode it 
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['email_address'] = user.email
        token['mobile'] = user.mobile
        token['first_sign_in'] = user.first_sign_in
        # ...

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# Return all apis to check them
@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/auth/token/'
    ]

    return Response(routes)