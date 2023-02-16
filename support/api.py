from django.db.models import query
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import SuportRequestModelSerializer
from .models import SupportRequestModel
from django_q.tasks import async_task

class ListCreateSupportRequest(ListCreateAPIView):
    """
    Allow owners and their tenants to list and create support
    requests 
    """
    
    permission_classes = [IsAuthenticated]
    serializer_class = SuportRequestModelSerializer

    def get_queryset(self):
        queryset = SupportRequestModel.objects.filter(user = self.request.user).order_by('-updated_at')
        return queryset

    def perform_create(self, serializer):
        # async task send email
        subject = serializer.validated_data.get("subject")
        email = serializer.validated_data.get("email")
        request = serializer.validated_data.get("request")
        user = self.request.user
        async_task('workers.utils.send_email', subject=subject, plain_text= request, recipient = email)
        serializer.save(user = user)
        
    
        
        

