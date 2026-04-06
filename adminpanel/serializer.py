from rest_framework import serializers

from recept.models import Category, Recept, ReceptPhoto


class AdminLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class ReceptPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceptPhoto
        fields = '__all__'


class ReceptSerializer(serializers.ModelSerializer):
    photos_list = serializers.SerializerMethodField()
    photos = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True
    )

    class Meta:
        model = Recept
        fields = '__all__'

    def validate_decription(self, decription):
        if (len(decription) < 50):
            raise serializers.ValidationError("Минимум 50 символов")
        return decription
    
    def get_photos_list(self, obj):
        return ReceptPhoto.objects.filter(recept=obj)

    def create(self, validated_data):
        photos = validated_data.pop('photos', [])
        recept = Recept.objects.create(**validated_data)

        for i in photos:
            ReceptPhoto.objects.create(recept=recept, photo=i)
        return recept


class CategorySerializer(serializers.ModelSerializer):
    count_recept = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = '__all__'

    def get_count_recept(self, obj):
        return Recept.objects.filter(category=obj).count()
