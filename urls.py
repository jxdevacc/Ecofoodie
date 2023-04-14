from django.urls import path, include
from .views import *
# from knox import views as knox_views

from rest_framework.routers import DefaultRouter
# from rest_framework_jwt.views import refresh_jwt_token, verify_jwt_token

router = DefaultRouter()
router.register('producers', ProducerView, basename = 'producers')
router.register('posts', PostView, basename = 'posts')
router.register('reviews', ReviewView, basename = 'reviews')
router.register('users', UserList, basename = 'users')
router.register('groups', GroupView, basename = 'groups')
# router.register('users', UserViewSet, basename = 'users')
urlpatterns = [
     path('auth/test', TestView.as_view()),
    path('auth/create-user/', UserView.as_view()),
    path('auth/get-user/', UserLoginView.as_view()),
    path('auth/producers/<str:pk>', ProducerDetails.as_view()),
    path('auth/posts/<str:pk>', PostDetails.as_view()),
    path('auth/reviews/<str:pk>', ReviewDetails.as_view()),
    path('auth/groups/<str:pk>', GroupDetails.as_view()),
    # path('auth/producers', ProducerView.as_view()),
    # path('auth/', include('knox.urls')),
    # path('auth/user', UserAPI.as_view()),
    # path('auth/logout', knox_views.LogoutView.as_view(), name = 'knox_logout'),
    path('auth/login-user/', UserLoginView.as_view()),
    path('auth/', include(router.urls)),
    # path('login/', views.loginPage, name="login"),
    # path('logout/', views.logoutUser, name="logout"),
    # path('register/', views.registerPage, name="register"),
    # path('api/usersemail/<str:email>', UserDetailsEmail.as_view(), name = "useremail"),
    # path('api/userspass/<str:password>', UserDetailsPassword.as_view(), name = "userpass"),
    # path('api/users/', UsersList.as_view(), name = "users"),
    # UserViewSet.as_view()
]

