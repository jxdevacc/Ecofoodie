# from django.shortcuts import render

from telnetlib import STATUS
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .serializers import *
from .models import *
from rest_framework import status
from rest_framework import viewsets
from rest_framework import status, generics, mixins
from django.shortcuts import get_object_or_404, render, redirect

from django.views.generic.list import ListView


# from knox.models import AuthToken
# from rest_framework import generics, permissions
# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail

# Create your views here.
from django.shortcuts import render

# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail

# import uuid
# import hashlib

# from .models import Token
# Create your views here.


class TestView(APIView):
    def get(self, request, format=None):
        print("API Was Called")
        return Response("You Made It", status=200)

class UserView(APIView):
    def post(self, request, format=None):
        print("Creating a user")

        user_data = request.data
        user_data['is_active'] = False

        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid(raise_exception=False):
            user = user_serializer.save()
            # token = AuthToken.objects.create(user)

            # message = Mail(
            #     from_email="tim@poieo-dev.com",
            #     to_emails=user_data['email'],
            #     subject='Please Confirm your Email Address',
            #     html_content=f"\
            #     Hi {user_data['first_name']},\
            #     <br><br>Thank you for signing up. To confirm your email address, please click <a href='http://localhost:8000/api/v1.0/user/verify-user/{token}'>HERE</a>\
            #     "
            #     )

            # try:
            #     sg = SendGridAPIClient("<<SENDGRID API KEY>>")
            #     response = sg.send(message)

            #     return Response(user_serializer.data, status=200)

            # except Exception as e:
            #     print("ERROR", e)

            return Response(user_serializer.data, status=200) #{"user": user_serializer.data, "token": token}

            # salt = uuid.uuid4().hex
            # hash_object = hashlib.sha256(salt.encode() + str(user_serializer.data['id']).encode())
            # token = hash_object.hexdigest() + ':' + salt

            # token_serializer=TokenSerializer(data={"user":user_serializer.data['id'], "token":token})
            # if token_serializer.is_valid(raise_exception=False):
            #     token_serializer.save()


            #     message = Mail(
            #         from_email="tim@poieo-dev.com",
            #         to_emails=user_data['email'],
            #         subject='Please Confirm your Email Address',
            #         html_content=f"\
            #         Hi {user_data['first_name']},\
            #         <br><br>Thank you for signing up. To confirm your email address, please click <a href='http://localhost:8000/api/v1.0/user/verify-user/{token}'>HERE</a>\
            #         "
            #         )

            #     try:
            #         sg = SendGridAPIClient("<<SENDGRID API KEY>>")
            #         response = sg.send(message)


            #     except Exception as e:
            #         print("ERROR", e)

        else:
            print(user_serializer.errors)

        return Response({"msg":"ERR"}, status=400)

        # class UserVerificationView(APIView):

        #     def get(self, request, pk, format=None):
        #         print("VERIFYING USER", pk)

        #         tokenObj = Token.objects.filter(token=pk).first()


        #         user = User.objects.filter(id=tokenObj.user.id).first()

        #         if user:
        #             user_serializer = UserSerializer(user, data={'is_active':True}, partial=True)
        #             if user_serializer.is_valid(raise_exception=False):
        #                 user_serializer.save()

        #                 return Response(status=200)

        #         return Response(status=404)



class UserLoginView(APIView):
    # Convert a user token into user data 
    # def get(self, request, email=None):
    #     user = self.get_object(email)
    #     serializer = UserSerializer(user)
    #     return Response(serializer.data)
    
    # def get(self, request, format=None):
    #     users = User.objects.all()
    #     serializer = UserSerializer(users, many=True)
    #     return Response(serializer.data)
    def get(self, request, format=None):

        if request.user.is_authenticated == False or request.user.is_active == False:
            return Response("Invalid Credentials", status=403)

        user = UserSerializer(request.user)
        return Response(user.data, status=200)

    def post(self, request, format=None):
        print("Login Class")

        user_obj = User.objects.filter(email=request.data['username']).first() or User.objects.filter(username=request.data['username']).first()

        if user_obj is not None:
            credentials = {
                'username': user_obj.username,
                'password': request.data['password']
            }
            user = authenticate(**credentials)

            if user and user.is_active:
                user_serializer = UserSerializer(user)
                # token = AuthToken.objects.create(user)
                return Response(user_serializer.data, status=200) #{"user": user_serializer.data, "token": token}

        return Response("Invalid Credentials", status=403)


