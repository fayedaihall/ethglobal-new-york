from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response = {
            "status": "Dating Matcher Agent is running",
            "agent": "lovefi-matcher",
            "message": "Simple test endpoint working"
        }
        
        self.wfile.write(json.dumps(response).encode())
        return

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response = {
            "status": "received",
            "message": "POST endpoint working",
            "received_data_length": len(post_data)
        }
        
        self.wfile.write(json.dumps(response).encode())
        return
