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
- 表示サイズは**約140px四方**（実測）。遠目でも誰か分かる**明快な配色・シルエット**にする
- **顔を大きく**。引きの戦場絵は縮小すると顔も武器も潰れて「色の塊」になる。
  UR第1弾で獄炎・業焔が引き構図で来たため、Claude側で中央寄りにクロップして救済した。
  背景の情景より**人物の顔＋兵種が分かる持ち物**を優先すること
- 納品は 512×512 か 1024×1024 の PNG（Claude側で256pxへ縮小・最適化して同梱する）

**同梱形式のメモ（Claude側の作業）**: カードは背景ありの全面イラストで透過不要のため、
建物用のPNG8（256色）ではなく **256px JPEG q80** で `art/card_*.jpg` に置き `embed_art.py` で同梱する。
256色に落とすとグラデーションが破綻するため。1枚あたり約22〜27KB。
ChatGPTからの原本（1254px・3MB級）はリポジトリにはコミットしない（26枚で80MB超になるため）。
再加工の可能性があるなら**ユーザー側でローカル保存しておくこと**。

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

**レア度は5段階（★1〜5）**。

| レア度 | 方向性 |
|---|---|
| **N（★1）** | 素朴な雑兵。粗末な革・布の装備、素朴な表情、くすんだ土色。演出なし |
| **R（★2）** | 一人前の武将。漆塗りの当世具足に家紋、自信のある表情、青の差し色と淡い逆光 |
| **SR（★3）** | 精鋭・名将。紫と銀の意匠、なびく羽織、紫の粒子エフェクト、強い逆光 |
| **SSR（★4）** | 伝説の英傑。金の装飾と神格的な意匠、金色の光条と舞う火の粉、圧倒的な威圧感 |
| **UR（★5）** | 神話級。**明らかに別格**。極彩の光背、周囲の空間が歪むような超常演出、<br>虹色のプリズム光、金と白の神装。一目で「別次元」と分かること |

### ★兵種を見た目に反映する（最重要）

**兵種は6種**。相性の三すくみが戦術の要なので、**一目で兵種が分かる**ことが重要。

| 兵種 | 見た目の指針 |
|---|---|
| 🛡️ **歩兵** infantry | 標準的な鎧に刀・打刀。バランスの取れた構え |
| 🔱 **槍兵** spear | 長槍・十文字槍。穂先を前に構え、対騎馬の間合い |
| 🐎 **騎兵** cavalry | 軽快な装備、馬具・鞭・手綱、風になびく装飾。躍動感 |
| 🏹 **弓兵** archer | 軽装、弓・矢筒・巻物などの遠距離／知略の小道具 |
| 🛡 **楯兵** shield | **大盾**が主役。重装で不動の構え。防御に特化した佇まい |
| 🏗️ **兵器** siege | **攻城兵器の操り手**。カタパルト・投石機・大砲・工兵道具。<br>人物より「機械」が目を引く構図でよい |

### 第一陣 26枚（納品済み）