class UserList(viewsets.ViewSet):
    def list(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)



class ProducerView(viewsets.ViewSet):
    def list(self, request):
        producers = Producer.objects.all()
        serializer = ProducerSerializer(producers, many=True)
        return Response(serializer.data)

    def create(self, request):

        serializer = ProducerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def retrieve(self, request, email=None):
    #     queryset = Producer.objects.all()
    #     producer = get_object_or_404(queryset, email=email)
    #     serializer = ProducerSerializer(producer)
    #     lookup_field = 'email'
    #     return Response(serializer.data)

    # def update(self, request, email=None):
    #     producer = Producer.objects.get(email=email)
    #     serializer = ProducerSerializer(producer, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # def destroy(self, request, email=None):
    #     producer = Producer.objects.get(email=email)
    #     producer.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


class ProducerDetails(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = Producer.objects.all()
    serializer_class = ProducerSerializer
    lookup_fields = "email"

    def get(self, request, pk):
        return self.retrieve(request, email=pk)
    
    def put(self, request, pk):
        return self.update(request, email=pk)
    def delete(self, request, pk):
        return self.destroy(request, email=pk)


class PostView(viewsets.ViewSet):
    def list(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def create(self, request):
        print(request)
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostDetails(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request, pk):
        return self.retrieve(request, pk=pk)
    
    def put(self, request, pk):
        return self.update(request, pk=pk)
    def delete(self, request, pk):
        return self.destroy(request, pk=pk)

class ReviewView(viewsets.ViewSet):
    def list(self, request):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def create(self, request):
        print(request)
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReviewDetails(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get(self, request, pk):
        return self.retrieve(request, pk=pk)
    
    def put(self, request, pk):
        return self.update(request, pk=pk)
    def delete(self, request, pk):
        return self.destroy(request, pk=pk)


class GroupView(viewsets.ViewSet):
    def list(self, request):
        groups = Group.objects.all()
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)

    def create(self, request):
        print(request)
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GroupDetails(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def get(self, request, pk):
        return self.retrieve(request, pk=pk)
    
    def put(self, request, pk):
        return self.update(request, pk=pk)
    def delete(self, request, pk):
        return self.destroy(request, pk=pk)


# class ProducerDetails(DetailView):
#     model = Producer

# class ProducerView(viewsets.ViewSet):
#     def list(self, request):
#         producers = Producer.objects.all()
#         serializer = ProducerSerializer(producers, many=True)
#         return Response(serializer.data)

#     def create(self, request):
#         # user = User.objects.filter(email=request.data['email']['username']).first() or User.objects.filter(username=request.data['email']['username']).first()
#         # if user is not None:
#         #     request.data['email'] = user
#         #     print(request.data)
#         serializer = ProducerSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def retrieve(self, request, email=None):
#         queryset = Producer.objects.all()
#         producer = get_object_or_404(queryset, email=email)
#         serializer = ProducerSerializer(producer)
#         # lookup_field = 'email'
#         return Response(serializer.data)

#     def update(self, request, email=None):
#         producer = Producer.objects.get(email=email)
#         serializer = ProducerSerializer(producer, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def destroy(self, request, email=None):
#         producer = Producer.objects.get(email=email)
#         producer.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class ProducerView(APIView):
#     def get_object(self, email=None):
#         try:
#             return Producer.objects.get(email=email)
#         except Producer.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
    
#     def get(self, request, email=None):
#         user = self.get_object(email)
#         serializer = ProducerSerializer(user)
#         return Response(serializer.data)
    
#     def put(self, request, email=None):
#         user = self.get_object(email)
#         serializer = ProducerView(user, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, email=None):
#         producer = self.get_object(email)
#         producer.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class UserAPI(generics.RetrieveAPIView):
#     permission_classes = [ 
#         permissions.IsAuthenticated,
#     ]
#     serializer_class = UserSerializer
#     def get_object(self):
#         return self.request.user

# class TestView(APIView):
#     def get(self, request, format=None):
#         print("API Was Called")
#         return Response("You Made It", status=200)


# class UserView(APIView):
#     def post(self, request, format=None):
#         print("Creating a user")

#         user_data = request.data
#         print(request.data)

#         user_serializer = UserSerializer(data=user_data)
#         if user_serializer.is_valid(raise_exception=False):
#             user_serializer.save()

#             return Response({"user":user_serializer.data}, status=200)


#         return Response({"msg":"ERR"}, status=400)




# class UserLoginView(APIView):
#     # Convert a user token into user data
#     def get(self, request, format=None):

#         if request.user.is_authenticated == False or request.user.is_active == False:
#             return Response("Invalid Credentials", status=403)

#         user = UserSerializer(request.user)
#         return Response(user.data, status=200)

#     def post(self, request, format=None):
#         print("Login Class")

#         user_obj = User.objects.filter(email=request.data['username']).first() or User.objects.filter(username=request.data['username']).first()

#         if user_obj is not None:
#             credentials = {
#                 'username': user_obj.username,
#                 'password': request.data['password']
#             }
#             user = authenticate(**credentials)

#             if user and user.is_active:
#                 user_serializer = UserSerializer(user)
#                 return Response(user_serializer.data, status=200)

#         return Response("Invalid Credentials", status=403)



# # from .models import *
# # from django.http import HttpResponse
# # from django.db.models import *
# # from .serializers import *
# # from rest_framework import viewsets
# # from rest_framework.views import APIView
# from rest_framework.response import Response
# # from rest_framework import status, generics, mixins
# from django.contrib.auth import authenticate, login, logout
# # from django.contrib import messages
# # from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.decorators import login_required
# # from django.shortcuts import get_object_or_404, render, redirect
# # from django.views.decorators.csrf import csrf_exempt
# # from rest_framework.decorators import api_view
# # Create your views here.


# def registerPage(request):

# def loginPage(request):


# # @csrf_exempt
# # @api_view(['GET', 'POST'])
# # def loginPage(request):
# #     if request.user.is_authenticated:
# #         email = request.POST.get('email').lower()
# #         user = User.objects.get(email=email)
# #         serializer = CurrentUserSerializer(user)
# #         return Response(serializer.data)

# #     if request.method == 'POST':
# #         email = request.POST.get('email').lower()
# #         password = request.POST.get('password')

# #         try:
# #             user = User.objects.get(email=email)
# #         except:
# #             messages.error(request, 'User does not exist')

# #         user = authenticate(request, email=email, password=password)

# #         if user is not None:
# #             login(request, user)
# #             serializer = CurrentUserSerializer(user)
# #             return Response(serializer.data)
# #         else:
# #             messages.error(request, 'Username OR password does not exit')

# # @csrf_exempt
# # @api_view(['GET', 'POST'])
# # def logoutUser(request):
# #     email = request.POST.get('email').lower()
# #     user = User.objects.get(email=email)
# #     serializer = CurrentUserSerializer(user)
# #     logout(request)
# #     return Response(serializer.data)

# # @csrf_exempt
# # @api_view(['GET', 'POST'])
# # def registerPage(request):
# #     form = Create()
# #     if request.method == 'POST':
# #         form = Create(request.POST)
# #         if form.is_valid():
# #             user = form.save(commit=False)
# #             user.username = user.username.lower()
# #             user.save()
# #             login(request, user)
# #             print(user)
# #             serializer = CurrentUserSerializer(user)
# #             print(serializer.data)
# #             return Response(serializer.data)
# #         else:
# #             print("boo")
# #             return Response("hello")
# #     return Response("hello")















# # class ArticleViewSet(viewsets.ModelViewSet):
# #     queryset = Article.objects.all()
# #     serializer_class = ArticleSerializer

# # class UsersList(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
# #     queryset = User.objects.all()
# #     serializer_class = UserSerializer

# #     def get(self, request):
# #         return self.list(request)
    
# #     def post(self, request):
# #         return self.create(request)

# # class UserDetailsEmail(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
# #     queryset = User.objects.all()
# #     serializer_class = UserSerializer
# #     lookup_fields = "email"

# #     def get(self, request, email):
# #         return self.retrieve(request, email=email)
    
# #     def put(self, request, email):
# #         return self.update(request, email=email)
# #     def delete(self, request, email):
# #         return self.destroy(request, email=email)

# # class UserDetailsPassword(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
# #     queryset = User.objects.all()
# #     serializer_class = UserSerializer
# #     lookup_fields = "password"

# #     def get(self, request, password):
# #         return self.retrieve(request, password=password)
# #     def put(self, request, password):
# #         return self.update(request, password=password)
# #     def delete(self, request, password):
# #         return self.destroy(request, password=password)


# # class UserViewSet(viewsets.ModelViewSet):
# #     queryset = User.objects.all()
# #     serializer_class = UserSerializer

# # class UserViewSet(APIView):
# #     def get(self, pk=None):  
# #         try:
# #             user = User.objects.get(pk=pk)
# #             print(user)
# #             return user
# #         except User.DoesNotExist:
# #             return Response(status= STATUS.HTTP_404_NOT_FOUND)

# #this works:


















# class UserViewSet(viewsets.ViewSet):
#     def list(self, request):
#         users = User.objects.all()
#         serializer = UserSerializer(users, many=True)
#         return Response(serializer.data)

#     def create(self, request):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def retrieve(self, request, email=None):
#         queryset = User.objects.all()
#         user = get_object_or_404(queryset, email=email)
#         serializer = UserSerializer(user)
#         # lookup_field = 'email'
#         return Response(serializer.data)

#     def update(self, request, pk=None):
#         user = User.objects.get(pk=pk)
#         serializer = UserSerializer(user, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def destroy(self, request, pk=None):
#         user = User.objects.get(pk=pk)
#         user.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# # def specificuser(request):
# #     registered = False

# #     if request.method == 'POST':
# #         user_form = User(data=request.POST)

# #         if user_form.is_valid():
# #             user = user_form.save()
# #             user.set_password(user.password)
# #             user.password = ""
# #             user.username = user.email
# #             user.save()

# #             profile = profile_form.save(commit=False)
# #             profile.user = user
# #             profile.email = user.email
# #             profile.save()

# #             user.first_name = profile.first_name
# #             user.last_name = profile.last_name
# #             user.save()

# #             registered = True
# #             return HttpResponseRedirect(reverse('registration'))
# #         else:
# #             print user_form.errors, profile_form.errors
# #     else:
# #         user_form = UserForm()
# #         profile_form = UserProfileForm1()

# #     context = {'user_form': user_form, 'profile_form': profile_form, 'registered': registered}
# #     return render(request, 'mysite/register.html', context)

# '''
# class ArticleViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
#     queryset = Article.objects.all()
#     serializer_class = ArticleSerializer


# class ArticleViewSet(viewsets.ViewSet):
#     def list(self, request):
#         articles = Article.objects.all()
#         serializer = ArticleSerializer(articles, many=True)
#         return Response(serializer.data)

#     def create(self, request):
#         serializer = ArticleSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def retrieve(self, request, pk=None):
#         queryset = Article.objects.all()
#         article = get_object_or_404(queryset, pk=pk)
#         serializer = ArticleSerializer(article)
#         return Response(serializer.data)

#     def update(self, request, pk=None):
#         article = Article.objects.get(pk=pk)
#         serializer = ArticleSerializer(article, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def destroy(self, request, pk=None):
#         article = Article.objects.get(pk=pk)
#         article.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# class ArticleList(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
#     queryset = Article.objects.all()
#     serializer_class = ArticleSerializer

#     def get(self, request):
#         return self.list(request)
    
#     def post(self, request):
#         return self.create(request)

# class ArticleDetails(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
#     queryset = Article.objects.all()
#     serializer_class = ArticleSerializer
#     lookup_field = "id"

#     def get(self, request, id):
#         return self.retrieve(request, id=id)
    
#     def put(self, request, id):
#         return self.update(request, id=id)
#     def delete(self, request, id):
#         return self.destroy(request, id=id)

# class ArticleList(APIView):
#     def get(self, request):
#         articles = Article.objects.all()
#         serializer = ArticleSerializer(articles, many=True)
#         return Response(serializer.data)
    
#     def post(self, request):
#         serializer = ArticleSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class ArticleDetails(APIView):
#     def get_object(self, id):
#         try:
#             return Article.objects.get(id=id)
#         except Article.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
    
#     def get(self, request, id):
#         article = self.get_object(id)
#         serializer = ArticleSerializer(article)
#         return Response(serializer.data)
    
#     def put(self, request, id):
#         article = self.get_object(id)
#         serializer = ArticleSerializer(article, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, id):
#         article = self.get_object(id)
#         article.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(['GET','POST'])
# def article_list(request):
#     if request.method == "GET":
#         articles = Article.objects.all()
#         serializer = ArticleSerializer(articles, many=True)
#         return Response(serializer.data)
    
#     elif request.method == "POST":
#         serializer = ArticleSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET','PUT', 'DELETE'])
# def article_details(request, pk):
#     try:
#         article = Article.objects.get(pk=pk)
#     except Article.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == "GET":
#         serializer = ArticleSerializer(article)
#         return Response(serializer.data)
    
#     elif request.method == "PUT":
#         serializer = ArticleSerializer(article, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == "DELETE":
#         article.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
# '''




