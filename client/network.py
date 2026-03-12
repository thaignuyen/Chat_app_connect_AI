import socket
from typing import Optional


class ChatClient:
    """Simple TCP chat client to talk to the project server.

    Usage:
        c = ChatClient('127.0.0.1', 5000)
        c.connect()
        reply = c.send_message('hello')
        c.close()
    """

    def __init__(self, host: str = '127.0.0.1', port: int = 5000, timeout: float = 5.0):
        self.host = host
        self.port = int(port)
        self.timeout = float(timeout)
        self.sock: Optional[socket.socket] = None

    def connect(self) -> None:
        if self.sock:
            return
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(self.timeout)
        s.connect((self.host, self.port))
        # Make recv blocking after connect
        s.settimeout(None)
        self.sock = s

    def send_message(self, message: str) -> str:
        if not isinstance(message, (str, bytes)):
            raise ValueError('message must be str or bytes')

        if not self.sock:
            self.connect()

        data = message if isinstance(message, (bytes, bytearray)) else message.encode('utf-8')
        # ensure newline to indicate end if server expects lines
        if not data.endswith(b"\n"):
            data = data + b"\n"

        try:
            self.sock.sendall(data)
        except Exception:
            # try reconnect once
            self.close()
            self.connect()
            self.sock.sendall(data)

        # read response until newline or socket closes
        chunks = []
        try:
            while True:
                part = self.sock.recv(4096)
                if not part:
                    break
                chunks.append(part)
                if b"\n" in part:
                    break
        except Exception:
            pass

        raw = b"".join(chunks)
        try:
            return raw.decode('utf-8').strip()
        except Exception:
            return str(raw)

    def close(self) -> None:
        if self.sock:
            try:
                self.sock.close()
            finally:
                self.sock = None


def send_once(host: str, port: int, message: str, timeout: float = 5.0) -> str:
    c = ChatClient(host, port, timeout=timeout)
    try:
        return c.send_message(message)
    finally:
        c.close()
