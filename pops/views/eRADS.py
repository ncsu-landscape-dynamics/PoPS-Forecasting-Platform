from django.views.generic import TemplateView

from ..models import *
from ..forms import *

from users.models import CustomUser

class EradsDashboardView(TemplateView):
    template_name = 'pops/eRADS/eRADS_dashboard.html'
