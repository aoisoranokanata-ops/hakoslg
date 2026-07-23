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

**納品**: 透過PNG 8枚を imageKey 名で（`bld_castle.png` 等）。Lv1基本アートは全8棟実装・公開済み。

### ティア2/3（育った外観・imageKey: bld_<type>_t2 / _t3）

建物は Lv6 で**ティア2**、Lv11 で**ティア3**に外観が育つ（`artTierKey` が自動で切替。素材が無ければ基本アートにフォールバック）。
- **共通仕様は Lv1 と同一**（256px・透過・アイソメ3/4・上手前光・**Lv1の同建物を参照画像として必ず添付**）
- **同じ建物の成長**として描く。シルエットの家系を保ちつつ、t2=増築・材質向上・付帯物追加、t3=最も壮麗（金装飾・幟・規模最大）
- ゲーム内で t1→t2→t3 が並ぶので、**一目で「育った」と分かる差**をつける（サイズ感・要素数・豪華さ）

| type | ティア2（Lv6 / _t2） | ティア3（Lv11 / _t3） |
|---|---|---|
| castle 本城 | 天守が高くなり外壁と門を追加、幟を数本 | 金の装飾の壮大な城郭、複数の櫓と大幟、石垣 |
| farm 農場 | 母屋が大きくなり水車小屋と棚田を増設 | 蔵付きの豪農屋敷、風車、広大な黄金の田 |
| sawmill 伐採所 | 建屋拡大・水車2連・製材ピットと丸太増 | 大型製材所、複数水車、木材クレーンと大量の材木 |
| quarry 採石場 | 採掘段が深くなり大型クレーンと運搬車 | 石切り足場を組んだ大採石場、複数クレーン |
| ironmine 製鉄所 | 炉が大きくなり鞴（ふいご）と鉱石トロッコ | 煙突の並ぶ大溶鉱炉、赤熱する溶けた鉄 |
| barracks 兵舎 | 塀と物見櫓、訓練用の的を追加 | 砦の駐屯地、柵と複数の軍旗、武器庫 |
| lab 研究所 | 二層になり天体観測台と望遠鏡を追加 | 壮大な学問所の塔、大型渾天儀と多数の提灯 |
| warehouse 倉庫 | 蔵が大きくなり荷積み場と物資を増設 | 複数棟の大蔵群、荷役クレーン |

**納品**: 透過PNG（256px）を imageKey 名で。最大16枚（8棟×t2/t3）。
一度に全部でなくてよく、**t2を8棟 → 次にt3を8棟**のように分割納品も可。届いた分から Claude が `art/` へ入れ `tools/embed_art.py` で埋め込み反映する。

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
