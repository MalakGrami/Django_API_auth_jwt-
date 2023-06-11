from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from users.models import User
from .serializers import UserSerializers
import jwt,datetime

# Create your views here.

class RegiterView(APIView):
    def  post(self,request):
        serializer=UserSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class loginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('user not found')
        if not user.check_password(password):
            raise AuthenticationFailed('incorrect password')
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        try:
            token = token.decode('utf-8')  # Appel à decode si disponible
        except AttributeError:
            pass
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response
    
class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('unauthenticated!')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])  # Specify the algorithm
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('unauthenticated!')

        user = User.objects.get(id=payload['id'])  # Use "id" instead of "payload['id']"
        serializer = UserSerializers(user)
        return Response(serializer.data)
    
class LogoutView(APIView):
    def post(self,request):
        response=Response()
        response.delete_cookie('jwt')
        response.data = {
            'message':'success'
        }
        return response