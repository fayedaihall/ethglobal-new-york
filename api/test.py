from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse the URL
        url_parts = urlparse(self.path)
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {
            "status": "Dating Matcher Agent is running",
            "agent": "lovefi-matcher",
            "message": "API endpoint working",
            "path": self.path,
            "method": "GET"
        }
        
        self.wfile.write(json.dumps(response).encode('utf-8'))
        
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length > 0:
            post_data = self.rfile.read(content_length)
        else:
            post_data = b''
            
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {
            "status": "POST received",
            "message": "POST endpoint working",
            "received_bytes": len(post_data),
            "path": self.path,
            "method": "POST"
        }
        
        self.wfile.write(json.dumps(response).encode('utf-8'))
        
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
