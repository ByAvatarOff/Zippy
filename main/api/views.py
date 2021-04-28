from rest_framework import generics, permissions, status
from rest_framework.response import Response
from main.api.serializers import ProfileSerializer, UpdateProfileSerializer,\
    UpdateLocationProfileSerializer, CreateAddContentSerializer, AddContentSerializer,\
    CreateLikeSerializer
from main.api import service
from main.models import Profile, AddContent, Like


class ProfileListView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_queryset(self):
        return service.filter_group(request=self.request)


class ProfileUpdateView(generics.UpdateAPIView):
    queryset = ProfileListView
    serializer_class = UpdateProfileSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class AddContentCreateView(generics.CreateAPIView):
    queryset = AddContent.objects.all()
    serializer_class = CreateAddContentSerializer

    def perform_create(self, serializer):
        serializer.save(profile=Profile.objects.get(user=self.request.user))


class AddContentListView(generics.ListAPIView):
    queryset = AddContent.objects.all()
    serializer_class = AddContentSerializer
    permission_classes = [permissions.IsAuthenticated, ]


class UpdateLocation(generics.RetrieveUpdateAPIView):
    queryset = ''
    serializer_class = UpdateLocationProfileSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.geo_location = service.get_location()
        instance.save()
        return Response(status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


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
        service.match(request=self.request, pk=self.request.data['profile'])
        serializer.save(user=self.request.user)








