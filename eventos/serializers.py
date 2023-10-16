from rest_framework import serializers
from .models import Evento, Usuario
from collections import OrderedDict

class EventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = '__all__'  # Esto incluirá todos los campos del modelo en el serializador

class UsuarioSerializer(serializers.ModelSerializer):

    password_confirmation = serializers.CharField(write_only=True)  # Campo para la confirmación de contraseña

    class Meta:
        model = Usuario
        fields = ('username', 'email', 'password', 'password_confirmation')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        validated_data.pop('password_confirmation', None)
        return Usuario.objects.create_user(**dict(validated_data))
    
    def validate(self, attrs: OrderedDict):
        if attrs.get('password') is None or attrs.get('password') != attrs.get('password_confirmation'):
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs