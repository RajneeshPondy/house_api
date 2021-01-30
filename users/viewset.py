from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework import viewsets, mixins

from users.serializers import UserSerializer, ProfileSerializer
from users.permissions import IsUserOwnerOrGetAndPostOnly, IsProfileOwnerOrReadOnly
from users.models import Profile


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        IsUserOwnerOrGetAndPostOnly,
    ]


class ProfileViewSet(
    viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin
):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsProfileOwnerOrReadOnly,]