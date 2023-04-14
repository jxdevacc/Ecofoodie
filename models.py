from asyncio.windows_events import NULL
from django.db import models
from django.contrib.auth.models import User

# from django.forms import ModelForm
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import AbstractUser
# from django.views.decorators.csrf import csrf_exempt
# from api.models import CustomUser

# #from phonenumber_field.modelfields import PhoneNumberField
# # Create your models here.  

# class Article(models.Model):
#     title = models.CharField(max_length=100)
#     description = models.TextField()

#     def __str__(self):
#         return self.title

# @csrf_exempt
# class User(AbstractUser):
#     name = models.CharField(max_length=200, null=True)
#     email = models.EmailField(unique=True, null=True)
#     bio = models.TextField(null=True)

#     avatar = models.ImageField(null=True, default="avatar.svg")

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []
#     class Meta:
#         app_label = 'api'


# csrf_exempt
# class UserForm(ModelForm):
#     class Meta:
#         model = User
#         fields = ['avatar', 'name', 'username', 'email', 'bio']

# @csrf_exempt
# class Create(UserCreationForm):
#     class Meta (UserCreationForm.Meta):
#         model = CustomUser
#         fields = ['email', 'username', 'password']

class Producer(models.Model):
    SSN = models.CharField(max_length=9)
    avg_rating = models.DecimalField(max_digits=3, decimal_places=1)
    num_pickups = models.IntegerField(default = 0)
    email = models.EmailField(primary_key = True)
    # email = models.ForeignKey(User, primary_key = True, on_delete= models.CASCADE)

    def __str__(self):
        return self.email

class Post(models.Model):
    header_text = models.CharField(max_length = 20)
    body_text = models.TextField()
    produceremail = models.EmailField()
    date_exp = models.CharField(max_length = 50)
    city = models.CharField(max_length = 50)
    street = models.CharField(max_length = 30)
    state = models.CharField(max_length = 50)
    country = models.CharField(max_length = 50)
    zipcode = models.CharField(max_length = 10)
    date_uploaded = models.DateTimeField(auto_now_add = True, blank = True, null = True)
    recieveremail = models.EmailField(blank = True, null = True)
    group_directed = models.BooleanField(default=False)
    complete = models.CharField(default= "No", max_length = 4)
    oldreciever = models.EmailField(blank = True, null = True)
    date_finish = models.CharField(default = '', blank = True, null = True, max_length = 50)
    def __str__(self):
        return self.header_text

class Review(models.Model):
    header_text = models.CharField(max_length = 20)
    body_text = models.TextField()
    useremail = models.EmailField()
    number_of_stars = models.CharField(max_length = 6)
    date = models.CharField(max_length = 50)
    post_id = models.CharField(max_length = 30)
    produceremail = models.EmailField(default="")

    def __str__(self):
        return self.header_text


class Group(models.Model):
    useremail = models.EmailField()
    date_uploaded = models.DateTimeField(auto_now_add = True, blank = True, null = True)
    admin = models.EmailField()

    def __str__(self):
        return self.useremail


#         {
# "header_text" : "help",
#     "body_text" : "alsdfsdfsdfs",
#     "produceremail" : "sncantu@yahoo.com",
#     "date_exp" : "1234",
#     "city" : "alsdjf",
#     "street" : "lksjaf",
#     "state" : "asdfa",
#     "country" : "usa",
#     "zipcode" : "87678",
#     "date_uploaded" : "909",
#     "recieveremail" : "sncantu2018@gmail.com"
# }