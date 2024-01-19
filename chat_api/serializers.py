from rest_framework import serializers
from chat_api.models import ChatResponse

class ChatResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatResponse
        fields = ['explanation','solution','code']
        