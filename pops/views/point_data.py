from django.views.generic import FormView, ListView, DetailView, TemplateView, CreateView, UpdateView, View, DeleteView
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import UserPassesTestMixin

from django.http import JsonResponse, HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie

from django.db.models.functions import Greatest
from django.db.models import Prefetch, Sum, Count, Exists, Max, Min, OuterRef, Subquery, Q

from ..models import *
from ..forms import *

from users.models import CustomUser

class PointDataView(ListView):

    model = Point
    context_object_name = 'points'
    #paginate_by = 10  # if pagination is desired
    template_name = 'pops/point_data.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
