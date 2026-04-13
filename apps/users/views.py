from django.shortcuts import render

# Create your views here.

from django.views.generic import TemplateView
from rest_framework import generics, permissions, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from apps.users.models import Users as User
from apps.users.serializers import UserSerializer
from helpers.custom_response import ResponseInfo
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class BaseTemplateView(TemplateView):
    """
    Base view used across project
    """

    page_title = None
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # global context (available everywhere)
        context["app_name"] = "Club Management"
        context["page_title"] = self.page_title

        return context
    


class HomeView(BaseTemplateView):
    template_name = "dashboards/dashboard.html"
    page_title    = "Dashboard"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["message"] = "Hello from Advanced CBV"
        return context
    
    
class UsersView(BaseTemplateView):
    template_name = "dashboards/users.html"
    page_title    = "Users"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["message"] = "Hello from Advanced CBV"
        return context
    













class UserListingAPiview(generics.GenericAPIView):
    
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(UserListingAPiview, self).__init__(**kwargs)
    
    serializer_class    = UserSerializer
    permission_classes  = [permissions.IsAuthenticated]
    queryset            = User.objects.all()

    filter_backends     = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields    = ['is_active', 'is_staff', 'is_superuser', 'is_admin']
    search_fields       = ['username', 'name', 'home_name']
    ordering_fields     = ['username', 'name', 'id']
    ordering            = ['id']

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='search',
                in_=openapi.IN_QUERY,
                description='Search by username, name, home_name',
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                name='ordering',
                in_=openapi.IN_QUERY,
                description='Order by username, name, id (prefix with - for descending)',
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                name='is_active',
                in_=openapi.IN_QUERY,
                description='Filter by is_active',
                type=openapi.TYPE_BOOLEAN
            ),
            openapi.Parameter(
                name='is_staff',
                in_=openapi.IN_QUERY,
                description='Filter by is_staff',
                type=openapi.TYPE_BOOLEAN
            ),
            openapi.Parameter(
                name='is_superuser',
                in_=openapi.IN_QUERY,
                description='Filter by is_superuser',
                type=openapi.TYPE_BOOLEAN
            ),
            openapi.Parameter(
                name='is_admin',
                in_=openapi.IN_QUERY,
                description='Filter by is_admin',
                type=openapi.TYPE_BOOLEAN
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        users = self.get_queryset()
        page = self.paginate_queryset(users)
        serializer = self.serializer_class(page, many=True)
        print(self.get_paginated_response(serializer.data))
        return self.get_paginated_response(serializer.data)