from rest_framework import views
from rest_framework.response import Response
from adminpanel.serializer import CategorySerializer, ReceptSerializer
from recept.models import Category, Favorite, Recept
from user.serializers import ApiReceptSerializer, AuthSerializer, RegistrSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404


class RegisterView(views.APIView):
    permission_classes = []

    def post(self, request):
        serializer = RegistrSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=403)
        serializer.save()
        return Response({"success": True}, status=201)


class AuthView(views.APIView):
    permission_classes = []

    def post(self, request):
        serializer = AuthSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=403)
        user = authenticate(
            email=request.data.get('email'),
            password=request.data.get('password')
        )
        if user and user.role == 'user':
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=200)

        return Response({"message": "Invalid"}, status=400)


class ReceptsView(views.APIView):
    def get(self, request):
        data = Recept.objects.all()
        paginator = Paginator(data, 5)
        page = request.GET.get('page', 1)
        page_obj = paginator.get_page(page)
        serializer = ApiReceptSerializer(page_obj, many=True)
        return Response({'data': serializer.data, 'paginator': {'current_page': page, 'total': paginator.num_pages, 'per_page': 5}}, status=200)

    def post(self, request):
        files = request.FILES.getlist('photos')
        md = request.data.copy()
        if files:
            md.setlist('photos', files)
        else:
            md.pop('photos', None)

        serializer = ReceptSerializer(data=md)
        if not serializer.is_valid():
            return Response({'error': serializer.errors}, status=403)
        data = serializer.save()
        return Response({'data': data}, status=403)


class ReceptsIdView(views.APIView):
    def get(self, request):
        pass


class FavoriteViews(views.APIView):
    def post(self, request):
        if 'recipe_id' not in request.data:
            return Response({"нет recipe_id"})

        recipe_id = request.data['recipe_id']

        exists = Recept.objects.filter(id=recipe_id).exists()
        if not exists:
            return Response({'Рецепта нет'})
        data = get_object_or_404(Recept, id=recipe_id)

        recept_like = Favorite.objects.filter(
            user=request.user, recept=recipe_id).exists()

        if data and recept_like:
            return Response({"message": "Recipe already in favorites"
                             }, status=409)
        if data:
            Favorite.objects.create(user=request.user, recept=data)
            return Response({"success": True, "message": "Recipe added to favorites"}, status=201)

        return Response({"message": "Recipe not found"}, status=404)

    def delete(self, request):
        pass


class CategoryViews(views.APIView):
    def get(self, request):
        data = Category.objects.all()
        serialiser = CategorySerializer(data, many=True)
        return Response(serialiser.data)
