from account.models import User
from rest_framework import serializers
from rest_framework import status
import django.contrib.auth.password_validation as validators
from django.core.exceptions import ValidationError

class RegistrationSerializer(serializers.ModelSerializer):
    confirmation_password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('email','password','confirmation_password')

    def validate(self, attrs):
        if attrs['password'] != attrs['confirmation_password']:
            raise serializers.ValidationError({'detail':'Passwords must match'})
        try:
            validators.validate_password(attrs['password'])
        except ValidationError as e:
            raise serializers.ValidationError({'detail':list(e.messages)})
        return self.validate(attrs)

    def create(self, validated_data):
        validated_data.pop('password1',None)
        return User.objects.create_user(**validated_data)

