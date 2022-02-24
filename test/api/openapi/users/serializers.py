from rest_framework import serializers

from users.models import User, Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'number', 'street', 'city', 'state', 'zip']


class UserSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = User
        fields = ['id', 'first_name', 'middle_name', 'last_name', 'date_of_birth', 'email', 'phone', 'address']

    def create(self, validated_data):
        address_dict = validated_data.pop('address', None)
        user = User.objects.create(**validated_data)

        if address_dict:
            address = Address.objects.create(**address_dict)
            address.save()
            user.address = address

        user.save()

        return user

    def update(self, instance, validated_data):
        if 'address' not in validated_data:
            return

        instance.address.update(**validated_data.pop('address'))
        instance.save()

        return instance
