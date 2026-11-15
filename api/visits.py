"""Python backend: visitor counter stored in Supabase via an RPC function."""
from http.server import BaseHTTPRequestHandler
import json, os, urllib.request

URL = os.environ.get("SUPABASE_URL", "")
KEY = os.environ.get("SUPABASE_KEY", "")

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        count = None
        try:
            req = urllib.request.Request(
                f"{URL}/rest/v1/rpc/increment_visits", data=b"{}", method="POST",
                headers={"apikey": KEY, "Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
            count = json.loads(urllib.request.urlopen(req, timeout=8).read())
        except Exception:
            pass
        body = json.dumps({"count": count}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)
