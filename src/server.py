from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import os

hostName = "localhost"
serverPort = 8080


class MyServer(BaseHTTPRequestHandler):

    def __read_html_file(self):
        """Читает HTML файл из папки html"""
        try:
            # Поднимаемся на один уровень выше (из src в корень), затем в папку html
            file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'html', 'contact.html')
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            return "<h1>Error: contact.html not found</h1>"
        except Exception as e:
            return f"<h1>Error: {str(e)}</h1>"

    def do_GET(self):
        # На любой GET-запрос возвращаем страницу контактов
        page_content = self.__read_html_file()

        # Отправляем ответ
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(page_content, "utf-8"))


if __name__ == "__main__":
    # Проверяем существование файла contacts.html
    contacts_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'html', 'contact.html')

    if not os.path.exists(contacts_path):
        print(f"Файл contacts.html не найден по пути: {contacts_path}")
    else:
        webServer = HTTPServer((hostName, serverPort), MyServer)
        print(f"Сервер запущен http://{hostName}:{serverPort}")
        print("На любой GET-запрос будет возвращаться contacts.html")

        try:
            webServer.serve_forever()
        except KeyboardInterrupt:
            pass

        webServer.server_close()
        print("Сервер остановлен")