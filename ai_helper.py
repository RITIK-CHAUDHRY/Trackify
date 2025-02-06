import openai
from config import Config

openai.api_key = Config.OPENAI_API_KEY

def analyze_spending_patterns(expenses):
    """Analyze spending patterns using OpenAI"""
    try:
        prompt = f"Analyze these expenses and provide insights: {expenses}"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error analyzing expenses: {str(e)}"

def get_budget_recommendations(income, expenses):
    """Get personalized budget recommendations"""
    try:
        prompt = f"Given monthly income of {income} and expenses {expenses}, provide budget recommendations"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=200
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error generating recommendations: {str(e)}"

def get_chatbot_response(message):
    """Get AI chatbot response"""
    try:
        prompt = f"""You are a financial advisor chatbot. 
        Provide helpful advice for the following query: {message}
        Keep the response concise and practical."""
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful financial advisor."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating response: {str(e)}"