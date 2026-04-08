from django.urls import path, include

from user.views import AuthView, RegisterView, ReceptsView, ReceptsIdView

urlpatterns = [
    path('registr', RegisterView.as_view()),
    path('auth', AuthView.as_view()),
    path('recepts', ReceptsView.as_view()),
    path('recepts/<int:id>', ReceptsIdView.as_view()),
]
