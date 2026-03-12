import google.generativeai as genai

genai.configure(api_key="AIzaSyCk1lzJ36Xg6x3o4JR4JhdS3ATO6YbNr0E")

model = genai.GenerativeModel("gemini-2.5-flash")

def get_ai_response(prompt):
    res = model.generate_content(prompt)
    return res.text