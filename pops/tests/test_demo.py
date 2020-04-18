from django.test import TestCase, SimpleTestCase
from django.urls import reverse
from django.http import HttpRequest
from django.conf import settings
from users.models import CustomUser
from ..models import *

class SessionTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(username='test', first_name='test_first', last_name='test_last',
                                              email='testuser@test.com', user_type='OTHER', password='testpass')
        self.client.force_login(self.user)
        case_study = CaseStudy.objects.create(
            created_by=self.user, 
            name='Case Study Name',
            description='Description',
            number_of_pests = 1,
            number_of_hosts = 1,
            start_year = 2012,
            end_year = 2018, 
            future_years = 2021,
            time_step = 'Month',
            staff_approved = False,
        )
        print(case_study)
        session = Session.objects.create(
            case_study = case_study,
            name = 'Test session name',
            description = 'Test session description',
            reproductive_rate = 1.00,
            distance_scale = 10.0,
            final_year = 2021,
            management_month = 6,
            weather = 'AVERAGE',    
        )
        print(session)
        run_collection = RunCollection.objects.create(
            session = session,
            name = 'Run collection name',
            description = 'Run collection description',
            budget = 10000000,
            efficacy = 90,
            cost_per_meter_squared = 100,
            default = True
        )
        print(run_collection)
        run = Run.objects.create(
            run_collection = run_collection,
            management_cost = 100000,
            management_area = 2000,
            steering_year = 2018,
            status = 'SUCCESS',
        )
        print(run)
        session.default_run = run
        session.save()
        print(session.default_run.status)

    def test_workspace_status_code(self):
        response = self.client.get('/demo/')
        self.assertEquals(response.status_code, 200)
        
    def test_workspace_by_name(self):
        response = self.client.get(reverse('demo'))
        self.assertEquals(response.status_code, 200)

    def test_page_contains_correct_html(self):
        response = self.client.get('/demo/')
        print(response.content)
        self.assertContains(response, 'demo')


