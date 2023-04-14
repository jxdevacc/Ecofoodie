from email.policy import default
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *


class UserSerializer(serializers.ModelSerializer):

    # token = serializers.SerializerMethodField()

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
        )

    username = serializers.CharField(
        required=True,
        max_length=32,
        validators=[UniqueValidator(queryset=User.objects.all())]
        )

    first_name = serializers.CharField(
        required=True,
        max_length=32,
        )

    last_name = serializers.CharField(
        required=True,
        max_length=32,
        )

    password = serializers.CharField(
        required=True,
        min_length=8,
        write_only=True
        )

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    # def get_token(self, obj):
    #     jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    #     jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    #     payload = jwt_payload_handler(obj)
    #     token = jwt_encode_handler(payload)
    #     return token

    class Meta:
        model=User
        fields = (
            # 'token',
            'username',
            'password',
            'first_name',
            'last_name',
            'email',
            'id'
            )



# class ProducerSerializer(serializers.ModelSerializer):

#     SSN = serializers.CharField(
#         required=True,
#         max_length = 9,
#         validators=[UniqueValidator(queryset=Producer.objects.all())]
#         )

#     avg_rating = serializers.DecimalField(
#         max_digits=3,
#         decimal_places=1
#         )

#     num_pickups = serializers.IntegerField(
#         default=0
#         )

#     email = UserSerializer(
#         required=True,
#         validators=[UniqueValidator(queryset=Producer.objects.all())]
#         )

#     def create(self, validated_data):
#         instance = self.Meta.model(**validated_data)
#         instance.save()
#         return instance

#     class Meta:
#         model=Producer
#         fields = (
#             # 'token',
#             'SSN',
#             'avg_rating',
#             'num_pickups',
#             'email',
#             )


# from rest_framework import serializers
# from .models import *
# from django.contrib.auth.models import User
# from django.views.decorators.csrf import csrf_exempt


# class ArticleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Article
#         fields = ['id','title','description']

# @csrf_exempt
# class CurrentUserSerializer(serializers.Serializer):
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password', 'id')






class ProducerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producer
        fields = ['email', 'SSN', 'avg_rating','num_pickups']

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id','header_text', 'body_text', 'produceremail','date_exp','city', 'street', 'state','country','zipcode', 'date_uploaded', 'recieveremail','group_directed', 'complete', 'oldreciever', 'date_finish']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'header_text', 'body_text', 'useremail', 'number_of_stars', 'date', 'post_id', 'produceremail']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'useremail', 'date_uploaded', 'admin']

