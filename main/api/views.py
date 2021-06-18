from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework import viewsets
from main.api.serializers import ProfileSerializer, UpdateProfileSerializer,\
    UpdateLocationProfileSerializer, CreateAddContentSerializer, AddContentSerializer,\
    CreateLikeSerializer
from main.api import service
from main.models import Profile, AddContent, Like


class ProfileViewSet(viewsets.ViewSet):
    """
    Class for view model Profile used viewsets
    """
    permission_classes = [permissions.IsAuthenticated, ]

    def list(self, request):
        queryset = Profile.objects.all()
        serializer = ProfileSerializer(queryset, many=True)
        return Response(serializer.data)
        # return service.filter_group(request=self.request)

    def retrieve(self, request):
        queryset = Profile.objects.get(user__username=request.user)
        serializer = ProfileSerializer(queryset)
        return Response(serializer.data)

    def partial_update(self, request):
        instance = Profile.objects.get(user__username=request.user)
        serializer = UpdateProfileSerializer(instance, data=request.data, partial=True)
        # instance.geo_location = service.get_location()
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class AddContentViewSet(viewsets.ViewSet):
    """
    Class for view content user
    """
    permission_classes = [permissions.IsAuthenticated, ]

    def list(self, request):
        queryset = AddContent.objects.filter(profile=Profile.objects.get(user=request.user))
        serializer = AddContentSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        # instance = AddContent.objects.all()
        serializer = CreateAddContentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(profile=Profile.objects.get(user=request.user))
        return Response(serializer.data)


class AddContentCreateView(generics.CreateAPIView):
    queryset = AddContent.objects.all()
    serializer_class = CreateAddContentSerializer

    def perform_create(self, serializer):
        serializer.save(profile=Profile.objects.get(user=self.request.user))


class LikeViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = Like.objects.all()

    def create(self, request):
        try:
            if Like.objects.get(user=self.request.user, profile=Profile.objects.get(pk=self.request.POST.get('profile'))):
                return Response(status=status.HTTP_202_ACCEPTED)
        except Like.DoesNotExist:
            serializer = CreateLikeSerializer(self.queryset)
            service.match(request=self.request, pk=self.request.data['profile'])
            return Response(serializer.data)


class CreateLikeView(generics.CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = CreateLikeSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        try:
            if Like.objects.get(user=self.request.user, profile=Profile.objects.get(pk=self.request.POST.get('profile'))):
                return Response(status=status.HTTP_202_ACCEPTED)
        except Like.DoesNotExist:
            return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        service.match(request=self.request, pk=self.request.data['profile'])











