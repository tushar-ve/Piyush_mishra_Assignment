import openai
from rest_framework import generics
from .models import CustomUser
from .serializers import CustomUserSerializer, CustomTokenObtainPairSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

openai.api_key = 'your_openai_api_key'

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = CustomUserSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class ChatView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user_message = request.data.get('message')
        response = openai.Completion.create(
            engine="gpt-3.5-turbo",
            prompt=user_message,
            max_tokens=150
        )
        return Response({'response': response.choices[0].text.strip()}, status=status.HTTP_200_OK)

class ChatHistoryView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        chats = Chat.objects.filter(user=request.user).order_by('-timestamp')
        chat_history = [{"message": chat.message, "response": chat.response, "timestamp": chat.timestamp} for chat in chats]
        return Response(chat_history, status=status.HTTP_200_OK)