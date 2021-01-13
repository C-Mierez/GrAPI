from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
from .models import User
from django.http.response import Http404
from django.db import transaction

from rest_framework.exceptions import ValidationError
    
class UserList(APIView):
    # authentication_classes = []
    permission_classes = [IsAdminUser]
    
    serializer_class = UserSerializer
    
    def get(self, request, format=None):
        """
        Lista de todos los usuarios
        """
        users = User.objects.all()
        serializer = self.serializer_class(users, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request, format=None):
        """
        Creacion de un usuario
        """
        serializer = self.serializer_class(data=request.data, many=False, context={'request': request})
        if serializer.is_valid():
            
            with transaction.atomic():
                serializer.save(created_by=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

class UserDetail(APIView):
    # authentication_classes = []
    permission_classes = [IsAdminUser]
    
    serializer_class = UserSerializer
    
    def get(self, request, pk, format=None):
        users = get_object_or_404(User, pk=pk)        
        serializer = self.serializer_class(users, many=False, context={'request': request})
        return Response(serializer.data)
    
    def patch(self, request, pk, format=None):
        user = get_object_or_404(User, pk=pk)
        serializer = self.serializer_class(user, data=request.data, many=False, partial=True, context={'request': request}) # set partial=True to update a data partially
        if serializer.is_valid():
            serializer.save(updated_by=request.user)
            if getattr(user, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                user._prefetched_objects_cache = {}
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Hacer un PUT seria en realidad lo que hace el Patch pero cambiando partial=True
    
    
    def delete(self, request, pk, format=None):
        user = get_object_or_404(User, pk=pk)
        with transaction.atomic():
            user.delete(user=request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)










@api_view(http_method_names=['GET', 'POST'])
@permission_classes([AllowAny])
def test_view(request, format=None):
    print(request.user)
    print(request.auth)
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True, context={'request': request})
        return JsonResponse(serializer.data, safe=False)
    
    elif request.method == 'POST':
        # data = JSONParser().parse(request)
        serializer = UserSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    