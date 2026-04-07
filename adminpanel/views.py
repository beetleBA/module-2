from django.shortcuts import render, redirect
from django.urls.base import reverse
from rest_framework import views
from rest_framework.authentication import SessionAuthentication
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from adminpanel.serializer import AdminLoginSerializer, CategorySerializer, ReceptSerializer, StepsSerializer
from recept.models import Category, Recept, Step
from django.core.paginator import Paginator


def errors_field(serializer):
    errors = {}
    for f, e in serializer.errors.items():
        errors[f] = [str(i) for i in e]
    return errors


class AdminLoginView(views.APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        serializer = AdminLoginSerializer(data=request.data)
        if not serializer.is_valid():
            return render(request, 'login.html', {'errors': errors_field(serializer)})
        user = authenticate(
            email=request.data.get('email'),
            password=request.data.get('password'),
        )
        if user and user.is_superuser:
            login(request, user)
            return redirect(reverse('recept'))
        return render(request, 'login.html', {'error': 'Неверный логин или пароль'})


class AdminLogoutView(views.APIView):
    authentication_classes = [SessionAuthentication]

    def post(self, request):
        logout(request)
        return redirect(reverse('login'))


class AdminReceptsView(views.APIView):
    authentication_classes = [SessionAuthentication]

    def get(self, request):

        data = Recept.objects.all().order_by('title')
        sort_hours = request.GET.get('hours')
        if sort_hours:
            if sort_hours == 'asc':
                data = data.order_by('hours')
            else:
                data = data.order_by('-hours')
        paginator = Paginator(data, 5)
        page = request.GET.get('page', 1)
        page_obj = paginator.get_page(page)
        serializer = ReceptSerializer(page_obj, many=True)
        print(serializer.data)

        return render(request, 'recipes_list.html', {'data': serializer.data, 'page_obj': page_obj})


class AdminReceptsCreateView(views.APIView):
    authentication_classes = [SessionAuthentication]

    def get(self, request):
        category = Category.objects.all()
        serializer_category = CategorySerializer(category, many=True)
        return render(request, 'recipe_form.html', {'category': serializer_category.data})

    def post(self, request):
        category = Category.objects.all()
        serializer_category = CategorySerializer(category, many=True)
        serializer = ReceptSerializer(data=request.data)
        if not serializer.is_valid():
            print(serializer.errors)

            return render(request, 'recipe_form.html', {'errors': errors_field(serializer), 'category': serializer_category.data})

        serializer.save()
        return redirect(reverse('recept'))


class AdminReceptsEditView(views.APIView):
    authentication_classes = [SessionAuthentication]

    def get(self, request, id):
        category = Category.objects.all()
        serializer_category = CategorySerializer(category, many=True)

        data = get_object_or_404(Recept, id=id)
        serializer = ReceptSerializer(data)

        steps = Step.objects.filter(recept=data)
        serializer_steps = StepsSerializer(steps, many=True)

        return render(request, 'recipe_form.html', {'category': serializer_category.data, 'data': serializer.data, 'steps': serializer_steps.data})

    def post(self, request, id):
        data = get_object_or_404(Recept, id=id)
        category = Category.objects.all()
        serializer_category = CategorySerializer(category, many=True)

        files = request.FILES.getlist('photos')
        md = request.data.copy()
        if files:
            md.setlist('photos', files)
        else:
            md.pop('photos', None)

        serializer = ReceptSerializer(data, data=md, partial=True)
        if not serializer.is_valid():
            print(serializer.errors)

            return render(request, 'recipe_form.html', {'errors': errors_field(serializer), 'category': serializer_category.data, 'data': serializer.data})

        serializer.save()
        return redirect(reverse('recept'))


class AdminCategoriesView(views.APIView):
    authentication_classes = [SessionAuthentication]

    def get(self, request):
        data = Category.objects.all()
        serializer = CategorySerializer(data, many=True)
        return render(request, 'categories_list.html', {'category': serializer.data})


class AdminCategoriesCreateView(views.APIView):
    authentication_classes = [SessionAuthentication]

    def get(self, request):
        return render(request, 'category_form.html')

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if not serializer.is_valid():
            return render(request, 'category_form.html', {'errors': errors_field(serializer)})
        serializer.save()
        return redirect(reverse('categories'))


class AdminCategoriesDeleteView(views.APIView):
    authentication_classes = [SessionAuthentication]

    def post(self, request, id):
        category = get_object_or_404(Category, id=id)
        data = Recept.objects.filter(category=category).exists()
        if not data:
            category.delete()
        return redirect(reverse('categories'))


class AdminCategoriesEditView(views.APIView):
    authentication_classes = [SessionAuthentication]

    def get(self, request, id):
        data = get_object_or_404(Category, id=id)
        serializer = CategorySerializer(data)
        return render(request, 'category_form.html', {'data': serializer.data})

    def post(self, request, id):
        data = get_object_or_404(Category, id=id)
        serializer = CategorySerializer(data, data=request.data, partial=True)
        if not serializer.is_valid():
            return render(request, 'category_form.html', {'errors': errors_field(serializer)})
        serializer.save()
        return redirect(reverse('categories'))


class AdminReceptsDeleteView(views.APIView):
    authentication_classes = [SessionAuthentication]

    def post(self, request, id):
        data = get_object_or_404(Recept, id=id)
        print("sakd")
        if data.on_delete:
            data.delete()
        else:
            data.on_delete = True
            data.save()
        return redirect(reverse('recept'))


class AdminStepsView(views.APIView):
    authentication_classes = [SessionAuthentication]

    def get(self, request, id):
        return render(request, 'step_form.html', {'id': id})

    def post(self, request, id):
        print(request.data)
        serializer = StepsSerializer(data=request.data)

        if not request.FILES.get('photo'):
            return render(request, 'step_form.html', {
                'errors': {'photo': ['Фото обязательно при создании']},
                'data': request.data
            })

        if not serializer.is_valid():
            return render(request, 'step_form.html', {'errors': errors_field(serializer)})
        serializer.save()
        return redirect(reverse('recept-edit', kwargs={'id': id}))


class AdminStepsEditView(views.APIView):
    authentication_classes = [SessionAuthentication]

    def get(self, request, id, id_step):
        data = get_object_or_404(Step, id=id_step)
        serializer = StepsSerializer(data)
        return render(request, 'step_form.html', {'id': id, 'data': serializer.data})

    def post(self, request, id, id_step):
        data = get_object_or_404(Step, id=id_step)

        file = request.FILES.get('photo')
        md = request.data.copy()
        if file:
            md['photo'] = file
        else:
            md.pop('photo', None)

        serializer = StepsSerializer(data, data=md, partial=True)
        if not serializer.is_valid():
            print(serializer.errors)

            return render(request, 'step_form.html', {'errors': errors_field(serializer), 'data': serializer.data})

        serializer.save()
        return redirect(reverse('recept-edit', kwargs={'id': str(id)}))
