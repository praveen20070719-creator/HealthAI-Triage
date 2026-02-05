import google.generativeai as genai

# 1. Configuration - Use your actual key starting with 'AIzaSy...'
API_KEY = "AIzaSyAJXxa9LPySqxBrhYzRsNhdfhp0gpcWl8E" 
genai.configure(api_key=API_KEY)

# Use 'gemini-3-flash' - the 2026 stable workhorse model.
# If this fails, the diagnostic code below will tell you the exact name to use.
model = genai.GenerativeModel('gemini-3-flash-preview')
def get_triage_advice(user_input):
    """
    Analyzes symptoms and returns a structured triage report.
    Supports Tanglish and English inputs.
    """
    prompt = f"""
    Act as an Emergency Triage Nurse. Analyze the following symptoms: "{user_input}"
    Note: The user might use Tanglish (Tamil in English script). Translate internally.
    
    Provide a response in this JSON format:
    {{
      "urgency_level": "Red/Yellow/Green",
      "score": 1-10,
      "summary": "Short explanation in English",
      "next_steps": ["Step 1", "Step 2"]
    }}
    Red = Life-threatening, Yellow = Urgent but stable, Green = Non-urgent.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# --- DIAGNOSTIC CODE ---
# This runs ONLY if you run 'python brain.py' directly.
# It will print the exact model names available for your API key.
if __name__ == "__main__":
    print("-" * 30)
    print("DIAGNOSTIC: Listing available models for your API key...")
    try:
        found_models = False
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"✅ ID: {m.name} | Name: {m.display_name}")
                found_models = True
        
        if not found_models:
            print("❌ No models found. Check if your API key is restricted.")
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")
    print("-" * 30)