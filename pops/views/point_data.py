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
from django.forms import modelform_factory

from ..models import *
from ..forms import *

from users.models import CustomUser

from django.contrib.gis.geos import Point as Pnt
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.utils import LayerMapping


class PointDataView(CreateView):

    model = Point
    context_object_name = 'points'
    #paginate_by = 10  # if pagination is desired
    template_name = 'pops/point_data.html'
    form_class = PointDataForm


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        points = Point.objects.all()
        context['points'] = points
        return context

    def get(self, request,*args, **kwargs):
        return super().get(request,*args, **kwargs)

    def post(self, request,*args, **kwargs):
        print(request.POST)
        print('POST SUCCESS')
        latitude=float(request.POST.get('latitude'))
        print(latitude)
        longitude=float(request.POST.get('longitude'))
        print(longitude)
        count = float(request.POST.get('count'))
        pnt = Pnt(latitude,longitude)
        print(pnt)
        pnt.srid = 4326
        print(pnt)
        #my_forms={}
        new_entry = Point(count=count, point=pnt)  
        print(new_entry)
        new_entry.save()
        print(new_entry)
        #my_forms['form'] = PointDataForm(post_data, file_data)
        #my_forms['form'].point = pnt
        #form = PointDataForm(request.POST)
        #print(my_forms['form'])
        return super().post(request,*args, **kwargs)

class ShapeFileUploadView(CreateView):

    model = PointDataFiles
    fields = ['user_file']
    template_name = 'pops/shape_file_upload.html'
    success_url = reverse_lazy('shape_file_upload')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        points = Point.objects.all()
        context['points'] = points
        return context

    def get(self, request,*args, **kwargs):
        return super().get(request,*args, **kwargs)

    def form_valid(self, form):
        # super of form_valid saves the form to the database (if it is valid)
        # here we are saving the response to return after we do stuff with the file contents
        response = super(ShapeFileUploadView, self).form_valid(form)
        # self.object is the newly uploaded file
        print(self.object)
        location_inside_media_folder = self.object.user_file
        print(location_inside_media_folder)
        file_location = self.object.user_file.url
        file_location_without_leading_slash = file_location[1:]
        print(file_location)
        ds = DataSource(file_location_without_leading_slash)
        print(ds)
        layer=ds[0]
        print(layer.fields)
        print(layer.srs)
        print(layer.geom_type)
        point_data_mapping = {            
            'count' : 'Report.ID',
            'point' : 'POINT',
        }
        lm = LayerMapping(Point, ds, point_data_mapping, transform=False)
        print(lm)
        lm.save()
        return response

    def post(self, request,*args, **kwargs):
        return super().post(request,*args, **kwargs)
