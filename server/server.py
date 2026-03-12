import socket
import threading
import os
import sys

# Ensure this directory is on sys.path so imports like `import chatbot_logic`
# succeed regardless of current working directory when server.py is executed.
base_dir = os.path.dirname(os.path.abspath(__file__))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)
# Import hàm xử lý AI từ file chatbot_logic.py của bạn
try:
    # Prefer the straightforward absolute import
    import chatbot_logic as _chatbot_mod
    get_ai_response = _chatbot_mod.get_ai_response
except ImportError:
    # Nếu chạy file này độc lập, dùng import thông thường
    try:
        # As a last resort, attempt to load the module directly from file
        from chatbot_logic import get_ai_response
    except Exception as e:
        print(f"[IMPORT ERROR] Không thể import chatbot_logic: {e}")
        # Provide a fallback handler that returns an error message so server can still run
        def get_ai_response(prompt: str) -> str:
            return 'Error: chatbot_logic not available.'

def handle_client(conn, addr):
    """Xử lý từng kết nối từ client."""
    print(f"[NEW CONNECTION] {addr} connected.")
    try:
        # Nhận dữ liệu từ Client (main_ui)
        data = conn.recv(1024).decode('utf-8').strip()
        if data:
            print(f"[{addr}] User gửi: {data}")
            
            # Gửi tin nhắn sang AI Gemini để lấy câu trả lời
            reply = get_ai_response(data)
            
            # Gửi lại phản hồi cho Client
            # Thêm \n để client biết đã kết thúc tin nhắn
            conn.sendall((reply + "\n").encode('utf-8'))
    except Exception as e:
        print(f"[ERROR] Lỗi xử lý client {addr}: {e}")
    finally:
        conn.close()

def run_server(host='127.0.0.1', port=5000):
    """Khởi động server socket."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Cho phép sử dụng lại địa chỉ cổng nếu server bị tắt đột ngột
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server.bind((host, port))
    except Exception as e:
        print(f"[BIND ERROR] Không thể mở cổng {port}: {e}")
        return

    server.listen()
    print(f"[LISTENING] Server đang chạy tại {host}:{port}...")

    while True:
        try:
            conn, addr = server.accept()
            # Mỗi client được xử lý trong một luồng (thread) riêng để không làm treo server
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
        except KeyboardInterrupt:
            print("\n[STOPPING] Server đang tắt...")
            break
        except Exception as e:
            print(f"[SERVER ERROR] {e}")
    
    server.close()

if __name__ == "__main__":
    # Chạy thử server độc lập
    run_server()