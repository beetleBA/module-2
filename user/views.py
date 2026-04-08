from rest_framework import views
from rest_framework.response import Response
from recept.models import Recept
from user.serializers import ApiReceptSerializer, AuthSerializer, RegistrSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.core.paginator import Paginator


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


class ReceptsIdView(views.APIView):
    def get(self, request):
        pass
