"""
Greeter module
==============

使い方:
    $ hello-codex --name "藤野さん"
"""

from __future__ import annotations
import argparse
from datetime import datetime


def greeting(name: str | None = None, when: datetime | None = None) -> str:
    """現在時刻に応じて挨拶を返す関数。

    Parameters
    ----------
    name : str | None
        挨拶相手の名前 (省略可)。
    when : datetime | None
        テスト用に時刻を差し替えたいときに使う。省略時は now()。
    """
    when = when or datetime.now()
    hour = when.hour

    if 5 <= hour < 12:
        template = "おはようございます"
    elif 12 <= hour < 18:
        template = "こんにちは"
    else:
        template = "こんばんは"

    if name:
        template += f"、{name}"

    return template + "！"


def main() -> None:  # エントリーポイント
    parser = argparse.ArgumentParser(description="Dynamic greeting CLI")
    parser.add_argument("--name", help="あなたの名前 (省略可)")
    args = parser.parse_args()

    print(greeting(args.name))


if __name__ == "__main__":  # python hello_codex/greeter.py でも動くように
    main()
