from rest_framework import serializers
from django.contrib.auth import get_user_model

from adminpanel.serializer import CategorySerializer
from recept.models import Recept, ReceptPhoto

User = get_user_model()


class RegistrSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate_email(self, email):
        user = User.objects.filter(email=email).exists()
        if user:
            raise serializers.ValidationError("Пользователь уже существует")
        return email

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class AuthSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class ApiReceptSerializer(serializers.ModelSerializer):
    cooking_time = serializers.CharField(source='hours')
    difficulty = serializers.CharField(source='get_status_display')
    category = CategorySerializer()
    formatted_time = serializers.SerializerMethodField()
    default_image = serializers.SerializerMethodField()

    class Meta:
        model = Recept
        fields = ['id', 'title', 'decription', 'cooking_time',
                  'difficulty', 'price', 'category', 'formatted_time', 'default_image']

    def get_formatted_time(self, obj):
        minute = obj.hours
        hours = minute // 60
        mins = minute % 60

        if hours == 0:
            return f"{mins} мин."
        elif mins == 0:
            return f"{hours} ч."
        else:
            return f"{hours} ч. {mins} мин."

    def get_default_image(self, obj):
        photo = ReceptPhoto.objects.filter(recept=obj).first()
        return photo.photo.url if photo else ''
