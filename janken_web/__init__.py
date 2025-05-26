from __future__ import annotations

import http.server
import random
import socketserver
import urllib.parse
from dataclasses import dataclass
from typing import Dict

CHOICES = ["rock", "scissors", "paper"]

HTML_TEMPLATE = """
<!doctype html>
<title>じゃんけん</title>
<h1>じゃんけんゲーム</h1>
<p>勝ち: {win} / 負け: {loss} / あいこ: {draw}</p>
<form method='post' action='/play'>
  <button type='submit' name='choice' value='rock'>ぐー</button>
  <button type='submit' name='choice' value='scissors'>ちょき</button>
  <button type='submit' name='choice' value='paper'>ぱー</button>
</form>
"""


@dataclass
class Score:
    win: int = 0
    loss: int = 0
    draw: int = 0

    def to_dict(self) -> Dict[str, int]:
        return {"win": self.win, "loss": self.loss, "draw": self.draw}


def determine_result(player: str, computer: str) -> str:
    if player == computer:
        return "draw"
    if (
        (player == "rock" and computer == "scissors")
        or (player == "scissors" and computer == "paper")
        or (player == "paper" and computer == "rock")
    ):
        return "win"
    return "loss"


class JankenHandler(http.server.SimpleHTTPRequestHandler):
    score = Score()

    def do_GET(self):
        if self.path != "/":
            self.send_error(404)
            return
        body = HTML_TEMPLATE.format(**self.score.to_dict()).encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if self.path != "/play":
            self.send_error(404)
            return
        length = int(self.headers.get("Content-Length", 0))
        data = self.rfile.read(length).decode()
        params = urllib.parse.parse_qs(data)
        choice = params.get("choice", [""])[0]
        if choice not in CHOICES:
            self.send_error(400)
            return
        computer = random.choice(CHOICES)
        result = determine_result(choice, computer)
        setattr(self.score, result, getattr(self.score, result) + 1)
        self.send_response(303)
        self.send_header("Location", "/")
        self.end_headers()


def run(server_class=http.server.HTTPServer, handler_class=JankenHandler, port: int = 8000):
    with server_class(("", port), handler_class) as httpd:
        print(f"Serving on http://localhost:{port}")
        httpd.serve_forever()


def main() -> None:
    run()


if __name__ == "__main__":
    main()
