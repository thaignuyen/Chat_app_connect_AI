import threading
import socket
import tkinter as tk
from tkinter import messagebox, scrolledtext
import time
import importlib.util
import pathlib
from typing import Optional

try:
    from network import ChatClient
except Exception:
    from .network import ChatClient  # type: ignore


def start_embedded_server() -> Optional[threading.Thread]:
    """Attempt to import and start server.run_server in a daemon thread.
    Returns the Thread if started, else None.
    """
    try:
        # prefer package import
        import server.server as _server  # type: ignore
    except Exception:
        # fallback to file import
        try:
            base = pathlib.Path(__file__).resolve().parents[1]
            server_path = base / 'server' / 'server.py'
            if server_path.exists():
                spec = importlib.util.spec_from_file_location('server.server', str(server_path))
                _server = importlib.util.module_from_spec(spec)
                assert spec.loader is not None
                spec.loader.exec_module(_server)  # type: ignore
            else:
                return None
        except Exception:
            return None

    try:
        t = threading.Thread(target=_server.run_server, daemon=True)  # type: ignore
        t.start()
        return t
    except Exception:
        return None


def check_server(host: str, port: int, retries: int = 6, delay: float = 0.5) -> bool:
    for _ in range(retries):
        try:
            with socket.create_connection((host, port), timeout=1):
                return True
        except Exception:
            time.sleep(delay)
    return False


class ChatUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title('Chat Client (simplified)')
        root.geometry('640x420')

        conn_frame = tk.Frame(root)
        conn_frame.pack(fill='x', padx=8, pady=6)

        tk.Label(conn_frame, text='Host:').pack(side='left')
        self.host_var = tk.StringVar(value='127.0.0.1')
        tk.Entry(conn_frame, textvariable=self.host_var, width=15).pack(side='left')

        tk.Label(conn_frame, text='Port:').pack(side='left', padx=(8, 0))
        self.port_var = tk.StringVar(value='5000')
        tk.Entry(conn_frame, textvariable=self.port_var, width=6).pack(side='left')

        self.connect_btn = tk.Button(conn_frame, text='Connect', command=self.toggle_connect)
        self.connect_btn.pack(side='left', padx=8)

        self.status_var = tk.StringVar(value='Disconnected')
        tk.Label(conn_frame, textvariable=self.status_var).pack(side='right')

        self.chat_box = scrolledtext.ScrolledText(root, state='disabled', wrap='word', height=18)
        self.chat_box.pack(fill='both', expand=True, padx=8, pady=(0, 6))

        entry_frame = tk.Frame(root)
        entry_frame.pack(fill='x', padx=8, pady=(0, 8))
        self.msg_var = tk.StringVar()
        self.entry = tk.Entry(entry_frame, textvariable=self.msg_var)
        self.entry.pack(side='left', fill='x', expand=True)
        self.entry.bind('<Return>', lambda e: (self.on_send(), 'break'))
        tk.Button(entry_frame, text='Send', command=self.on_send).pack(side='left', padx=(8, 0))

        self.client: Optional[ChatClient] = None
        self.connected = False

    def append(self, text: str) -> None:
        self.chat_box.configure(state='normal')
        self.chat_box.insert('end', text + '\n')
        self.chat_box.see('end')
        self.chat_box.configure(state='disabled')

    def toggle_connect(self) -> None:
        host = self.host_var.get().strip() or '127.0.0.1'
        try:
            port = int(self.port_var.get().strip())
        except ValueError:
            messagebox.showerror('Error', 'Port must be an integer')
            return

        if not self.connected:
            # Try to connect; on ConnectionRefused, start embedded server and retry
            try:
                self.client = ChatClient(host, port)
                self.client.connect()
            except ConnectionRefusedError as e:
                self.append('Connection refused; attempting to start embedded server...')
                t = start_embedded_server()
                if t and check_server(host, port):
                    try:
                        # retry connect
                        self.client = ChatClient(host, port)
                        self.client.connect()
                    except Exception as e2:
                        messagebox.showerror('Connection failed', repr(e2))
                        self.client = None
                        return
                else:
                    messagebox.showerror('Connection failed', 'Could not start embedded server or server not available')
                    self.client = None
                    return
            except Exception as e:
                messagebox.showerror('Connection failed', repr(e))
                self.client = None
                return

            self.connected = True
            self.connect_btn.configure(text='Disconnect')
            self.status_var.set(f'Connected to {host}:{port}')
            self.append(f'Connected to {host}:{port}')
        else:
            if self.client:
                try:
                    self.client.close()
                except Exception:
                    pass
            self.client = None
            self.connected = False
            self.connect_btn.configure(text='Connect')
            self.status_var.set('Disconnected')
            self.append('Disconnected')

    def on_send(self) -> None:
        msg = self.msg_var.get().strip()
        if not msg:
            return
        self.append('You: ' + msg)
        self.msg_var.set('')

        def worker():
            try:
                if not self.connected or not self.client:
                    # one-shot send
                    c = ChatClient(self.host_var.get().strip(), int(self.port_var.get().strip()))
                    try:
                        reply = c.send_message(msg)
                    finally:
                        try:
                            c.close()
                        except Exception:
                            pass
                else:
                    reply = self.client.send_message(msg)
                self.root.after(0, lambda: self.append('Bot: ' + (reply or '')))
            except Exception as e:
                self.root.after(0, lambda: self.append('Error: ' + repr(e)))

        threading.Thread(target=worker, daemon=True).start()

