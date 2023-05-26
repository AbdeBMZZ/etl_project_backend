from django.test import TestCase
from rest_framework.test import APIClient
from .models import CSVFile, TransformationRule, TransformedData

class YourTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_csv_file_list(self):
        # Your test implementation

    def test_csv_file_detail(self):
        # Your test implementation

    def test_transformation_rule_list(self):
        # Your test implementation

    def test_transformation_rule_detail(self):
        # Your test implementation

    def test_transformed_data_list(self):
        # Your test implementation

    def test_transformed_data_creation(self):
        # Your test implementation

    def test_transformed_data_creation_invalid(self):
        # Your test implementation
