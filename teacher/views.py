from django.shortcuts import render
from rest_framework import filters
from rest_framework.viewsets import ReadOnlyModelViewSet
from .serializers import *
from .models import Designation, Specialization

# Create your views here.

class DesignationById(filters.BaseFilterBackend):
    def filter_queryset(self, request, query_set, view):
        designation_id = request.query_params.get("id")
        if designation_id:
            return query_set.filter(id = designation_id)
        return query_set

class DesignationReadOnlyViewset(ReadOnlyModelViewSet):
    queryset = Designation.objects.all()
    serializer_class = DesignationSerializer
    filter_backends = [DesignationById]
    
class SpecializationById(filters.BaseFilterBackend):
    def filter_queryset(self, request, query_set, view):
        designation_id = request.query_params.get("id")
        if designation_id:
            return query_set.filter(id = designation_id)
        return query_set

class SpecializationReadOnlyViewset(ReadOnlyModelViewSet):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer
    filter_backends = [SpecializationById]