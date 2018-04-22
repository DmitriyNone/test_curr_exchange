from django.contrib.auth.models import User, Group
from rest_framework import serializers
from quickstart.models import Currencies

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class CurrenciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Currencies
        fields = ('id', 'timestamp', 'usd', 'eur', 'czk', 'pln')

    def create(self, validated_data):
        """
        Create and return a new `curr_rates` instance, given the validated data.
        """
        return Currencies.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `curr_rates` instance, given the validated data.
        """
        instance.timestamp = validated_data.get('timestamp', instance.timestamp)
        instance.usd = validated_data.get('usd', instance.usd)
        instance.eur = validated_data.get('eur', instance.eur)
        instance.czk = validated_data.get('czk', instance.czk)
        instance.pln = validated_data.get('pln', instance.pln)
        instance.save()
        return instance
