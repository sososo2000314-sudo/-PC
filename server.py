
import json
import os
import sqlite3
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = Path(os.environ.get("DB_PATH", str(BASE_DIR / "data.db")))

def initialize_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS app_state (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                data TEXT NOT NULL
            )
        """)
        conn.execute(
            "INSERT OR IGNORE INTO app_state (id, data) VALUES (1, '{}')"
        )

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/state":
            with sqlite3.connect(DB_PATH) as conn:
                row = conn.execute(
                    "SELECT data FROM app_state WHERE id = 1"
                ).fetchone()
            body = (row[0] if row else "{}").encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        if self.path == "/":
            self.path = "/index.html"
        super().do_GET()

    def do_POST(self):
        if self.path != "/api/state":
            self.send_error(404)
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > 5_000_000:
                self.send_error(413, "Invalid request size")
                return

            data = json.loads(self.rfile.read(length))
            if not isinstance(data, dict):
                self.send_error(400, "Expected a JSON object")
                return

            serialized = json.dumps(data, ensure_ascii=False)
            with sqlite3.connect(DB_PATH) as conn:
                conn.execute(
                    "UPDATE app_state SET data = ? WHERE id = 1",
                    (serialized,)
                )

            body = b'{"ok":true}'
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        except (ValueError, json.JSONDecodeError):
            self.send_error(400, "Invalid JSON")

    def log_message(self, format, *args):
        print(format % args)

if __name__ == "__main__":
    initialize_db()
    port = int(os.environ.get("PORT", "8000"))
    print(f"Japan Connect server starting on port {port}")
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()
