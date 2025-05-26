import pathlib
import sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import subprocess
from datetime import datetime

from hello_codex import greeter


def test_greeting_morning_with_name():
    when = datetime(2023, 1, 1, 8, 0, 0)
    assert greeter.greeting("Alice", when) == "おはようございます、Alice！"


def test_greeting_afternoon_no_name():
    when = datetime(2023, 1, 1, 15, 0, 0)
    assert greeter.greeting(when=when) == "こんにちは！"


def test_greeting_evening_with_name():
    when = datetime(2023, 1, 1, 20, 0, 0)
    assert greeter.greeting("Bob", when) == "こんばんは、Bob！"


def test_cli_runs():
    proc = subprocess.run(
        [sys.executable, "-m", "hello_codex.greeter", "--name", "Alice"],
        capture_output=True,
        text=True,
        check=True,
    )
    out = proc.stdout.strip()
    assert out.endswith("Alice！")
    assert any(
        out.startswith(prefix) for prefix in ["おはようございます", "こんにちは", "こんばんは"]
    )
