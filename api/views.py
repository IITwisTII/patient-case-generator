from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status
from api.services.openai_client import client
from api.services.case_generator import generate_patient_case, generate_sbar_report
from api.services.chat_manager import chat_with_patient
from api.services.evaluation import evaluate_diagnosis
from api.services.medical_test_results import perform_medical_test
from api.utils.data_utils import load_diagnoses
from api.utils.commands import final_diagnosis_command, medical_test_command

json_file_path = 'media/final_icd_data.json'
diagnoses = load_diagnoses(json_file_path)

class GenerateCaseView(APIView):
    def get(self, request):
        try:
            request.session.pop('chat_history', None)
            request.session.pop('patient_case', None)

            case = generate_patient_case(client, diagnoses)
            request.session['patient_case'] = case
            sbar = generate_sbar_report(case)
            return Response(sbar, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ChatMessageView(APIView):
    parser_classes = [JSONParser]
    
    def post(self, request):
        user_input = request.data.get('user_input')
        if "patient_case" in request.session:
            patient_case = request.session.get('patient_case')
        else:
            return Response({"error": "No patient case found."}, status=status.HTTP_404_NOT_FOUND)

        chat_history = request.session.get('chat_history', [])
        response = chat_with_patient(client, user_input, patient_case, chat_history).get('message')

        chat_history.append(f"User: {user_input}")
        chat_history.append(f"Patient: {response}")
        request.session['chat_history'] = chat_history
        
        '''
        first_element = user_input[0][0]
        if final_diagnosis_command(first_element):
            evaluation = evaluate_diagnosis(client, patient_case, chat_history)
            return Response({
                "history": chat_history,
                "chat_ended": True,
                "evaluation": evaluation
            }, status=status.HTTP_200_OK)
        elif medical_test_command(first_element):
            test_results = perform_medical_test(client, user_input, patient_case, chat_history)
            return Response({
                "test_results": test_results, 
                "history": chat_history
            }, status=status.HTTP_200_OK)'''
        
        return Response({"response": response, "history": chat_history}, status=status.HTTP_200_OK)

class ClearChatHistoryView(APIView):
    def post(self, request):
        request.session.pop('chat_history', None)
        return Response({"message": "Chat history cleared."}, status=status.HTTP_200_OK)

