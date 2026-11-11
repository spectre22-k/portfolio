from http.server import BaseHTTPRequestHandler
import json, os, urllib.request


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            d = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))))
            name, email, phone, msg = (str(d.get(k, "")).strip() for k in ("name", "email", "phone", "message"))
            if not (name and email and msg):
                return self._send(400, {"ok": False})
            payload = json.dumps({
                "from": "Portfolio <onboarding@resend.dev>",
                "to": ["kaiftnvr@gmail.com"],
                "reply_to": email,
                "subject": f"New portfolio enquiry from {name}",
                "text": f"Name: {name}\nEmail: {email}\nPhone: {phone}\n\n{msg}",
            }).encode()
            req = urllib.request.Request(
                "https://api.resend.com/emails", payload,
                {"Authorization": "Bearer " + os.environ["RESEND_API_KEY"],
                 "Content-Type": "application/json",
                 "User-Agent": "portfolio/1.0"})
            urllib.request.urlopen(req, timeout=10)
            self._send(200, {"ok": True})
        except Exception:
            self._send(500, {"ok": False})

    def _send(self, code, body):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(body).encode())
