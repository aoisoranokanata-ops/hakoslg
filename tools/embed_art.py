#!/usr/bin/env python3
"""art/*.png を base64 で index.html の [S02b] ART_DATA ブロックへ埋め込む（冪等）。

使い方（リポジトリ直下で）:
    python tools/embed_art.py

- art/ 内の <imageKey>.png すべてを対象に ART_DATA を再生成する。
  例: 建物ティアアートを足す時は art/bld_castle_t2.png 等を置いて再実行するだけ。
- 既存の [S02b] ブロックがあれば置換、無ければ ASSET_URLS 行の直後に挿入。
- 画像は 256x256・透過PNG 推奨（大きすぎる素材は事前に縮小しておくこと）。
- 実行後は index.html が変わるので sw.js の CACHE バージョンも上げること。

artHTML の解決順は IndexedDB取り込み > この埋め込み(ART_DATA) > 絵文字。
ティアキーは artTierKey() が bld_x_t3 > bld_x_t2 > bld_x の順にフォールバック。
"""
import base64, glob, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML = os.path.join(ROOT, "index.html")
ART = os.path.join(ROOT, "art")

# 置換前後で必ず残っていなければならない目印（誤って本体コードを消していないか検査）
SENTINELS = ["const CONFIG =", "const BUILDING_DEFS =", "const CARD_POOL =",
             "function artHTML(", "function boot()", "function newGameState("]

# [S02b] ブロックだけを一意に捕捉する。`/* ===` の直後行が ` * [S02b]` のものに限定する
# ことで、他セクションの `/* ===` コメントを巻き込まない（過去に全削除する不具合があった）。
BLOCK_RE = re.compile(r"/\* =+\n \* \[S02b\][\s\S]*?\nconst ART_DATA = \{[\s\S]*?\n\};\n")
ANCHOR = "const ASSET_URLS = {}; // imageKey → objectURL\n"

def build_block():
    keys = sorted(os.path.splitext(os.path.basename(p))[0] for p in glob.glob(os.path.join(ART, "*.png")))
    if not keys:
        sys.exit("no PNGs in art/")
    lines, total = [], 0
    for k in keys:
        b = open(os.path.join(ART, k + ".png"), "rb").read(); total += len(b)
        lines.append(f'  "{k}": "data:image/png;base64,{base64.b64encode(b).decode()}",')
    block = (
        "/* =====================================================================\n"
        " * [S02b] EMBEDDED ART — 建物アート(256px透過PNG)を base64 で同梱。\n"
        " *   全オリジン(公開/file://)で初回から表示するため。差し替え・追加は\n"
        " *   art/<imageKey>.png を置いて `python tools/embed_art.py` を再実行する。\n"
        " *   artHTML は IndexedDB取り込み > この埋め込み > 絵文字 の順で解決。\n"
        " * ===================================================================*/\n"
        "const ART_DATA = {\n" + "\n".join(lines) + "\n};\n")
    return block, keys, total

def main():
    block, keys, total = build_block()
    src = open(HTML, encoding="utf-8").read()
    if BLOCK_RE.search(src):
        n = len(BLOCK_RE.findall(src))
        if n != 1:
            sys.exit(f"ABORT: [S02b] block matched {n} times (expected 1)")
        new = BLOCK_RE.sub(lambda m: block, src, count=1)
        action = "replaced"
    else:
        if ANCHOR not in src:
            sys.exit("ABORT: neither ART_DATA block nor ASSET_URLS anchor found")
        new = src.replace(ANCHOR, ANCHOR + block, 1)
        action = "inserted"
    # 安全ガード: 本体コードの目印が全て残っているか
    missing = [s for s in SENTINELS if s not in new]
    if missing:
        sys.exit(f"ABORT: sentinels missing after edit, not writing: {missing}")
    if new.count("const ART_DATA = {") != 1:
        sys.exit("ABORT: ART_DATA count != 1 after edit")
    open(HTML, "w", encoding="utf-8").write(new)
    print(f"{action} ART_DATA: {len(keys)} keys ({', '.join(keys)}), raw={total//1024}KB, "
          f"index.html={os.path.getsize(HTML)//1024}KB")
    print("NOTE: sw.js の CACHE バージョンを上げること。")

if __name__ == "__main__":
    main()
