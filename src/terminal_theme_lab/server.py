from __future__ import annotations

import json
from functools import partial
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from .theme import load_theme, save_theme


class ThemeHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args: Any, static_dir: Path, theme_path: Path, **kwargs: Any) -> None:
        self.theme_path = theme_path
        super().__init__(*args, directory=str(static_dir), **kwargs)

    def _json_response(self, status: HTTPStatus, body: Any) -> None:
        data = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self) -> None:
        if self.path == "/api/theme":
            self._json_response(HTTPStatus.OK, load_theme(self.theme_path))
            return
        super().do_GET()

    def do_PUT(self) -> None:
        if self.path != "/api/theme":
            self.send_error(HTTPStatus.NOT_FOUND)
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length > 64_000:
                raise ValueError("request is too large")
            payload = json.loads(self.rfile.read(length))
            theme = save_theme(self.theme_path, payload)
        except (ValueError, json.JSONDecodeError) as error:
            self._json_response(HTTPStatus.BAD_REQUEST, {"error": str(error)})
            return

        self._json_response(HTTPStatus.OK, theme)


def serve(project_root: Path, theme_path: Path, host: str, port: int) -> None:
    handler = partial(
        ThemeHandler,
        static_dir=project_root / "static",
        theme_path=theme_path,
    )
    server = ThreadingHTTPServer((host, port), handler)
    display_host = "localhost" if host in {"0.0.0.0", "::"} else host
    print(f"Theme Lab: http://{display_host}:{port}")
    print(f"Listening: {host}:{port}")
    print(f"Editing:   {theme_path}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Theme Lab")
    finally:
        server.server_close()

