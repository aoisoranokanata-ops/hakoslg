# 画像生成プロンプト集（ChatGPT画像生成用）

生成した画像は、ゲーム内「ガチャ」タブ最下部の「画像取り込み」で `imageKey` を指定して登録すると、
絵文字プレースホルダーの代わりに表示される（IndexedDBに保存、オフライン保持）。

## 統一アートスタイル（全プロンプト共通の接頭辞）

すべてのプロンプトの先頭に以下を付けること:

```
Stylized mobile strategy game art, Japanese sengoku-fantasy theme, clean bold
shapes, warm painterly shading, rich saturated colors, dark navy background,
no text, no watermark, centered composition.
```

カードは縦長（3:4推奨）、アイコン類は正方形（1:1）で生成。

## 1. キャラカード（レア度別の作り分け）

共通仕様: 上半身のキャラクター立ち絵＋レア度別の枠・エフェクト。レア度が上がるほど
「枠の豪華さ」「背景エフェクト」「ポーズの派手さ」を強くする。

### N（imageKey: card_n_*）
```
[共通接頭辞] Portrait card of a humble common soldier, simple leather armor,
plain expression, muted earth-tone palette, simple flat gray-silver card frame
with thin border, plain dark background, no special effects, modest and
unremarkable atmosphere. 3:4 aspect.
```
対象: card_n_taichi(足軽・槍), card_n_yosuke(農兵・鍬), card_n_kosuzu(少女斥候・鈴),
card_n_gonroku(門衛・老兵), card_n_maruta(新兵・木刀), card_n_nihei(輜重兵・荷箱)

### R（imageKey: card_r_*）
```
[共通接頭辞] Portrait card of a capable samurai officer, well-made lacquered
armor with clan crest, confident pose, cool blue accent lighting, polished
blue metallic card frame with subtle geometric engraving, faint blue glow
behind the character. 3:4 aspect.
```
対象: card_r_katsuma(侍大将), card_r_kota(槍兵), card_r_senri(参謀・書物),
card_r_hayate(騎兵・馬上), card_r_katayama(守将・大盾)

### SR（imageKey: card_sr_*）
```
[共通接頭辞] Portrait card of an elite legendary warrior, ornate purple and
silver armor with flowing cape, dramatic wind-blown pose, glowing purple
particle effects swirling around, luxurious amethyst card frame with engraved
dragon motifs, radiant backlight. 3:4 aspect.
```
対象: card_sr_soji(剣豪・二刀), card_sr_genba(策士・軍配), card_sr_mitsuru(弓聖・大弓),
card_sr_gantetsu(猛将・大斧), card_sr_kasumi(陰陽師・呪符)

### SSR（imageKey: card_ssr_*）
```
[共通接頭辞] Portrait card of a mythic supreme hero, magnificent golden armor
with divine ornaments, epic dynamic pose breaking out of the card frame,
brilliant golden light rays and floating embers, prismatic rainbow flare,
ultra-ornate gold card frame with phoenix and dragon reliefs, overwhelming
aura of power. 3:4 aspect.
```
対象: card_ssr_tenba(覇王・大剣と王冠), card_ssr_byakuren(軍神・雷を纏う女神将),
card_ssr_saya(聖女・光の錫杖), card_ssr_benimaru(鬼神・炎の金棒)

## 2. 建築物アイコン（1:1・背景透過PNG・imageKey: bld_*）

**技術前提（厳守）**: city plot 側は 48×48 の角丸タイル（暗いグラデ背景＋接地影）に
`object-fit:cover` で表示する（`.bld .bld-icon` 参照）。よってアートは
**建物単体を描いた背景透過PNG**とし、土台・地面・草地・背景は一切描かない
（枠と影はCSSが用意する）。被写体は中央、周囲に均等な小さめの余白。
**48pxでも判別できる太く明快なシルエット**にすること（細かい小物は潰れる）。

### 共通仕様プロンプト（全建物で使う）
```
256x256 px, 1:1 square, TRANSPARENT background (PNG with alpha).
A single Japanese sengoku-fantasy strategy-game building, centered,
isometric 3/4 view from slightly above, soft light from the top-left,
warm painterly shading, rich saturated colors, bold clean readable
silhouette. NO ground base, NO grass, NO scenery, NO cast shadow,
no text, no watermark. Keep small even padding around the subject.
Match the art style, viewing angle, light direction and color palette
of the reference images (the existing V1 buildings).
Building: {下記}
```

### 既存V1（生成済み・**スタイルの基準**。発注時に参照画像として必ず添付）
- bld_castle — a grand multi-tiered Japanese castle keep with golden roof ornaments
- bld_farm — a small farmhouse beside golden rice paddies
- bld_ironmine — a mine entrance with iron ore carts and a glowing forge
- bld_barracks — a fortified drill yard with banners and spear racks

### 今回の発注（残り4棟・Lv1）
- bld_sawmill（伐採所／木材生産） — a wooden sawmill hut with a turning water wheel and a neat stack of freshly cut logs, an axe embedded in a chopping block
- bld_quarry（採石場／石材生産） — a small terraced stone quarry with hewn gray granite blocks and a simple wooden hoist crane, a pickaxe leaning against the blocks
- bld_lab（研究所／研究） — a scholar's study pavilion with unfurled scrolls, a brass armillary sphere and warm glowing paper lanterns, indigo-and-gold accents
- bld_warehouse（倉庫／保管容量） — a Japanese kura storehouse with white plaster walls, a black tiled roof and a heavy wooden door, stacked rice-straw sacks, barrels and wooden crates beside it

**納品**: 透過PNG 4枚を imageKey 名で（`bld_sawmill.png` / `bld_quarry.png` / `bld_lab.png` / `bld_warehouse.png`）。
取り込みはガチャタブ「🖼️ 画像取り込み」でキー指定 → IndexedDB保存（オリジン単位）。
全オリジンで初回から表示させたい場合は base64 埋め込み（未実装#11）をClaude側で実施する。

## 3. 資源アイコン（1:1、imageKey: res_*）※コード側は現状絵文字。将来差し替え用

```
[共通接頭辞] Game resource icon, single object, thick outline, slight 3D
bevel, on transparent background, 1:1 aspect. Object: {下記}
```
- res_food — a bundle of golden rice stalks with a rice bale
- res_wood — three stacked cut logs with visible growth rings
- res_stone — a neat pile of gray hewn stone blocks
- res_iron — dark iron ingots with metallic sheen
- res_diamond — a brilliant cyan-blue faceted diamond with sparkle (premium currency, extra shiny)

## 4. 聖地アイコン（1:1、imageKey: tile_holy）

```
[共通接頭辞] Sacred shrine site icon: an ancient torii gate on a floating
stone platform, surrounded by cherry blossom petals and golden divine light
pillars, mystical purple-gold color scheme, awe-inspiring holy atmosphere,
1:1 aspect.
```
