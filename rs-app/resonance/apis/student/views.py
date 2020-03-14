from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import authentication
from rest_framework.response import Response

from .serializers import TOCSerializer, BaseTOCSerializer,DashboardSerializer
from content.views import render_response
from subject.models import TOC
from users.models import Student

class TOCDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    queryset = TOC.objects.all()
    serializer_class = BaseTOCSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = {"toc_data": serializer.data, "errors": [], "status": 1}
        data['current_open_toc_id'] = self.kwargs['pk']
        return Response(data)




class DashboardAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]

    def get(self, request, *args, **kwargs):
        student = Student.objects.filter(user=request.user).first()
        return render_response(data=DashboardSerializer(Student,many=False).data, error=[], status=1)
