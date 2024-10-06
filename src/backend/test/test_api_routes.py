import unittest
from unittest.mock import patch
from flask import Flask
from api_routes import api_routes

class ApiRoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.secret_key = 'test_secret'
        self.app.register_blueprint(api_routes)
        self.client = self.app.test_client()
        self.client.testing = True


    @patch('api_routes.load_diagnoses')
    @patch('api_routes.generate_patient_case')
    def test_generate_case_failure(self, mock_generate_patient_case, mock_load_diagnoses):
        mock_load_diagnoses.return_value = {'diagnosis': 'Test Diagnosis'}
        mock_generate_patient_case.side_effect = Exception("An error occurred")

        response = self.client.get('/generate-case')

        self.assertEqual(response.status_code, 500)
        self.assertIn('error', response.get_json())

    @patch('api_routes.chat_with_patient')
    def test_chat_message_success(self, mock_chat_with_patient):
        with self.client as c:
            c.get('/generate-case')  # First generate a case to set session
            mock_chat_with_patient.return_value = {'response': 'Chat response'}

            response = c.post('/chat/messages', json={'user_input': 'Hello'})

            self.assertEqual(response.status_code, 200)
            self.assertIn('response', response.get_json())

if __name__ == '__main__':
    unittest.main()
