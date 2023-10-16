from django.shortcuts import render, redirect
from django.contrib.auth import login
from rest_framework.viewsets import ViewSet
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import *
from .serializers import *

class RegisterApi(ViewSet):
    permission_classes = [AllowAny]

    def register_index(self, request, *args, **kwargs):
        return render(request, 'pages/auth/register.html')

    def register(self, request, *args, **kwargs):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.create(serializer.validated_data)
            login(request, user)
            return redirect(to='eventos.index')
        else:
            errors = {
                'errors': serializer.errors
            }
            return render(request, 'pages/auth/register.html', context=errors)

class EventosApi(ViewSet):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def index(self, request, *args, **kwargs):
        eventos = Evento.objects.all()
        orden = request.GET.get('order_by')
        request.session['order_asc'] = not request.session['order_asc'] if 'order_asc' in request.session else True
        if orden is not None:
            if request.session['order_asc']: # switch asc | desc
                orden = '-' + orden
            eventos = eventos.order_by(orden)
        organizadores = Usuario.objects.exclude(pk=request.user.id).filter(eventos_creados__isnull=False).distinct()
        context = {
            'eventos': eventos,
            'organizadores': organizadores,
        }
        return render(request, 'pages/eventos/eventos.html', context=context)
    
    def create(self, request, *args, **kwargs):
        return render(request, 'pages/eventos/create_evento.html')
    
    def store(self, request, *args, **kwargs):
        data = request.data.copy()
        data['autor'] = request.user.id
        serializer = EventoSerializer(data=data)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            return redirect(to='eventos.profile')
        else:
            errors = {
                'errors': serializer.errors
            }
            return render(request, 'pages/eventos/create_evento.html', context=errors, status=409)
    
    def show(self, request, id, *args, **kwargs):
        evento = Evento.objects.get(pk=id)
        registros = RegistroEvento.objects.filter(evento=evento)
        context = {
            'evento': evento,
            'registros': registros.all(),
            'participando': registros.filter(usuario=request.user).exists()
        }
        return render(request, 'pages/eventos/show_evento.html', context=context)

    def update(self, request, id, *args, **kwargs):
        data = request.data.copy()
        data["autor"] = request.user.id
        if data["portada"] == "": del data["portada"]
        serializer = EventoSerializer(data=data)
        evento = Evento.objects.get(pk=id)
        registros = RegistroEvento.objects.filter(evento=evento)
        
        if serializer.is_valid():
            serializer.update(evento, serializer.validated_data)
            return redirect(to=f'/eventos/{id}')
        else:
            context = {
                "errors": serializer.errors,
                "evento": evento,
                "registros": registros.all(),
                "participando": registros.filter(usuario=request.user).exists()
            }
            return render(request, 'pages/eventos/show_evento.html', context=context, status=409)
    
    def destroy(self, request, id, *args, **kwargs):
        evento = Evento.objects.get(pk=id)
        if evento.autor == request.user:
            evento.delete()
        return redirect(to='eventos.profile')
    
        
class ParticipacionesApi(ViewSet):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def store(self, request, id, *args, **kwargs):
        evento = Evento.objects.get(pk=id)
        if evento.autor != request.user and not evento.participantes.contains(request.user):
            evento.participantes.add(request.user)

        return redirect(to=f'/eventos/{id}')

    def destroy(self, request, id, user, *args, **kwargs):
        usuario = Usuario.objects.get(pk=user)
        evento = Evento.objects.get(pk=id)
        if (request.user in [usuario, evento.autor]) and evento.participantes.contains(usuario):
            evento.participantes.remove(usuario)
        return redirect(to=f'/eventos/{id}')

class ProfileView(ViewSet):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def index(self, request, id = None, *args, **kwargs):
        autor = request.user if id is None else Usuario.objects.get(pk=id)
        eventos = autor.eventos_creados.all()
        orden = request.GET.get('order_by')
        request.session['order_asc'] = not request.session['order_asc'] if 'order_asc' in request.session else True
        if orden is not None:
            if request.session['order_asc']: # switch asc | desc
                orden = '-' + orden
            eventos = eventos.order_by(orden)
        organizadores = Usuario.objects.exclude(pk=request.user.id).filter(eventos_creados__isnull=False).distinct()
        context = {
            'eventos': eventos,
            'autor': autor,
            'organizadores': organizadores
        }
        return render(request, 'pages/perfiles/perfil.html', context=context)