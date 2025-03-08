from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from .models import UserProfile
from .serializers import UserProfileSerializer

class UserRegistrationView(APIView):
    def get_user_credentials(self, email):
        cached_data = UserProfile.get_cached_credentials(email)
        if cached_data:
            return cached_data
        try:
            user = UserProfile.objects.get(email=email)
            return {'email': user.email, 'password': user.password}
        except UserProfile.DoesNotExist:
            return None

    def post(self, request):
        try:
            serializer = UserProfileSerializer(data=request.data)
            if serializer.is_valid():
                serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
                user = serializer.save()
                
                # Cache the credentials after saving
                credentials = self.get_user_credentials(user.email)
                
                return Response({
                    "status": "success",
                    "message": "Registration successful",
                    "user": UserProfileSerializer(user).data
                }, status=status.HTTP_201_CREATED)
            
            return Response({
                "status": "error",
                "message": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                "status": "error",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
