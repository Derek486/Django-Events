from django.urls import path
from django.contrib.auth import views as authViews
from . import views

urlpatterns = [
    path('login/', view=authViews.LoginView.as_view(template_name='pages/auth/login.html'), name='eventos.login'),
    path('logout/', view=authViews.LogoutView.as_view(), name='eventos.logout'),
    path('register/', view=views.RegisterApi.as_view(
        {
            'get':'register_index',
            'post': 'register'
        }), name='eventos.register'),
    path('profile/<int:id>', view=views.ProfileView.as_view(
        {
            'get': 'index'
        }), name='eventos.profile'),
    path('profile/', view=views.ProfileView.as_view(
        {
            'get': 'index'
        }), name='eventos.profile'),
    path('', view=views.EventosApi.as_view({'get':'index'}), name='eventos.index'),
    path('<int:id>', view=views.EventosApi.as_view(
        {
            'get': 'show',
            'post': 'update'
        }), name='eventos.update'),
    path('create/', view=views.EventosApi.as_view(
        {
            'get':'create',
            'post': 'store'
        }), name='eventos.create'),
    path('<int:id>/delete', view=views.EventosApi.as_view(
        {
            'get': 'destroy',
        }), name='eventos.destroy'),
    path('<int:id>/participar', view=views.ParticipacionesApi.as_view(
        {
            'post': 'store'
        }), name='participacion.store'),
    path('<int:id>/abandonar/<int:user>', view=views.ParticipacionesApi.as_view(
        {
            'post': 'destroy'
        }), name='participacion.destroy'),
]