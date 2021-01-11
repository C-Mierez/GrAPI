from django.shortcuts import render
from .models import User
from .serializers import UserSerializer
from rest_framework import viewsets
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.http import  JsonResponse
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    permission_classes = [IsAdminUser]
    
    def retrieve(self, request, pk=None):
        print('ESTOY EN EL RETRIEVE JAJAJFJDS,JKFHJSKFHJSDJF')
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)
        

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
    