#!/usr/bin/env python3
"""
Lightweight, zero-dependency local web server for the Missouri Driver Guide portal.
Supports automatic port discovery, proper MIME types (WebP, JS, JSON), and caching.
"""

import http.server
import socketserver
import os
import sys
import webbrowser

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def guess_type(self, path):
        mtype = super().guess_type(path)
        if path.endswith(".webp"):
            return "image/webp"
        if path.endswith(".js"):
            return "application/javascript; charset=utf-8"
        if path.endswith(".json"):
            return "application/json; charset=utf-8"
        if path.endswith(".css"):
            return "text/css; charset=utf-8"
        return mtype

    def end_headers(self):
        # Enable CORS and disable caching so updates reflect immediately
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        super().end_headers()

def run():
    global PORT
    for attempt in range(10):
        try:
            with socketserver.TCPServer(("", PORT), Handler) as httpd:
                url = f"http://localhost:{PORT}"
                print("=" * 60)
                print("  🚗 MISSOURI DRIVER GUIDE - LOCAL INTERACTIVE SERVER")
                print("=" * 60)
                print(f"  URL:  {url}")
                print(f"  Path: {DIRECTORY}")
                print(f"  Press Ctrl+C to stop the server.")
                print("=" * 60)
                
                # If launched with --open, open browser
                if "--open" in sys.argv or "-o" in sys.argv:
                    webbrowser.open(url)
                
                httpd.serve_forever()
                break
        except OSError as e:
            if "Address already in use" in str(e):
                PORT += 1
            else:
                raise e

if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        print("\nServer stopped.")
