from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from base import mods


class PostProcTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        mods.mock_query(self.client)

    def tearDown(self):
        self.client = None

    def test_identity(self):
        data = {
            'type': 'IDENTITY',
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 5 },
                { 'option': 'Option 2', 'number': 2, 'votes': 0 },
                { 'option': 'Option 3', 'number': 3, 'votes': 3 },
                { 'option': 'Option 4', 'number': 4, 'votes': 2 },
                { 'option': 'Option 5', 'number': 5, 'votes': 5 },
                { 'option': 'Option 6', 'number': 6, 'votes': 1 },
            ]
        }

        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 5, 'postproc': 5 },
            { 'option': 'Option 5', 'number': 5, 'votes': 5, 'postproc': 5 },
            { 'option': 'Option 3', 'number': 3, 'votes': 3, 'postproc': 3 },
            { 'option': 'Option 4', 'number': 4, 'votes': 2, 'postproc': 2 },
            { 'option': 'Option 6', 'number': 6, 'votes': 1, 'postproc': 1 },
            { 'option': 'Option 2', 'number': 2, 'votes': 0, 'postproc': 0 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_bad_postproc(self):
        data = {
            'type': 'SCORED_QUESTION',
            'options': [
                { 'option': 'Option 1', 'number': 2, 'votes': 5 },
                { 'option': 'Option 2', 'number': 3, 'votes': 0 },
                { 'option': 'Option 3', 'number': 4, 'votes': 3 },
                { 'option': 'Option 4', 'number': 5, 'votes': 2 },
                { 'option': 'Option 5', 'number': 6, 'votes': 5 },
                { 'option': 'Option 6', 'number': 7, 'votes': 1 },
                { 'option': 'Option 7', 'number': 8, 'votes': 3 },
                { 'option': 'Option 8', 'number': 9, 'votes': 2 },
                { 'option': 'Option 9', 'number': 10, 'votes': 5 },
                { 'option': 'Option 10', 'number': 11, 'votes': 1 },
            ]
        }

        expected_result = [
            { 'option': 'Option 1', 'number': 2, 'votes': 5 ,'posproc': 4},
            { 'option': 'Option 2', 'number': 3, 'votes': 0 ,'posproc': 0},
            { 'option': 'Option 3', 'number': 4, 'votes': 3 ,'posproc': 0},
            { 'option': 'Option 4', 'number': 5, 'votes': 2 ,'posproc': 0},
            { 'option': 'Option 5', 'number': 6, 'votes': 5 ,'posproc': 6},
            { 'option': 'Option 6', 'number': 7, 'votes': 1 ,'posproc': 7},
            { 'option': 'Option 7', 'number': 8, 'votes': 3 ,'posproc': 5},
            { 'option': 'Option 8', 'number': 9, 'votes': 2 ,'posproc': 0},
            { 'option': 'Option 9', 'number': 10, 'votes': 5 ,'posproc': 1},
            { 'option': 'Option 10', 'number': 11, 'votes': 1 ,'posproc': 0},
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertNotEqual(values, expected_result)
