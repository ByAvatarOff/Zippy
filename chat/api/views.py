from chat.models import Message
from chat.api.serializers import MessageSerializer
from rest_framework import generics, permissions, status
from rest_framework import viewsets
from rest_framework.response import Response


class ChatListView(viewsets.ViewSet):
    """"""
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



# def message_list(request, sender=None, receiver=None):
#     """
#     List all required messages, or create a new message.
#     """
#     if request.method == 'GET':
#         messages = Message.objects.filter(sender_id=sender, receiver_id=receiver, is_read=False)
#         serializer = MessageSerializer(messages, many=True, context={'request': request})
#         for message in messages:
#             message.is_read = True
#             message.save()
#         return JsonResponse(serializer.data, safe=False)
#
#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = MessageSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)