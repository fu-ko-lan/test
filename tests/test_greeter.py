import subprocess
import sys
from datetime import datetime

from hello_codex import greeter


def test_greeting_morning_with_name():
    when = datetime(2023, 1, 1, 8, 0, 0)
    assert greeter.greeting("藤野さん", when) == "おはようございます、藤野さん！"


def test_greeting_afternoon_no_name():
    when = datetime(2023, 1, 1, 13, 0, 0)
    assert greeter.greeting(when=when) == "こんにちは！"


def test_greeting_evening_with_name():
    when = datetime(2023, 1, 1, 21, 0, 0)
    assert greeter.greeting("田中さん", when) == "こんばんは、田中さん！"


def test_cli_runs():
    proc = subprocess.run(
        [sys.executable, "-m", "hello_codex.greeter", "--name", "テスト"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert "テスト" in proc.stdout