def main():
    #khởi động server trong một thread riêng để không block GUI
    #chay main thì sẽ gọi server
    def _start_server_thread():
        try:
            # Prefer normal import if package path is set
            import server.server as _server  # type: ignore
        except Exception:
            # Fallback: load by file path 
            try:
                base = pathlib.Path(__file__).resolve().parents[1]
                server_path = base / 'server' / 'server.py'
                if server_path.exists():
                    spec = importlib.util.spec_from_file_location('server.server', str(server_path))
                    _server = importlib.util.module_from_spec(spec)
                    assert spec.loader is not None
                    spec.loader.exec_module(_server)  # type: ignore
                else:
                    return None
            except Exception:
                return None

        # start server.run_server in a daemon thread so it won't block GUI
        try:
            t = threading.Thread(target=_server.run_server, daemon=True)  # type: ignore
            t.start()
            return t
        except Exception:
            return None

    # server will be started after UI is created so we can report status in the UI

    root = tk.Tk()
    ui = ChatUI(root)
    # start embedded server in background and confirm availability
    try:
        t = _start_server_thread()
        def _check_server(host: str, port: str, retries: int = 6, delay: float = 0.5) -> bool:
            for _ in range(retries):
                try:
                    with socket.create_connection((host, int(port)), timeout=1):
                        return True
                except Exception:
                    time.sleep(delay)
            return False

        host = ui.host_var.get().strip() or '127.0.0.1'
        port = ui.port_var.get().strip() or '5000'
        if t and _check_server(host, port):
            ui.append(f'Server đang chạy tại {host}:{port}')
    except Exception:
        try:
            ui.append('Không thể khởi động server nhúng.')
        except Exception:
            pass
    # initial greeting and mode selection
    try:
        ui.append('Xin chào!')
        # Ask user which mode they want
        choice = messagebox.askquestion('Chọn chế độ', 'Bạn muốn chat với chatbot hay là chat với user?\nChọn "Yes" = chatbot, "No" = user')
        if choice == 'yes':
            ui.mode = 'chatbot'
            ui.append('Bạn đang chat với: Chatbot. Gõ tin nhắn rồi nhấn Enter hoặc click Send.')
        else:
            ui.mode = 'user'
            ui.append('Bạn đang chat với: User (local). Tin nhắn sẽ chỉ hiển thị cục bộ.)')
    except Exception:
        # ignore UI errors and default to chatbot
        ui.mode = 'chatbot'
    root.protocol('WM_DELETE_WINDOW', lambda: (ui.client.close() if ui.client else None, root.destroy()))
    root.mainloop()


if __name__ == '__main__':
    main()
