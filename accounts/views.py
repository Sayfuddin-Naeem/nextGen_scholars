from rest_framework import status, permissions
from rest_framework.decorators import permission_classes, api_view
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
# For Token and Unique confirmation url genarate
from rest_framework.authtoken.models import Token
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.urls import reverse
from student.serializers import StudentSerializer
from teacher.serializers import TeacherSerializer
from .constants import TEACHER, STUDENT
from .serializers import *
from .utils import send_email, generate_confirmation_link
from .permission import IsStudent, IsTeacher
from .models import ContactUs


class StudentById(filters.BaseFilterBackend):
    def filter_queryset(self, request, query_set, view):
        user_id = request.query_params.get("user_id")
        if user_id:
            return query_set.filter(id = user_id)
        return query_set

class StudentViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(profile__role=STUDENT)
    serializer_class = StudentSerializer
    filter_backends = [StudentById]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Create unique confirmation link
            confirm_link = generate_confirmation_link(user)
            
            # Send confirmation email
            send_email(
                user=user,
                subject="Confirm Your Email",
                template="confirm_email.html",
                extra=confirm_link
            )
            
            return Response({'message': 'Check Your Mail for Confirmation', 'user_id': user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class TeacherById(filters.BaseFilterBackend):
    def filter_queryset(self, request, query_set, view):
        user_id = request.query_params.get("id")
        if user_id:
            return query_set.filter(id = user_id)
        return query_set

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(profile__role=TEACHER)
    serializer_class = TeacherSerializer
    filter_backends = [TeacherById]
    
    def get_permissions(self):
        if self.action in ['retrieve', 'update', 'partial_update']:
            self.permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'destroy':
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Create unique confirmation link
            confirm_link = generate_confirmation_link(user)
            
            # Send confirmation email
            send_email(
                user=user,
                subject="Confirm Your Email",
                template="confirm_email.html",
                extra=confirm_link
            )
            
            return Response({'message': 'Check Your Mail for Confirmation', 'user_id': user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError, OverflowError):
        return Response({'error': 'Invalid activation link'}, status=status.HTTP_400_BAD_REQUEST)

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return Response({'message': 'Account activated successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Activation failed'}, status=status.HTTP_400_BAD_REQUEST)


class UserLoginApiView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            # Authenticate the user
            user = authenticate(username=username, password=password)
            if user:
                # Ensure the user is logged in and get or create a token
                login(request, user)
                token, _ = Token.objects.get_or_create(user=user)
                
                # Check if the user is an admin
                if user.is_superuser or user.is_staff:
                    # Redirect to the Django admin panel
                    admin_url = reverse('admin:index')
                    return Response({
                        'token': token.key,
                        'user_id': user.id,
                        'user_type': user.profile.role,
                        'redirect_url': request.build_absolute_uri(admin_url)
                    }, status=status.HTTP_200_OK)
                else:
                    # For non-admin users, return the usual response
                    return Response({
                        'token': token.key,
                        'user_id': user.id,
                        'user_type': user.profile.role,
                        }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogoutApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Delete the token to log the user out
        request.user.auth_token.delete()
        
        # Perform logout
        logout(request)
        
        # Return a JSON response to confirm successful logout
        return Response({"message": "Logout successful."}, status=status.HTTP_200_OK)

class PasswordUpdateApiView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, *args, **kwargs):
        serializer = PasswordUpdateSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            user = request.user
            serializer.update(user, serializer.validated_data)
            return Response({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContactUsCreateView(CreateAPIView):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer