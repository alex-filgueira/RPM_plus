from django.test import TestCase

# Create your tests here.
from rpm_web.models import Types_inputs_model

class Types_inputs_modelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        Types_inputs_model.objects.create(name='Big', comment='commentario',)

    def test_name_label(self):
        types=Types_inputs_model.objects.get(id=1)
        field_label = types._meta.get_field('name').verbose_name
        self.assertEquals(field_label,'name')

    def test_comment_label(self):
        types=Types_inputs_model.objects.get(id=1)
        field_label = types._meta.get_field('comment').verbose_name
        self.assertEquals(field_label,'comment')

    def test_name_max_length(self):
        types=Types_inputs_model.objects.get(id=1)
        max_length = types._meta.get_field('name').max_length
        self.assertEquals(max_length,200)




