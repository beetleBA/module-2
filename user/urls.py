from django.urls import path, include

from user.views import AuthView, FavoriteViews, RegisterView, ReceptsView, ReceptsIdView, CategoryViews

urlpatterns = [
    path('registr', RegisterView.as_view()),
    path('auth', AuthView.as_view()),
    path('recepts', ReceptsView.as_view()),
    path('recepts/<int:id>', ReceptsIdView.as_view()),
    path('favorites', FavoriteViews.as_view()),
    path('category', CategoryViews.as_view()),
]
