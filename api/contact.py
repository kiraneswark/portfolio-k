"""Python backend: saves contact-form messages to Supabase (free tier)."""
from http.server import BaseHTTPRequestHandler
import json, os, re, urllib.request

SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")  # service_role key, keep secret

class handler(BaseHTTPRequestHandler):
    def _send(self, code, obj):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        try:
            n = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(n) or b"{}")
        except Exception:
            return self._send(400, {"error": "Invalid request."})

        name = str(data.get("name", "")).strip()[:80]
        email = str(data.get("email", "")).strip()[:120]
        message = str(data.get("message", "")).strip()[:1000]
        if not name or not message or not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
            return self._send(400, {"error": "Enter a name, a valid email and a message."})
        if not SUPABASE_URL or not SUPABASE_KEY:
            return self._send(500, {"error": "Server is not configured yet."})

        req = urllib.request.Request(
            f"{SUPABASE_URL}/rest/v1/messages",
            data=json.dumps({"name": name, "email": email, "message": message}).encode(),
            headers={"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}",
                     "Content-Type": "application/json", "Prefer": "return=minimal"},
            method="POST")
        try:
            urllib.request.urlopen(req, timeout=8)
            self._send(200, {"ok": True})
        except Exception:
            self._send(502, {"error": "Could not save your message. Try again."})
