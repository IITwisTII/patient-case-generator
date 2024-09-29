import unittest
from unittest.mock import patch, MagicMock
from flask import Flask, session
from api_routes import api_routes

class ApiRoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.secret_key = 'test_secret'
        self.app.register_blueprint(api_routes)
        self.client = self.app.test_client()
        self.client.testing = True

    @patch('api.load_diagnoses')
    @patch('api.generate_patient_case')
    @patch('api.generate_sbar_report')
    def test_generate_case_success(self, mock_generate_sbar_report, mock_generate_patient_case, mock_load_diagnoses):
        # Mocking the dependencies
        mock_load_diagnoses.return_value = {'diagnosis': 'Test Diagnosis'}
        mock_generate_patient_case.return_value = {'case_info': 'Test Case'}
        mock_generate_sbar_report.return_value = {'sbar': 'Test SBAR'}

        response = self.client.get('/generate-case')

        self.assertEqual(response.status_code, 201)
        self.assertIn('sbar', response.get_json())
        self.assertEqual(session['patient_case'], {'case_info': 'Test Case'})

    @patch('api.load_diagnoses')
    @patch('api.generate_patient_case')
    def test_generate_case_failure(self, mock_generate_patient_case, mock_load_diagnoses):
        mock_load_diagnoses.return_value = {'diagnosis': 'Test Diagnosis'}
        mock_generate_patient_case.side_effect = Exception("An error occurred")

        response = self.client.get('/generate-case')

        self.assertEqual(response.status_code, 500)
        self.assertIn('error', response.get_json())

    @patch('api.chat_with_patient')
    def test_chat_message_success(self, mock_chat_with_patient):
        with self.client as c:
            c.post('/generate-case')  # First generate a case to set session
            mock_chat_with_patient.return_value = {'response': 'Chat response'}

            response = c.post('/chat/messages', json={'user_input': 'Hello'})

            self.assertEqual(response.status_code, 200)
            self.assertIn('response', response.get_json())

    def test_chat_message_no_case(self):
        response = self.client.post('/chat/messages', json={'user_input': 'Hello'})

        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.get_json())

    def test_index_init(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<!DOCTYPE html>', response.data)  # Check for the presence of HTML

    def test_chat_init(self):
        response = self.client.get('/chat')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<!DOCTYPE html>', response.data)  # Check for the presence of HTML

if __name__ == '__main__':
    unittest.main()
