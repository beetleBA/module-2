from rest_framework import serializers

from recept.models import Category, Recept, ReceptPhoto, Step


class AdminLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class ReceptPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceptPhoto
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    count_recept = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = '__all__'

    def get_count_recept(self, obj):
        return Recept.objects.filter(category=obj).count()


class ReceptSerializer(serializers.ModelSerializer):
    photos_list = serializers.SerializerMethodField()
    photos = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )
    status_display = serializers.CharField(
        source="get_status_display", read_only=True)
    category_display = CategorySerializer(source="category", read_only=True)
    formatted_time = serializers.SerializerMethodField(read_only=True)
    is_delete = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recept
        fields = '__all__'

    def validate_photos(self, photos_list):
        if photos_list is not None and len(photos_list) > 5:
            raise serializers.ValidationError("Макимум 5")
        return photos_list

    def validate_decription(self, decription):
        if (len(decription) < 50):
            raise serializers.ValidationError("Минимум 50 символов")
        return decription

    def get_is_delete(self, obj):
        if obj.on_delete:
            return f"На удаление"
        else:
            return f"Нет"

    def get_formatted_time(self, obj):
        minuts = obj.hours
        hours = minuts // 60
        mins = minuts % 60

        if hours == 0:
            return f"{minuts} мин."
        elif minuts == 0:
            return f"{hours} час"
        else:
            return f"{hours} час{'а' if hours > 1 else ''} {mins} минут"

    def get_photos_list(self, obj):
        return ReceptPhoto.objects.filter(recept=obj)

    def create(self, validated_data):
        photos = validated_data.pop('photos', [])
        recept = Recept.objects.create(**validated_data)

        if not photos:
            raise serializers.ValidationError("Мимимум 1 фото")

        for i in photos:
            ReceptPhoto.objects.create(recept=recept, photo=i)
        return recept

    def update(self, instance, validated_data):
        photos = validated_data.pop('photos', None)

        for a, v in validated_data.items():
            setattr(instance, a, v)
        instance.save()

        if photos is not None:
            old_photos = ReceptPhoto.objects.filter(recept=instance)
            for i in old_photos:
                i.photo.delete(save=False)
                i.delete()

            for i in photos:
                ReceptPhoto.objects.create(recept=instance, photo=i)
        return instance


class StepsSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(
        required=False
    )

    class Meta:
        model = Step
        fields = '__all__'

    def update(self, obj, validated_data):
        if 'photo' in validated_data:
            old = obj.photo
            obj = super().update(obj, validated_data)
            if old and old != obj.photo:
                old.delete(save=False)
        else:
            obj = super().update(obj, validated_data)

        return obj
