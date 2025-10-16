from http.server import BaseHTTPRequestHandler, HTTPServer
import json

data = [
    {'ID': 1, 'Country': 'Nigeria', 'State': 'Ogun'},
    {'ID': 2, 'Country': 'Nigeria', 'State': 'Lagos'},
    {'ID': 3, 'Country': 'Nigeria', 'State': 'Kwara'}
]

class BasicApi(BaseHTTPRequestHandler):
    def send_data(self, payload, status = 200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode())

    def do_DELETE(self):
        content_size = int(self.headers.get('Content-Length', 0))
        parsed_data = self.rfile.read(content_size)

        post_data = json.loads(parsed_data)
        id = post_data.get('ID')

        if id is None:
            self.send_data({"error": "Missing ID in request body"}, status =400)
        else:
            target_list = [(x, data.index(x)) for x in data if x['ID'] == id]
            target_tuple = target_list[0]
            target_dic, target_index = target_tuple
            data.remove(target_dic)
            print(data)

            self.send_data([{
                'Message': 'Data Deleted',
                'data': post_data
            }])
def run():
    HTTPServer(('localhost', 8080), BasicApi).serve_forever()

print('Application is running')
run()