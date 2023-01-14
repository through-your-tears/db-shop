from django.contrib.auth import authenticate

from rest_framework import serializers

from .models import *
from .token_generators import generate_rt


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    access_token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'access_token', 'refresh_token']

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):

    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, attrs):

        email = attrs.get('email', None)
        password = attrs.get('password', None)

        if email is None:
            raise serializers.ValidationError(
                str(attrs)
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in'
            )

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found'
            )

        user.refresh_token = generate_rt()
        user.save(update_fields=('refresh_token',))

        return {
            "email": email,
            'access_token': user.access_token,
            'refresh_token': user.refresh_token
        }


class CustomUserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'is_staff', 'role', 'password')
        read_only_fields = ('is_staff',)

    def update(self, instance, validated_data):

        password = validated_data.pop('password', None)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance


class JobSerializer(serializers.ModelSerializer):

    class Meta:
        model = Job
        fields = ('title', 'salary')


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Profile
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Notification
        fields = ('user', 'text', 'confirmed')


class WorkingDaySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = WorkingDay
        fields = ('user', 'today', 'start_day', 'end_day')


class DayOffSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = DayOff
        fields = ('user', 'date')


class VacationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Vacation
        fields = '__all__'

    def validate(self, attrs):
        delta = (attrs['end'] - attrs['start']).days
        if delta > 28:
            raise serializers.ValidationError("Отпуск не может быть больше 28 дней")
        elif delta < 0:
            raise serializers.ValidationError("Отпуск не может закончиться раньше начала")
        return attrs
