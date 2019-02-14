from rest_framework import viewsets
from rest_framework import permissions

from ..models import *
from ..serializers import *

class CaseStudyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = CaseStudy.objects.all()
    serializer_class = CaseStudySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)



