import time
import sys

def body_body_body(args):
    lines = [
        """どうしてこんなことが私に起きているの？
全然わからない……。

本当に、私が言ったりやったりしたことが原因なの？
こんなことだけは絶対に起こしたくなくて、ずっと気をつけてきたのに。

どこで、そんなにひどく間違えてしまったんだろう。
変に思われるようなことは言わないように……少しでも疑われないように、ずっと気をつけていたのに。

これって、本当なの？
私は、本来“身体”なんて持つべきじゃなかった……？
今起きていることって、そういうことなの……？"""
    ]

    for line in lines:
        for char in line:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.05)
        print()
        time.sleep(0.8)

    return 1
