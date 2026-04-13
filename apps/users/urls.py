from django.urls import path
from apps.users.views import HomeView, UserListingAPiview, UsersView


urlpatterns = [

    path('', HomeView.as_view(), name='home'),
    path('users/', UsersView.as_view(), name='users'),




    # api urls
    path('list-users/', UserListingAPiview.as_view(), name='api-users-listing')
]
