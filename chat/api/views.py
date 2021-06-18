from chat.models import Message
from django.contrib.auth.models import User
from chat.api.serializers import MessageSerializer, UserSerializer
from rest_framework import generics, permissions, status
from rest_framework import viewsets
from rest_framework.response import Response


class MessageView(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated, ]

    def list(self, request, sender=None, receiver=None):
        """
        View messages sender with receiver <int:sender> <int:receiver>
        :param request:
        :param sender:
        :param receiver:
        :return:
        """
        queryset = Message.objects.filter(sender_id=sender, receiver_id=receiver, is_read=False)
        serializer = MessageSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ChatView(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated, ]

    def list(self, request):
        queryset = User.objects.exclude(username=request.user.username)
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    # def retrieve(self, request, sender, receiver):
    #     queryset = Message.objects.filter(sender_id=sender, receiver_id=receiver)
    #     serializer = MessageSerializer(queryset, many=True)
    #     return Response(serializer.data)




