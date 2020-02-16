from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import Album, Track

from .serializers import AlbumSerializer #, AlbumPKSerializer


class AlbumAPIView(APIView):

    permission_classes = [IsAuthenticated]
    #authentication_classes = [TokenAuthentication]

    def get(self, request, format=None):

        albums = Album.objects.all()
        serializer = AlbumSerializer(instance=albums, many=True)
        #serializer = AlbumPKSerializer(instance=albums, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = AlbumSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
