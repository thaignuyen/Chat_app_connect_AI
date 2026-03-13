# 💬 Smart Chat Application with Gemini AI

Một ứng dụng web trò chuyện thông minh được xây dựng bằng **Python (Flask)**, tích hợp trí tuệ nhân tạo **Gemini 2.5 Flash** của Google và quản lý dữ liệu với **SQLite**. Ứng dụng cung cấp giao diện người dùng hiện đại, cho phép tương tác trực tiếp với AI và lưu trữ/xem lại lịch sử trò chuyện.

---

## ✨ Tính năng nổi bật

* **🤖 Chat với AI (Gemini):** Tích hợp API `google-generativeai` cho phép trò chuyện mượt mà với model Gemini 2.5 Flash.
* **👤 Chế độ Chat Người dùng:** Giao diện mô phỏng phòng chat giữa người với người (sẵn sàng để mở rộng tính năng real-time/WebSocket trong tương lai).
* **🕒 Quản lý lịch sử trò chuyện:** Tự động lưu trữ nội dung tin nhắn của cả Người dùng và AI vào cơ sở dữ liệu SQLite. Xem lại lịch sử dễ dàng với giao diện trực quan.
* **🎨 Giao diện hiện đại (UI/UX):** Sử dụng HTML, CSS (font Inter) và Vanilla JS. Có thanh điều chỉnh độ sáng màn hình (Brightness Control) và hiệu ứng chuyển động mượt mà.
* **⚙️ Backend API RESTful:** Kiến trúc rõ ràng với các route xử lý giao diện riêng biệt và các endpoint API (`/api/chat`, `/api/history`) để Frontend giao tiếp với Backend.

---

## 🛠️ Công nghệ sử dụng

* **Backend:** Python 3, Flask
* **AI Integration:** Google Generative AI (Gemini API)
* **Database:** SQLite (thư viện `sqlite3` tích hợp sẵn)
* **Frontend:** HTML5, CSS3, JavaScript (DOM Manipulation, Fetch API)

---

## 📁 Cấu trúc thư mục

\`\`\`text
📦 project-root
 ┣ 📂 static
 ┃ ┣ 📜 style.css               # Style cho Dashboard chính
 ┃ ┣ 📜 style_chat_bot.css      # Style cho màn hình Chat Bot
 ┃ ┣ 📜 style_chat_user.css     # Style cho màn hình Chat User
 ┃ ┣ 📜 style_history_chat.css  # Style cho màn hình Lịch sử
 ┃ ┗ 📜 script.js               # Logic điều khiển Dashboard (độ sáng, chuyển trang)
 ┣ 📂 templates
 ┃ ┣ 📜 index.html              # Trang chủ (Dashboard)
 ┃ ┣ 📜 chat_bot.html           # Giao diện chat với AI
 ┃ ┣ 📜 chat_user.html          # Giao diện chat người dùng
 ┃ ┗ 📜 history.html            # Giao diện xem lịch sử chat
 ┣ 📜 app.py                    # Khởi tạo Flask server và định nghĩa Routes/APIs
 ┣ 📜 chatbot_logic.py          # Logic kết nối và gọi API Google Gemini
 ┣ 📜 database.py               # Module xử lý cơ sở dữ liệu SQLite
 ┗ 📜 README.md                 # Tài liệu dự án
\`\`\`

---

## 🚀 Hướng dẫn cài đặt và chạy dự án

### 1. Yêu cầu hệ thống
* Python 3.8 trở lên.
* Key API của Google Gemini. Có thể lấy tại [Google AI Studio](https://aistudio.google.com/).

### 2. Cài đặt các thư viện cần thiết
Mở terminal và chạy lệnh sau để cài đặt Flask và thư viện Generative AI:
\`\`\`bash
pip install flask google-generativeai
\`\`\`

*(Khuyến khích sử dụng môi trường ảo `venv` và file `requirements.txt` để quản lý thư viện).*

### 3. Cấu hình biến môi trường
Bạn cần thiết lập biến môi trường `GEMINI_API_KEY` để ứng dụng có thể kết nối với AI.
* **Trên Windows (Command Prompt):**
    \`\`\`cmd
    set GEMINI_API_KEY=your_api_key_here
    \`\`\`
* **Trên Windows (PowerShell):**
    \`\`\`powershell
    $env:GEMINI_API_KEY="your_api_key_here"
    \`\`\`
* **Trên macOS/Linux:**
    \`\`\`bash
    export GEMINI_API_KEY="your_api_key_here"
    \`\`\`

### 4. Khởi chạy ứng dụng
Chạy file backend chính:
\`\`\`bash
python app.py
\`\`\`
Server sẽ khởi động và chạy tại địa chỉ: `http://127.0.0.1:5000/`. Mở đường dẫn này trên trình duyệt để trải nghiệm ứng dụng. Dữ liệu (file `chat_app.db`) sẽ tự động được tạo trong lần chạy đầu tiên.

---

## 💡 Hướng phát triển trong tương lai (To-do)
- [ ] Thêm tính năng đăng nhập/đăng ký (Login/Register) bằng bảng `users` đã tạo sẵn trong database.
- [ ] Tích hợp WebSocket (ví dụ: Flask-SocketIO) cho phần `chat_user.html` để có thể chat real-time.
- [ ] Mở rộng cơ sở dữ liệu để phân biệt phiên chat (Chat Sessions) thay vì lưu tất cả tin nhắn vào chung một luồng.
- [ ] Dockerize ứng dụng để dễ dàng deploy lên các nền tảng cloud.

---

## 👨‍💻 Tác giả
Dự án được phát triển và thiết kế bởi **Minh Thái**. 
\`\`\`

**Một số điểm lưu ý thêm cho bạn:**
* Đảm bảo rằng bạn đã có sẵn thư mục `templates` chứa các file `.html` (kể cả `index.html` và `chat_bot.html` chưa có trong log trên) và thư mục `static` chứa các file `.css`, `.js`. Flask yêu cầu cấu trúc thư mục chuẩn này để render đúng.
* Để README chuyên nghiệp hơn khi đưa lên GitHub, bạn có thể chụp 1-2 bức ảnh màn hình (screenshot) giao diện Dashboard và giao diện Chat để chèn ngay dưới phần giới thiệu.

Bạn có cần tôi giải thích hoặc hỗ trợ tinh chỉnh thêm chức năng nào trong phần backend Python hay database không?
