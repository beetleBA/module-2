from django.contrib import admin
from django.urls import path

from adminpanel.views import AdminLoginView, AdminReceptsView, AdminCategoriesEditView, AdminCategoriesDeleteView, AdminCategoriesCreateView, AdminCategoriesView, AdminLogoutView, AdminReceptsCreateView

urlpatterns = [
    path('login/', AdminLoginView.as_view(), name='login'),
    path('recept/', AdminReceptsView.as_view(), name='recept'),
    path('recept/create', AdminReceptsCreateView.as_view(), name='recept-create'),
    path('logout/', AdminLogoutView.as_view(), name='logout'),
    path('categories/', AdminCategoriesView.as_view(), name='categories'),
    path('categories/<int:id>/delete',
         AdminCategoriesDeleteView.as_view(), name='categories-delete'),
    path('categories/<int:id>/edit',
         AdminCategoriesEditView.as_view(), name='categories-edit'),
    path('categories/create', AdminCategoriesCreateView.as_view(),
         name='categories-create'),
]
