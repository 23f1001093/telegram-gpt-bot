import httpx
from src.config import OPENAI_API_KEY

async def get_gpt_reply(messages):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-3.5-turbo",  # Free tier model
        "messages": messages,
        "max_tokens": 180
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)
        
        try:
            data = response.json()
        except Exception as e:
            print("Error decoding OpenAI response as JSON:", e)
            print("Raw response text:", response.text)
            return "Sorry, couldn't decode OpenAI response."
        
        print("OpenAI response:", data)
        
        # Error handling block goes here!
        if "error" in data:
            error_msg = data["error"]["message"]
            print("OpenAI API returned error:", error_msg)
            if "quota" in error_msg:
                return "Sorry, my AI backend is out of quota now. Please try again later."
            return f"OpenAI error: {error_msg}"
        
        # If no error, proceed to extract answer
        if "choices" in data and len(data["choices"]) > 0:
            return data["choices"][0]["message"]["content"]
        
        print("Unexpected OpenAI API response:", data)
        return "Sorry, no reply could be generated."
