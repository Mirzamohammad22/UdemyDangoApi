from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, filters
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated
from profiles_api import serializers, models, permissions

# Create your views here.


class HelloApiView(APIView):
    """ TEST API VIEW """
    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        an_apiview = [
            'Uses HTTP Methods as function',
            'hello world'
        ]
        return Response({'message': 'hi im a message', 'an_apiview': an_apiview})

    def post(self, request):
        """ Create a hello message with our name"""
        serializers = self.serializer_class(data=request.data)

        if serializers.is_valid():
            name = serializers.validated_data.get('name')
            message = f'Hello my friend {name}'
            return Response({
                "name": name,
                "message": message
            })
        else:
            return Response({
                "errors": serializers.errors,
                "status": status.HTTP_400_BAD_REQUEST
            })

    def put(self, request, pk=None):
        """ Handle updating an object """
        return Response({"method": "PUT"})

    def patch(self, request, pk=None):
        """ Handle partial update of an object """
        return Response({"method": "PUT"})

    def delete(self, request, pk=None):
        """Handle deleting an object """
        return Response({"method": "PUT"})


class HelloViewSet(ViewSet):
    """ TEST API VIEWSET """
    serializers_class = serializers.HelloSerializer

    def list(self, request):
        """ Return a Hello Message """

        a_viewset = [
            'Uses actions (list, create,retrieve,update,partial_update)',
            'Automatically maps to URLs using Routers',
            'Provides more functionality with less code',
        ]
        return Response({'message': 'Hello!', 'a_viewset': a_viewset})

    def create(self, request):
        """ Handle creating an object """
        serializers = self.serializers_class(data=request.data)

        if serializers.is_valid():
            name = serializers.validated_data.get('name')
            message = f'hello {name}'
            return Response({"message": message})
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """ Handle getting an object by its ID """
        return Response({"method": "GET"})

    def update(self, request, pk=None):
        """ Handle updating an object"""
        return Response({"method": "PUT"})

    def partial_update(self, request, pk=None):
        """ Handle partial updating an object"""
        return Response({"method": "PATCH"})

    def destroy(self, request, pk=None):
        """ Handle removing an object """
        return Response({"method": "Delete"})


class UserProfileViewSet(ModelViewSet):
    """ Handle creating and updating profiles"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)


class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserProfileFeedViewSet(ModelViewSet):
    """Handles creating, reading and updating profile feed items """
    serializer_class = serializers.ProfileFeedItemSerializer
    authentication_classes = (TokenAuthentication,)
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes =(
        permissions.UpdateOwnStatus,
        IsAuthenticated
    )

    def perform_create(self, serializer):
        """ Sets the user profile to the logged in user """
        serializer.save(user_profile=self.request.user)
    



