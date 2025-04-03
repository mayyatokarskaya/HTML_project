from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import os

hostName = "localhost"
serverPort = 8080


class MyServer(BaseHTTPRequestHandler):

    def __read_html_file(self):
        """Читает HTML файл из папки html"""
        try:
            file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'html', 'contact.html')
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            return "<h1>Error: contact.html not found</h1>"

    def do_GET(self):
        page_content = self.__read_html_file()
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(page_content, "utf-8"))

    def do_POST(self):
        # Обработка POST-запроса
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)

        # Парсим данные формы (application/x-www-form-urlencoded)
        try:
            form_data = parse_qs(post_data.decode('utf-8'))

            # Логируем в консоль
            print("\nПолучены POST-данные:")
            for key, values in form_data.items():
                print(f"{key}: {values[0]}")

            # Отправляем ответ клиенту
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            # Читаем HTML снова для отправки
            page_content = self.__read_html_file()
            self.wfile.write(bytes(page_content, "utf-8"))

        except Exception as e:
            print(f"Ошибка обработки POST-запроса: {str(e)}")
            self.send_response(500)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(bytes("Internal Server Error", "utf-8"))


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print(f"Сервер запущен http://{hostName}:{serverPort}")
    print("GET: возвращает contact.html")
    print("POST: логирует данные формы в консоль")

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Сервер остановлен")