| ファイル名 | 名前 | レア | 兵種 | 人物像 |
|---|---|---|---|---|
| `card_ur_kagurazaka` | 天佑・神楽坂 | UR★5 | 🐎騎兵 | **神託を受けた天馬の乗り手**。白銀と虹光の神装、背に星の光輪、すべてを見通す眼 |
| `card_ur_gouen` | 獄炎・業焔 | UR★5 | 🏗️兵器 | **炎を撃ち出す巨大攻城砲の操り手**。黒鉄と溶岩色、彗星のような火球、灼熱の粒子 |
| `card_ur_shirayuki` | 白雪・凍月 | UR★5 | 🏹弓兵 | **氷の大弓を引く静謐な女将**。白銀と淡青、舞う雪片、凍てつく月光の光背 |
| `card_ssr_tenba` | 覇王・天羽 | SSR★4 | 🐎騎兵 | 王冠と大剣を持つ覇王。金の甲冑、馬上の威容 |
| `card_ssr_byakuren` | 軍神・白蓮 | SSR★4 | 🏹弓兵 | 雷を纏う女神将。白と金、雷光の大弓 |
| `card_ssr_saya` | 聖女・沙耶 | SSR★4 | 🛡楯兵 | 光の**大盾**を掲げる聖女。桜の花びら、白金の法衣。守りの化身 |
| `card_ssr_benimaru` | 鬼神・紅丸 | SSR★4 | 🛡️歩兵 | 炎の金棒を担ぐ鬼神。赤黒の重装、燃える双眸 |
| `card_ssr_raiden` | 砲将・雷伝 | SSR★4 | 🏗️兵器 | **雷を仕込んだ大砲を操る砲術の将**。硝煙と稲光、火薬袋と点火縄 |
| `card_sr_soji` | 剣豪・宗二 | SR★3 | 🛡️歩兵 | 二刀を構える剣豪。紫銀の具足、鋭い眼光 |
| `card_sr_genba` | 策士・玄葉 | SR★3 | 🏹弓兵 | 軍配と巻物を持つ策士。羽根飾り、涼しげな知略の表情 |
| `card_sr_mitsuru` | 弓聖・美弦 | SR★3 | 🏹弓兵 | 大弓を引き絞る弓の名手。長い髪、集中した構え |
| `card_sr_gantetsu` | 猛将・岩鉄 | SR★3 | 🛡楯兵 | **岩の大盾**を構える巨漢。重装、豪快な笑み |
| `card_sr_kasumi` | 陰陽師・霞 | SR★3 | 🐎騎兵 | 呪符を操る陰陽師。三日月の意匠、翻る狩衣で疾走感 |
| `card_sr_yariha` | 槍将・槍羽 | SR★3 | 🔱槍兵 | **朱塗りの長槍**を構える精鋭。羽根飾りの兜、鋭い穂先 |
| `card_r_katsuma` | 侍大将・勝真 | R★2 | 🛡️歩兵 | 采配を執る侍大将。青の当世具足に家紋 |
| `card_r_kota` | 槍働き・虎太 | R★2 | 🔱槍兵 | 十文字槍の若武者。日焼けした精悍な顔 |
| `card_r_senri` | 参謀・千里 | R★2 | 🏹弓兵 | 書物を抱えた参謀。理知的な雰囲気、矢筒を背負う |
| `card_r_hayate` | 騎兵長・颯 | R★2 | 🐎騎兵 | 手綱を握る騎兵長。風になびくマント、疾走の気配 |
| `card_r_katayama` | 守将・堅山 | R★2 | 🛡楯兵 | **大盾**を構える守将。城門を背にした不動の構え |
| `card_r_ishizuchi` | 石槌・石鎚 | R★2 | 🏗️兵器 | **投石機を操る工兵**。縄と滑車、積まれた石弾、無骨な手 |
| `card_n_taichi` | 足軽・太一 | N★1 | 🛡️歩兵 | 刀を持つ若い足軽。粗末な陣笠と革鎧 |
| `card_n_yosuke` | 農兵・与助 | N★1 | 🔱槍兵 | **竹槍**を手にした農民兵。日焼けした素朴な顔 |
| `card_n_kosuzu` | 斥候・小鈴 | N★1 | 🐎騎兵 | 鈴を下げた少女斥候。身軽な装束 |
| `card_n_gonroku` | 衛兵・権六 | N★1 | 🛡楯兵 | **小盾**を持つ老衛兵。使い込まれた装備、門番の風格 |
| `card_n_maruta` | 新兵・丸太 | N★1 | 🏹弓兵 | 粗末な弓を持つ新兵。あどけない不安顔 |
| `card_n_nihei` | 輜重兵・荷平 | N★1 | 🏗️兵器 | 攻城具の**部材と縄を担ぐ輜重兵**。実直な働き者 |

**納品**: 第一陣は上記のファイル名で（例 `card_ur_gouen.png`）。
一度に全部でなくてよく、**UR3枚 → SSR5枚 → SR6枚 → R6枚 → N6枚** のように分割納品も可。
**まずUR3枚で画風とレア度差を確認**してから量産するのを推奨。
届いた分から Claude が正方形256pxへ縮小・PNG8最適化し、`tools/embed_art.py` で同梱する。

