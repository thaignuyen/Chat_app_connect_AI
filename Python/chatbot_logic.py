import google.generativeai as genai
import os 

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

def get_ai_response(prompt : str) -> str:
    try : 
        reponse = model.generate_content(prompt)
        if reponse.text:
            return reponse.text
        return "AI không thể trả nội dung vì đã hết quota "
            
    except Exception as e:
        return f"Đã có lỗi xảy ra khi gọi API: {repr(e)}"
