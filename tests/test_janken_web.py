import pathlib
import sys
import threading
import urllib.request
import urllib.parse
from http.server import HTTPServer

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import janken_web


def start_server(server: HTTPServer):
    threading.Thread(target=server.serve_forever, daemon=True).start()


def test_play_win(monkeypatch):
    server = HTTPServer(("localhost", 0), janken_web.JankenHandler)
    start_server(server)
    port = server.server_port
    monkeypatch.setattr(janken_web.random, "choice", lambda x: "scissors")
    data = urllib.parse.urlencode({"choice": "rock"}).encode()
    urllib.request.urlopen(f"http://localhost:{port}/play", data=data)
    server.shutdown()
    assert janken_web.JankenHandler.score.win == 1


def test_play_loss(monkeypatch):
    # reset score
    janken_web.JankenHandler.score = janken_web.Score()
    server = HTTPServer(("localhost", 0), janken_web.JankenHandler)
    start_server(server)
    port = server.server_port
    monkeypatch.setattr(janken_web.random, "choice", lambda x: "paper")
    data = urllib.parse.urlencode({"choice": "rock"}).encode()
    urllib.request.urlopen(f"http://localhost:{port}/play", data=data)
    server.shutdown()
    assert janken_web.JankenHandler.score.loss == 1