### 第二陣 12枚（第二ステージの新武将・**第4弾として発注**）

第二ステージ（皇都制圧後の異民族討伐）に向けた追加。**知将6枚と武将6枚**。
設計は [DESIGN_S2.md](DESIGN_S2.md) §2。

**★この12枚でいちばん大事なこと: 知将と武将を見た目で描き分ける**

| 型 | 見た目の方針 |
|---|---|
| **知将**（6枚） | **武器を主役にしない**。書物・巻物・呪符・軍配・羅針・筆・扇を持つ。<br>装束は軽く優美（狩衣・法衣・道服）。**線が細く、佇まいは静か**。<br>知略で戦う者なので、力任せの気配を出さない |
| **武将**（6枚） | 重装の甲冑・大型の武器（大剣・大槌・長槍・大砲）。**体格を大きく**、<br>構えは力強い。第一陣の武将系と同じ温度 |

**UR 6枚**（★5・虹色のプリズム光＋金と白の神装。第一陣URと同じ演出強度）

| ファイル名 | 名前 | 兵種 | 型 | 人物像 |
|---|---|---|---|---|
| `card_ur_kagen.png` | 臥龍・臥玄 | 🏹弓兵 | **知将** | 巨大な巻物を広げる隠者の軍師。伏せた龍の意匠、墨色と白銀、指先に灯る蒼い炎（**大火計**） |
| `card_ur_seiran.png` | 蒼嵐・青蘭 | 🐎騎兵 | **知将** | 蒼い雷を纏う女軍師。翻る薄衣、手には羅針と呪符、背後に渦巻く嵐（**落雷**） |
| `card_ur_mumei.png` | 無銘・霧明 | 🛡楯兵 | **知将** | 素性の知れぬ白面の策士。霧に沈む八角の陣形図、灰白と淡金（**八門**） |
| `card_ur_gouki.png` | 剛鬼・轟鬼 | 🛡️歩兵 | 武将 | 巨大な鉄槌を担ぐ大男。岩のような筋骨、砕けた鎧、雷鳴のような気迫（**奇襲**） |
| `card_ur_hayabusa.png` | 隼将・疾隼 | 🐎騎兵 | 武将 | 隼を象った兜の若き将。流線的な軽甲、疾走の残像、鋭い眼（**軍略**） |
| `card_ur_kongou.png` | 金剛・不動 | 🛡楯兵 | 武将 | 山のごとき巨盾を構える不動の将。金剛石の光、微動もしない構え（**八門**） |

**SSR 6枚**（★4・金の光条と舞う火の粉。URの虹光は使わない）

| ファイル名 | 名前 | 兵種 | 型 | 人物像 |
|---|---|---|---|---|
| `card_ssr_gyokuen.png` | 玉煙・玉艶 | 🏹弓兵 | **知将** | 煙管から紫煙を流す妖艶な女策士。玉の首飾り、揺れる煙が人影を描く（**天変**） |
| `card_ssr_suiun.png` | 水運・翠雲 | 🏗️兵器 | **知将** | 水路図を手にする治水の軍師。翡翠色の衣、背後に水門と攻城具（**大火計**） |
| `card_ssr_reimei.png` | 黎明・玲明 | 🔱槍兵 | **知将** | 夜明けの光を背負う若き軍師。細身の槍は背に、手には筆と兵書（**落雷**） |
| `card_ssr_tessai.png` | 鉄砕・鉄斎 | 🏗️兵器 | 武将 | 鉄塊を鋳る攻城技師。灼けた鉄と火花、無骨な腕、背に破城槌（**奇襲**） |
| `card_ssr_shunrai.png` | 迅雷・駿雷 | 🐎騎兵 | 武将 | 雷光のごとく駆ける騎将。稲妻の紋の旗、疾走する馬上（**軍略**） |
| `card_ssr_gagoze.png` | 牙吾・牙皇 | 🛡️歩兵 | 武将 | 牙を剥く獣面の兜の猛将。裂けた朱の陣羽織、荒々しい構え（**突撃**） |

