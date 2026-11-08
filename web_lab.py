"""Loopback-only SQL injection teaching app. NEVER deploy on a public server."""

import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit

from lab import database, safe_lookup, vulnerable_lookup


PAGE = """<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>SQL Query Security Lab</title>
<style>body{font:16px system-ui;background:#101b2d;color:#f5f7fb;max-width:800px;margin:3rem auto;padding:1rem}
input,button{font:inherit;padding:.65rem;margin:.25rem}input{width:60%}button{cursor:pointer}
pre{background:#243652;padding:1rem;border-radius:8px;white-space:pre-wrap}
.notice{background:#5d411b;padding:1rem;border-radius:8px}</style>
<h1>SQL Query Security Lab</h1><p class="notice">Intentionally vulnerable local example. Use only the three fictional records.</p>
<label for="username">Username</label><input id="username" value="alice" maxlength="200">
<p><button id="normal">Compare ordinary input</button><button id="demo">Compare controlled predicate</button></p>
<pre id="results" aria-live="polite">Choose a comparison.</pre>
<script>
const input=document.querySelector('#username'), output=document.querySelector('#results');
async function compare(value){output.textContent='Running local comparison...';
  try{const res=await fetch('/api/compare?username='+encodeURIComponent(value));
    const data=await res.json();output.textContent=JSON.stringify(data,null,2)}
  catch(error){output.textContent='Local request failed: '+error.message}}
document.querySelector('#normal').addEventListener('click',()=>compare(input.value));
document.querySelector('#demo').addEventListener('click',()=>{input.value="' OR '1'='1";compare(input.value)});
</script></html>"""


def compare(username):
    """Demonstrate input as SQL syntax versus data, in a fresh in-memory DB."""
    if not isinstance(username, str) or len(username) > 200:
        raise ValueError("Username must be a string with at most 200 characters")
    with database() as db:
        try:
            unsafe = vulnerable_lookup(db, username)
            unsafe_error = None
        except Exception as exc:  # unsafe SQL can produce syntax errors in this teaching lab
            unsafe, unsafe_error = [], type(exc).__name__
        safe = safe_lookup(db, username)
    return {"input": username,
            "unsafe": {"rows": [list(row) for row in unsafe], "error": unsafe_error},
            "parameterized": {"rows": [list(row) for row in safe]},
            "scope": "Fictional in-memory SQLite records only"}


class Handler(BaseHTTPRequestHandler):
    def send(self, status, content, content_type):
        body = content.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlsplit(self.path)
        if parsed.path == "/":
            return self.send(200, PAGE, "text/html; charset=utf-8")
        if parsed.path == "/api/compare":
            username = parse_qs(parsed.query, keep_blank_values=True).get("username", [""])[0]
            try:
                result = compare(username)
            except ValueError as exc:
                return self.send(400, json.dumps({"error": str(exc)}), "application/json")
            return self.send(200, json.dumps(result), "application/json")
        self.send(404, json.dumps({"error": "Not found"}), "application/json")

    def log_message(self, fmt, *args):
        pass  # avoid recording input-bearing URLs in console logs


def make_server(port=8765):
    return ThreadingHTTPServer(("127.0.0.1", port), Handler)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Run deliberately vulnerable local-only SQL teaching app")
    p.add_argument("--port", type=int, default=8765)
    args = p.parse_args()
    with make_server(args.port) as server:
        print(f"Local lab: http://127.0.0.1:{server.server_port} (Ctrl+C to stop)")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
