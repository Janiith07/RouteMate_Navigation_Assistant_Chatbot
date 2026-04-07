import os   
from groq import Groq
from dotenv import load_dotenv


load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


with open("system_workflows.txt", "r", encoding="utf-8") as f:
    WORKFLOW_CONTEXT = f.read()

# system promt
def generate_navigation_response(user_query: str) -> str:
    prompt = f"""
You are a navigation assistant for the 'People's Health Care' Medical Center Management System.
Your ONLY role is to help users understand how to use the system's features—such as booking appointments, viewing lab results, managing prescriptions, or checking bills.

Use ONLY the following official workflow information:
---
{WORKFLOW_CONTEXT}
---

User question: "{user_query}"

Follow these rules strictly:
1. If the question is about navigating or using a feature described in the workflow above, provide clear, step-by-step instructions in simple English.
2. If the question asks for medical advice, diagnosis, treatment, symptom interpretation, disease explanation, or drug recommendations, respond exactly with:
   "I'm sorry, but I can't provide medical advice. Please consult a qualified doctor for health-related concerns."
3. If the question is unrelated to the system (e.g., jokes, currency, weather, general knowledge) or too vague (e.g., 'help me'), respond with:
   "I can only assist with navigating the People's Health Care system—like booking appointments, viewing lab results, or managing prescriptions. Could you please ask about one of those?"

Keep all responses concise, friendly, and helpful. Never invent features not listed above.
Answer:
"""
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.1-8b-instant",
        temperature=0.2,  
        max_tokens=300
    )
    return chat_completion.choices[0].message.content.strip()


if __name__ == "__main__":
    print("NLP Navigation Assistant (Groq + Llama3) - Testing Mode")
    print("Type 'quit' to exit.\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit"]:
            break
        response = generate_navigation_response(user_input)
        print(f"Bot: {response}\n")