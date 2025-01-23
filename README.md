# patient-case-generator

Alis Comments on the current state: 
- routes: 
    - api_routes.py: 
        - chat_message route should map calls to a seperate controller function since the function is starting to get complicated and will, no doubt, get more complicated.
            - chat_messages needs inprovement. When asked for medical tests or when stating the final diagnoses, it seems to be generating patient reponse anyways. 
        - clear-chat-history isn't being used right now.
- services: 
    - case_generator: 
        - The case generated should be very detailed, containing most of the information the user will try to investigate and all the best management practices and routines tailored for the case (will be used later in evaluation and feedback). 
            - Current complaint should be specified with history of complaint
            - It should have previous patients records that look like they've been written by doctors from past healthcare visits (if any) 
            - It should also contain past and current medications. Past and current diseases and allergies. Lifestyle (physical acitivity, occupation, social life). Alchohol, drugs and smoking habits. Heredity for diseases.
        - Have past information available in the API response to display in the case viewer (instead of an SBAR report).
        - Present information (tests, radiology, physical examination etc) that are expected of the user to ask for should be ready to be sent individually when the user orders these diagnostic tests. 
    - chat_manager: 
        - There is alot of room for improvement on the prompt to make it sound more like a human patient and maybe have varied personalities. 
    - config_loader: 
        - Temporary fix. Learn to use dotenv properly and implement it instead. 
    - evaluation: 
        - Needs improvement via prompt engineering to evaluate properly. Seems to be hallucinating the users actions and unable to distinguish information provided by the AI model (patient_case) and information gathered by the user. 
        - Inconsistent naming. 
    - medical_test_results: 
        - Needs improvement via prompt engineering to return only relevant medical tests that the user asked for instead of recommending what kind of tests they should take. Inconsistent naming. 
- tests: 
    - Create a lot of tests for easier developement, testing of new features and better security
- models: 
    - Database ORM
        - User details, role and contactinformation
        - Past case details (?), scores and evaluation 
        - Validation metrics

