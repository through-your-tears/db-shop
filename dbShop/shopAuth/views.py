from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from .models import CustomUser, Job, Profile
from .serializers import *
from .permissions import IsAuthorOrReadOnly, IsDirector
from .renderers import CustomUserJSONRenderer
from .token_generators import generate_rt, generate_jwt


# Create your views here.


class RefreshView(APIView):
    """
    Refreshing old access token
    """
    permission_classes = (AllowAny,)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'refresh_token': openapi.Schema(type=openapi.TYPE_STRING, description='refresh_token'),
        },
        required=['refresh_token']
    ),
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'access_token': openapi.Schema(type=openapi.TYPE_STRING),
                    'refresh_token': openapi.Schema(type=openapi.TYPE_STRING)
                }
            ),
        }
    )
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            user = CustomUser.objects.get(refresh_token=refresh_token)
        except CustomUser.DoesNotExist:
            return Response({
                'error': 'User does not exist'
            }, status=status.HTTP_418_IM_A_TEAPOT)
        if refresh_token == user.refresh_token:
            user.refresh_token = generate_rt()
            user.save(update_fields=('refresh_token',))
            data = {
                    'access_token': generate_jwt(user.pk),
                    'refresh_token': user.refresh_token
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
    renderer_classes = (CustomUserJSONRenderer,)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='email - using like username'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='user password')
        }
    ),
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'email': openapi.Schema(type=openapi.TYPE_STRING),
                    'access_token': openapi.Schema(type=openapi.TYPE_STRING),
                    'refresh_token': openapi.Schema(type=openapi.TYPE_STRING)
                }
            ),
        }
    )
    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    renderer_classes = (CustomUserJSONRenderer,)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='email - using like username'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='user password')
        },
    ),
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'email': openapi.Schema(type=openapi.TYPE_STRING),
                    'access_token': openapi.Schema(type=openapi.TYPE_STRING),
                    'refresh_token': openapi.Schema(type=openapi.TYPE_STRING)
                }
            ),
        }
    )
    def post(self, request):
        user = request.data

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomUserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (CustomUserJSONRenderer,)
    serializer_class = CustomUserSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class JobViewSet(ModelViewSet):
    queryset = Job.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = JobSerializer
    pagination_class = LimitOffsetPagination


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)
    serializer_class = ProfileSerializer
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class NotificationViewSet(GenericViewSet):
    queryset = Notification.objects.all()
    permission_classes = (IsDirector,)
    serializer_class = NotificationSerializer
    pagination_class = LimitOffsetPagination


class WorkDayViewSet(ModelViewSet):
    queryset = WorkingDay.objects.all()
    permission_classes = (IsDirector,)
    serializer_class = WorkingDaySerializer
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class DayOffViewSet(ModelViewSet):
    queryset = DayOff.objects.all()
    permission_classes = (IsDirector,)
    serializer_class = DayOffSerializer
    pagination_class = LimitOffsetPagination


class VacationViewSet(ModelViewSet):
    queryset = Vacation.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)
    serializer_class = VacationSerializer
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
