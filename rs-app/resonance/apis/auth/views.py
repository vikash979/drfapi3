from django.contrib.auth import logout


from rest_framework import generics
from rest_framework import status

from rest_framework.views import View
from rest_framework.response import Response

from rest_framework import authentication

from rest_framework import permissions
from rest_framework import views
from rest_framework.authtoken.models import Token
from users.models import User
from .serializers import LoginSerializer, UserSerializer
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework import serializers

class UserListViewAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    def get_token_function(self, user=None, model=Token):
        return model.objects.get_or_create(user=user)

    def get(self, reqeust, *args, **kwargs):
        context_data = {
            'password': 'python@123',
        }
        for i in User.objects.all():
            context_data["username: {user}, role: {role}".format(user=self.get_token_function(i)[0].user, role=self.get_token_function(i)[0].user.get_role_display())] = self.get_token_function(i)[0].key
        return Response(context_data)

class LoginView(views.APIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        status = 0
        errors = []
        data = {}
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user:
                data = UserSerializer(user).data
                status = 1
            else:
                errors.append("username or password is not correct")
        else:
            validation_errors = []
            for k in serializer.errors:
                # print(str(serializer.errors.get(k)[0]))
                validation_errors.append("{}: {}".format(k,serializer.errors.get(k)[0]))
            # serializer.errors
            errors = validation_errors


        return Response({"status": status, 'data':data, "errors": errors})


class LogoutView(views.APIView):
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()

    def get_auth_token_header(self, request):
        get_token = request.META.get('HTTP_AUTHORIZATION', None)
        if get_token:
            _, token = get_token.split()
            return token
        return None

    def delete_token(self, token_value, model=Token):
        model.objects.filter(key=token_value).delete()
        return True

    def get(self, request, *args, **kwargs):
        self.post(request,args,kwargs)

    def post(self, request, *args, **kwargs):
        token = self.get_auth_token_header(request)
        if not token:
            return Response({"data": {}, "errors": ["Please provide auth_token"], "status": 0})

        if self.delete_token(token):
            logout(request)
            data = {'success': 'Sucessfully logged out'}
            errors = []
        return Response({"data": data, "errors": errors, "status": 1}, status=status.HTTP_200_OK)
