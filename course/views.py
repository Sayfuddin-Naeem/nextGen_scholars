from django.core.exceptions import PermissionDenied
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError
from rest_framework import viewsets, pagination, filters
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from accounts.permission import IsStudent
from .models import *
from .serializers import *

# Create your views here.

class DepartmentCustomFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, query_set, view):
        dept_id = request.query_params.get("id")
        dept_slug = request.query_params.get("slug")
        if dept_id:
            return query_set.filter(id = dept_id)
        if dept_slug:
            return query_set.filter(slug = dept_slug)
        return query_set

class DepartmentReadOnlyViewset(ReadOnlyModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    filter_backends = [DepartmentCustomFilter]

class CourseCustomFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        course_id = request.query_params.get("course_id")
        dept_id = request.query_params.get("dept_id")
        dept_slug = request.query_params.get("dept_slug")
        teacher_id = request.query_params.get("teacher_id")

        if course_id:
            queryset = queryset.filter(id=course_id)
        if dept_id:
            queryset = queryset.filter(department__id=dept_id)
            
        if dept_slug:
            queryset = queryset.filter(department__slug=dept_slug)

        # Apply filtering by teacher_id only if the authenticated user is an instructor
        if teacher_id and request.user.is_authenticated:
            current_teacher = request.user.profile.teacher
            
            # Allow filtering by teacher_id only if the user is the course instructor
            if teacher_id == str(current_teacher.id):
                queryset = queryset.filter(instructor__id=teacher_id)
            else:
                raise PermissionDenied("You do not have permission to filter by this teacher ID.")

        return queryset

class CoursePagination(pagination.PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 100

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [CourseCustomFilter]
    pagination_class = CoursePagination

    def destroy(self, request, *args, **kwargs):
        course = self.get_object()

        # Check if the current user is the instructor of the course
        if course.instructor != request.user.profile.teacher:
            return Response(
                {"error": "You do not have permission to delete this course."},
                status=status.HTTP_403_FORBIDDEN,
            )
            
        return super().destroy(request, *args, **kwargs)

class EnrollmentPagination(pagination.PageNumberPagination):
    page_size = 9
    page_size_query_param = 'page_size'
    max_page_size = 100

class CourseEnrollmentViewSet(viewsets.ModelViewSet):
    queryset = CourseEnrollment.objects.all()
    serializer_class = CourseEnrollmentSerializer
    pagination_class = EnrollmentPagination
    permission_classes = [IsAuthenticated & IsStudent]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['course_id'] = self.kwargs.get('course_id')  # Add course_id to context
        return context

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        enrollment = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def perform_create(self, serializer):
        course_id = self.request.data.get('course_id')
        if not course_id:
            raise ValidationError('Course ID is required.')

        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            raise ValidationError('Course not found.')

        serializer.save(course=course)



