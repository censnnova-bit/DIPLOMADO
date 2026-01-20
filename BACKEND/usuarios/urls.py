from django.urls import path
from .views import login_view, logout_view

# Las rutas del ViewSet se manejan en el router principal
urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
