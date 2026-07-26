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

**すべて正方形（1:1）で生成する**（カード・建物・アイコンとも）。

## 1. キャラカード（imageKey: card_*）

### 技術前提（厳守）

- **1:1 の正方形・バストアップ**（顔と上半身が中心）。
  ゲーム側の表示枠は正方形で `object-fit: cover` のため、**縦長で描くと顔が切れる**
- **カード枠・レア度の縁取りは描かない**。枠と発光はゲーム側のCSSが付ける（描くと二重になる）
- **背景は塗ってよい**（透過不要）。ただし人物が主役で、背景は雰囲気を出す程度
- 表示サイズは**約152px四方**。遠目でも誰か分かる**明快な配色・シルエット**にする
- 納品は 512×512 か 1024×1024 の PNG（Claude側で256pxへ縮小・最適化して同梱する）

### 共通プロンプト（全カードで使う）

```
512x512 px, 1:1 square. Bust-up portrait of a Japanese sengoku-fantasy
character, facing the viewer, head and shoulders centered and fully inside
the frame. Stylized mobile game art, clean bold shapes, warm painterly
shading, rich saturated colors, strong readable silhouette.
NO card frame, NO border, NO text, no watermark, no UI elements.
Simple atmospheric background that does not distract from the face.
Character: {下記}
```

### レア度で「格」を変える（枠ではなく人物と光で表現）

| レア度 | 方向性 |
|---|---|
| **N** | 素朴な雑兵。粗末な革・布の装備、素朴な表情、くすんだ土色。演出なし |
| **R** | 一人前の武将。漆塗りの当世具足に家紋、自信のある表情、青の差し色と淡い逆光 |
| **SR** | 精鋭・名将。紫と銀の意匠、なびく羽織、紫の粒子エフェクト、強い逆光 |
| **SSR** | 伝説の英傑。金の装飾と神格的な意匠、金色の光条と舞う火の粉、圧倒的な威圧感 |

### ★兵種を見た目に反映する（今回の重要ポイント）

ゲームに**兵種の三すくみ**が入ったため、**一目で兵種が分かる**ことが重要。

| 兵種 | 見た目の指針 |
|---|---|
| 🛡️ **歩兵** infantry | 重めの鎧、盾・槍・刀。どっしり構えた姿勢 |
| 🐎 **騎兵** cavalry | 軽快な装備、馬具・鞭・手綱、風になびく装飾。躍動感 |
| 🏹 **弓兵** archer | 軽装、弓・矢筒・巻物などの遠距離/知略の小道具 |

### 全20枚の一覧（この通りに発注）

| imageKey | 名前 | レア | 兵種 | 人物像 |
|---|---|---|---|---|
| `card_ssr_tenba` | 覇王・天羽 | SSR | 🐎騎兵 | 王冠と大剣を持つ覇王。金の甲冑、馬上の威容 |
| `card_ssr_byakuren` | 軍神・白蓮 | SSR | 🏹弓兵 | 雷を纏う女神将。白と金、雷光の大弓 |
| `card_ssr_saya` | 聖女・沙耶 | SSR | 🛡️歩兵 | 光の錫杖を持つ聖女。桜の花びら、白金の法衣に軽い護り |
| `card_ssr_benimaru` | 鬼神・紅丸 | SSR | 🛡️歩兵 | 炎の金棒を担ぐ鬼神。赤黒の重装、燃える双眸 |
| `card_sr_soji` | 剣豪・宗二 | SR | 🛡️歩兵 | 二刀を構える剣豪。紫銀の具足、鋭い眼光 |
| `card_sr_genba` | 策士・玄葉 | SR | 🏹弓兵 | 軍配と巻物を持つ策士。羽根飾り、涼しげな知略の表情 |
| `card_sr_mitsuru` | 弓聖・美弦 | SR | 🏹弓兵 | 大弓を引き絞る弓の名手。長い髪、集中した横顔気味の構え |
| `card_sr_gantetsu` | 猛将・岩鉄 | SR | 🛡️歩兵 | 大盾と大斧の巨漢。岩のような重装、豪快な笑み |
| `card_sr_kasumi` | 陰陽師・霞 | SR | 🐎騎兵 | 呪符を操る陰陽師。三日月の意匠、翻る狩衣で疾走感 |
| `card_r_katsuma` | 侍大将・勝真 | R | 🛡️歩兵 | 采配を執る侍大将。青の当世具足に家紋 |
| `card_r_kota` | 槍働き・虎太 | R | 🛡️歩兵 | 十文字槍の若武者。日焼けした精悍な顔 |
| `card_r_senri` | 参謀・千里 | R | 🏹弓兵 | 書物を抱えた参謀。眼鏡的な理知の雰囲気、矢筒を背負う |
| `card_r_hayate` | 騎兵長・颯 | R | 🐎騎兵 | 手綱を握る騎兵長。風になびくマント、疾走の気配 |
| `card_r_katayama` | 守将・堅山 | R | 🛡️歩兵 | 大盾を構える守将。城門を背にした不動の構え |
| `card_n_taichi` | 足軽・太一 | N | 🛡️歩兵 | 槍を持つ若い足軽。粗末な陣笠と革鎧 |
| `card_n_yosuke` | 農兵・与助 | N | 🛡️歩兵 | 鍬を手にした農民兵。日焼けした素朴な顔 |
| `card_n_kosuzu` | 斥候・小鈴 | N | 🐎騎兵 | 鈴を下げた少女斥候。身軽な装束 |
| `card_n_gonroku` | 衛兵・権六 | N | 🛡️歩兵 | 門を守る老衛兵。使い込まれた槍と履物 |
| `card_n_maruta` | 新兵・丸太 | N | 🏹弓兵 | 木刀と粗末な弓の新兵。あどけない不安顔 |
| `card_n_nihei` | 輜重兵・荷平 | N | 🏹弓兵 | 荷を背負う輜重兵。矢束を運ぶ実直な男 |

**納品**: `card_<レア>_<名前>.png` の形式で（例 `card_ssr_tenba.png`）。
一度に全部でなくてよく、**SSR4枚 → SR5枚 → R5枚 → N6枚** のように分割納品も可。
届いた分から Claude が正方形256pxへ縮小・PNG8最適化し、`tools/embed_art.py` で同梱する。

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