**納品**: 上記のファイル名で。**UR3枚 → UR3枚 → SSR3枚 → SSR3枚** の分割納品も可。
まず**知将1枚と武将1枚**を先に出してもらい、**描き分けが成立しているか確認**してから量産するのを推奨。
届いた分から Claude が256px JPEG q80 へ変換し、`tools/embed_art.py` で同梱する（第一陣と同じ手順）。
12枚ぶんで index.html は約250KB増える見込み。


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

---

## 5. 盟主の容姿（1:1、imageKey: avatar_*）★発注中

ゲーム開始時に**男3・女3の計6枚**から選ぶ、プレイヤー自身の姿。
名前は入力させず **「盟主」で固定**（主役は率いられる武将たちで、盟主はその采配者、という立て付け）。

### 技術前提

- **1:1 の正方形・バストアップ**。カードと同じく `object-fit: cover` の正方枠に入る
- **表示は丸くマスクされる**（同盟タブで38px、チャットで16px の円）。
  **顔を中央に、円の外へ出る四隅には重要なものを置かない**
- **16pxでも誰か分かること**が最優先。カード（140px）よりさらに小さい。
  髪色・装束の主色をはっきり分け、顔を大きめに
- カード枠・縁取りは描かない（CSSが丸マスクと枠を付ける）
- 背景は塗ってよいが**無地に近い単色〜ごく淡いグラデ**が望ましい（円に切られるため）
- 納品は 512×512 PNG。Claude 側で 192px JPEG q82 に落として同梱する（カードと同じ方式）

### 共通プロンプト

```
512x512 px, 1:1 square. Bust-up portrait of a Japanese sengoku-fantasy
warlord, facing the viewer, head centered and large in the frame, shoulders
visible. Stylized mobile game art, clean bold shapes, warm painterly shading,
rich saturated colors. Plain near-solid background, subtle gradient only.
Composition must survive a CIRCULAR CROP: keep the face well inside the
center circle, nothing important in the corners.
NO card frame, NO border, NO text, NO watermark.
Character: {下記}
```

### 6枚の指定

**主色を6枚すべてで散らすこと**（16pxの円で見分けるための最重要点）。

| imageKey | 呼称 | 主色 | Character（英語プロンプトに入れる） |
|---|---|---|---|
| `avatar_m1` | 青年武官 | 濃紺＋銀 | young man in his twenties, short black hair, determined bright eyes, dark navy lamellar armor with silver trim, no helmet |
| `avatar_m2` | 壮年の将 | 深紅＋黒 | broad-shouldered man in his forties, thick black beard, weathered scar on cheek, deep crimson armor with black leather straps, commanding gaze |
| `avatar_m3` | 白髪の軍師 | 白＋薄紫 | elderly man with long white hair and beard, calm narrow eyes, white and pale-violet scholar robe, folding fan at chest |
| `avatar_f1` | 若き女将 | 若草＋金 | young woman in her late teens, high ponytail of chestnut hair, spirited smile, light green armored haori with gold cord |
| `avatar_f2` | 紅蓮の女傑 | 紅＋黒 | woman in her thirties, long crimson hair swept back, fierce confident expression, black armor with crimson under-robe |
| `avatar_f3` | 静謐の女軍師 | 白銀＋水色 | woman with straight silver-white hair and a hair ornament, serene half-closed eyes, pale blue court robe, quiet composed air |

### 注意

- 6枚は**同じ画角・同じ寄り・同じ光源**で揃えること。選択画面に3×2で並ぶので、
  1枚だけ引き構図や逆光だと浮く
- **年齢と髪色で見分けがつく**ようにしてほしい。装束の細部は16pxでは消える
- コード側は `AVATAR_DEFS`（[S02]）に配置済み。**未納品でも絵文字で完全に動く**ので、
  6枚まとめてでも1枚ずつでも構わない
