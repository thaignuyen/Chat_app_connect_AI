from flask import Flask, render_template, request, jsonify
from chatbot_logic import get_ai_response
from database import Database

app = Flask(__name__)
db = Database()
db.init_db()

# --- Các route để phục vụ giao diện HTML ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat_bot.html')
def chat_bot():
    return render_template('chat_bot.html')

@app.route('/chat_user.html')
def chat_user():
    return render_template('chat_user.html')

@app.route('/history.html')
def history():
    return render_template('history.html')

# --- REST API để Frontend gọi Backend AI ---
@app.route('/api/chat', methods=['POST'])
def api_chat():
    data = request.get_json()
    user_message = data.get('message')

    if not user_message:
        return jsonify({'error': 'Không có tin nhắn'}), 400

    # Lưu tin nhắn của user vào DB
    db.save_message("User", user_message)

    # Gọi AI để lấy phản hồi
    ai_reply = get_ai_response(user_message)

    # Lưu tin nhắn của AI vào DB
    db.save_message("AI", ai_reply)

    return jsonify({'reply': ai_reply})
@app.route('/api/history', methods=['GET'])
def api_history():
    # Gọi hàm get_messages từ file database.py 
    # Dữ liệu trả về đang là dạng tuple: (id, sender, content, timestamp)
    raw_messages = db.get_messages(limit=50) 
    
    # Chuyển đổi dữ liệu thành danh sách dictionary (để jsonify có thể chuyển thành JSON)
    formatted_history = []
    for msg in raw_messages:
        msg_id, sender, content, timestamp = msg
        
        # Format lại cho khớp với cấu trúc JS trong file HTML
        formatted_history.append({
            'id': msg_id,
            'type': 'ai' if sender == 'AI' else 'user',
            'title': 'Chat với AI' if sender == 'AI' else 'Người dùng',
            'time': timestamp, 
            'snippet': f'{sender}: "{content}"'
        })
        
    return jsonify(formatted_history)

if __name__ == '__main__':
    # Chạy server ở port 500
    app.run(host='127.0.0.1', port= 5000, debug=True)