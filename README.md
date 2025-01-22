# patient-case-generator


Comments: 
- routes: 
    - api_routes.py: 
        - chat_message route should map calls to a seperate controller function since the function is starting to get complicated and will, no doubt, get more complicated.
            - Final_diagnosis and medical_test_command not working right now
        - clear-chat-history isn't being used right now.
- services: 
    - case_generator: 
        - The case generated should be very detailed, containing most of the information the user will try to investigate and all the best management practices and routines tailored for the case (will be used later in evaluation and feedback). 
        - Have a prompt for the AI to act like a patient instead of an SBAR prompt
    - chat_manager: 
        - Currently not working as it should. I think this could be merged with case_generator
    - config_loader: 
        - Temporary fix. Learn to use dotenv properly and implement it instead. 
    - evaluation: 
        - Not currently working. Inconsistent naming. 
    - medical_test_results: 
        - Not currently working. Inconsistent naming. 
- tests: 
    - Create a lot of tests for easier developement and better security

