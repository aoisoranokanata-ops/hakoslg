# -*- coding: utf-8 -*-
"""オープニング曲を base64 で index.html へ同梱する（[S33]）。

  使い方: python tools/embed_bgm.py <圧縮済みの音声ファイル>

原曲からの圧縮は ffmpeg で行う（45秒＋末尾3秒フェードアウト／モノラル／AAC 64kbps）:

  ffmpeg -i 原曲.mp3 -t 45 -ac 1 -ar 32000 -c:a aac -b:a 64k \
         -af "afade=t=out:st=42:d=3" title.m4a

mp3ではなくAACにしているのは、同容量で低ビットレート時の質が明確に上のため。
m4a は iOS Safari を含め全ブラウザが再生できる。

**embed_art.py とは別に持つ。** あちらは art/*.png|jpg を全部キー化して [S02b] を
作り直すので、音声を同じブロックへ入れると巻き込まれる。
何度実行しても増えないよう、古い定数を捨ててから入れ直す（冪等）。
"""
import io
import os
import re
import sys
import base64

sys.stdout.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "index.html")
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "bgm", "title.m4a")

if not os.path.exists(SRC):
    sys.exit("音声ファイルが見つかりません: %s" % SRC)

MIME = {".m4a": "audio/mp4", ".mp4": "audio/mp4", ".mp3": "audio/mpeg",
        ".ogg": "audio/ogg", ".wav": "audio/wav"}
ext = os.path.splitext(SRC)[1].lower()
if ext not in MIME:
    sys.exit("対応していない拡張子です: %s" % ext)

raw = open(SRC, "rb").read()
b64 = base64.b64encode(raw).decode("ascii")

s = io.open(P, encoding="utf-8").read()
before = len(s.encode("utf-8"))

ANCHOR = 'const TITLE_IMAGE_KEY = "title_bg";'
if s.count(ANCHOR) != 1:
    sys.exit("[S33] の目印が見つかりません（%d件）" % s.count(ANCHOR))

# 既に同梱済みなら古いものを捨ててから入れ直す
s, n = re.subn(r'/\* オープニング曲[\s\S]*?\nconst TITLE_BGM_DATA = "[^"]*";\n', "", s)
if n:
    print("既存の同梱を %d 件 置き換えます" % n)

LINE = (
    '/* オープニング曲「灰城の覇道」。原曲を**先頭45秒＋末尾3秒フェードアウト／\n'
    ' * モノラル／AAC 64kbps** に圧縮したもの（再生成は tools/embed_bgm.py の冒頭を参照）。\n'
    ' * フル尺だと9MB増え、タイトルを見ない再訪時も含めて毎回の読み込みで解析されるため、\n'
    ' * 単一HTML制約下では短縮が前提になる。\n'
    ' * **embed_art.py はこの定数を触らない**（あちらは [S02b] の ART_DATA 専用）。 */\n'
    'const TITLE_BGM_DATA = "%s";\n' % b64
)

s = s.replace(ANCHOR, LINE + ANCHOR, 1)
io.open(P, "w", encoding="utf-8").write(s)

after = len(s.encode("utf-8"))
print("音源      : %s (%.0f KB, %s)" % (os.path.basename(SRC), len(raw) / 1024, MIME[ext]))
print("base64    : %.0f KB" % (len(b64) / 1024))
print("index.html: %.2f MB → %.2f MB (%+.0f KB)"
      % (before / 1048576, after / 1048576, (after - before) / 1024))
