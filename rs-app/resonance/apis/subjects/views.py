from rest_framework import generics
from rest_framework import authentication
from rest_framework import permissions

from subject.models import Subject

from .serializers import SubjectSerializer


class SubjectList(generics.ListAPIView):
	permission_classes = [permissions.IsAuthenticated]
	authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]
	serializer_class = SubjectSerializer
	queryset = Subject.objects.all()

