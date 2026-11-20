import json
import math
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import joblib

MODEL = joblib.load("model.joblib")


class Handler(BaseHTTPRequestHandler):
    def reply(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/healthz":
            self.reply(200, {"status": "ok"})
        else:
            self.reply(404, {"error": "unknown endpoint"})

    def do_POST(self):
        if self.path != "/predict":
            self.reply(404, {"error": "unknown endpoint"})
            return
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if not 1 <= size <= 65536:
                raise ValueError("invalid payload size")
            rows = json.loads(self.rfile.read(size))["instances"]
            if not isinstance(rows, list) or not 1 <= len(rows) <= 128:
                raise ValueError("expected 1 to 128 observations")
            for row in rows:
                if not isinstance(row, list) or len(row) != 4 or not all(
                    type(value) in (float, int) and math.isfinite(value) for value in row
                ):
                    raise ValueError("each observation must contain four finite numbers")
        except (ValueError, KeyError, TypeError, OverflowError):
            self.reply(400, {"error": "invalid instances"})
            return
        self.reply(200, {"predictions": MODEL.predict(rows).tolist()})


if __name__ == "__main__":
    ThreadingHTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
