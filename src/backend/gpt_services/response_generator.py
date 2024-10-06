import json

def generate_openai_response(client, system_prompt, user_prompts, model="gpt-3.5-turbo", max_tokens=1000, temperature=0.7):
    messages = [{"role": "system", "content": system_prompt}]
    
    for prompt in user_prompts:
        messages.append({"role": "user", "content": prompt})
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature
        )
        
        print("Raw API Response:", response)  # Check raw response
        content = response.choices[0].message.content
        
        # Attempt to load the content as JSON
        try:
            return json.loads(content)  # Try to parse as JSON
        except json.JSONDecodeError:
            return {"message": content}  # Return as plain text if JSON parsing fails
    except Exception as e:
        return {"error": str(e)}