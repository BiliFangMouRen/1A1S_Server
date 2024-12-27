import http.server
import socketserver
import os
import signal
import sys

PORT = 8080

def signal_handler(sig, frame):
    print('\nShutting down server...')
    sys.exit(0)

# 注册信号处理器
signal.signal(signal.SIGINT, signal_handler)

class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

def main():
    try:
        # 尝试终止可能存在的旧进程
        try:
            with open('server.pid', 'r') as f:
                old_pid = int(f.read())
                try:
                    os.kill(old_pid, signal.SIGTERM)
                except ProcessLookupError:
                    pass  # 进程已经不存在
        except FileNotFoundError:
            pass  # PID文件不存在

        # 保存当前进程的PID
        with open('server.pid', 'w') as f:
            f.write(str(os.getpid()))

        # 设置服务器
        Handler.extensions_map.update({
            '.html': 'text/html',
            '.json': 'application/json',
        })

        # 使用 SO_REUSEADDR 选项
        socketserver.TCPServer.allow_reuse_address = True
        
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print(f"Server running at http://localhost:{PORT}")
            httpd.serve_forever()

    except OSError as e:
        if e.errno == 48:  # Address already in use
            print("Error: Port 8080 is already in use.")
            print("Please try the following steps:")
            print("1. Kill any existing Python processes:")
            print("   pkill -f python")
            print("2. Or change the port number in server.py")
            sys.exit(1)
        else:
            raise

if __name__ == "__main__":
    main() 