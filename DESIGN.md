# 箱庭クロニクル — 基本設計ドキュメント

ローカル完結・完全無料・オフラインで遊べる「自城育成（COC型）× マップ領土制圧（三國志真戦型）」ハイブリッド箱庭SLG。

- 配布形態: 単一HTMLファイル `index.html`（CSS/JSすべてインライン、CDN不使用）
  - 例外: Service Worker はブラウザ仕様上、別ファイルでの配信が必須のため `sw.js` のみ分離
- 保存: localStorage（セーブ本体）＋ IndexedDB（画像アセット）。キーはすべて `hakoslg_` プレフィックス
- 対象環境: iPhone Safari / GitHub Pages 配信を第一想定。file:// 直開きでも動作
- AI勢力: ルールベースの軽量な状態機械のみ。LLM・外部API不使用

## 1. ゲームの目的とコアループ

**目的**: 自城を強化し、マップ四隅にある「聖地」のいずれか1つを領有する（勝利）。

```
時間経過 → 資源生産（オフライン中はタイムスタンプ差分で一括加算）
   ↓
建物アップグレード（資源消費・実時間タイマー）
   ↓
出兵 → 隣接タイルを制圧 → ownedTiles に追加
   ↓
領有タイルの数×レベルに比例してダイヤが自動増加
   ↓
ダイヤでガチャ → カード獲得 → 部隊戦力アップ → より高レベルのタイルへ
   ↓
隣接AI城を勧誘して同盟に加入させ、役職バフを得る
   ↓
外周の聖地を制圧 → 勝利
```

## 2. 経済バランスの方針

- 「課金で渋いガチャ／ダイヤ」を反転させ、**領土拡大＝ダイヤ収入**にする。実課金要素ゼロ。
- ダイヤ収入 = Σ(領有タイルのレベル) × `DIAMOND_PER_TILELEVEL_PER_HOUR`（聖地はレベル×3換算）
  ＋ 新規制圧時ボーナス `DIAMOND_CAPTURE_BONUS_PER_LEVEL × level`
- 初期ダイヤ1000（単発10回分）。序盤から回せて、領土10枚もあれば毎時1回以上回せる想定。
- **全バランス定数は `index.html` 先頭の `CONFIG` オブジェクトに集約**。調整はここだけ触ればよい。

## 3. データモデル（スキーマ概要 — 完全版はコード内 [S02][S06] のコメント参照）

### World
- グリッド 40×40。`tiles` はフラット配列（index = y*40+x）
- tile = `{ x, y, type, level, ownerId }`
- type: `empty` / `food` / `wood` / `stone` / `iron`（資源4種）/ `holy`（聖地）/ `castle`（城）
- レベルは中心からのチェビシェフ距離の帯で決定（中心Lv1 → 外周Lv5、聖地Lv6）。四隅付近に聖地4つ。

### Player
`{ castleLevel, buildings[], resources{food,wood,stone,iron}, diamonds, ownedTiles[], cards[], allianceId, marches[], gacha{sinceSSR,total} }`
- `castleLevel` は本城ビルの level のミラー（表示用）。ownedTiles は自城タイルを**含まない**（ダイヤ計算対象のみ）。

### Building（インスタンス）
`{ id, type, level, upgradeEndsAt }` — prodRate / upgradeCost / upgradeTime は**静的定義 `BUILDING_DEFS` から都度計算**（セーブ肥大化防止・調整容易化のため）。
- 種類: castle(本城) / farm(農場) / sawmill(伐採所) / quarry(採石場) / ironMine(製鉄所) / barracks(兵舎) / lab(研究所) / warehouse(倉庫)
- 本城以外は「本城レベル以下まで」しか上げられない（ゲート）。

### Resource
食料・木材・石材・鉄（倉庫容量でキャップ）＋ ダイヤ（プレミア通貨、キャップなし）。内部は浮動小数で保持し表示時にfloor。

### Card
- 静的定義 `CARD_POOL`: `{ id, name, rarity(N/R/SR/SSR), atk(武力), int(知力), lead(統率), imageKey, emoji }`
- 所持インスタンス: `{ uid, defId, obtainedAt }`（重複所持可、一覧では枚数表示）
- 戦力 = `(武力*1.2 + 統率*1.0 + 知力*0.6) × レア倍率`。出撃編成は戦力上位5枚を自動採用。

### Gacha
- 排出率（甘め）: SSR 5% / SR 15% / R 35% / N 45%
- コスト: 単発100ダイヤ / 10連900ダイヤ（10連はSR以上1枚保証）
- 天井: 50連でSSR確定（SSR排出でリセット）

### Alliance
`{ id, name, members[{id, role}] }` — 役職: 盟主(プレイヤー固定) / 軍師 / 将軍 / 都督 / 斥候 / 一般
- 役職バフ（同盟内に1人でもいれば発動）: 将軍=戦力+10% / 都督=生産+10% / 斥候=行軍速度+20% / 軍師=（研究系・未実装プレースホルダ）

### AIUser
`{ id, name, castleLevel, x, y, personality, recruitable, allianceId, ownedTiles[], nextActionAt, color }`
- personality: `expander`（頻繁に拡張）/ `balanced`（拡張と内政半々）/ `turtle`（内政のみ）
- 挙動は「次回行動時刻が来たら1アクション」の軽量状態機械。隣接未所有タイルを1枚claimするか城レベルを上げるだけ。
- 勧誘: recruitable なAI城をタップ→食料コスト→成功率 = 0.5 + 0.06×(自城Lv − AI城Lv)（0.15〜0.95にクランプ）。

## 4. 戦闘（意図的に最小構成）

- 出兵は同時1部隊。行軍時間 = チェビシェフ距離 ÷ 速度（最低3秒）。帰還は省略（即時）。
- 判定は決定論: `自軍戦力 ≥ タイル防御力` なら制圧。
- 防御力 = `TILE_DEF_BASE × level^1.5`（空地は×0.3、AI領有は +AI城Lv×80、聖地は固定 `HOLY_DEF`）
- **隣接ルール**: 自領（自城含む）に8方向で隣接するタイルのみ出兵可（真戦式の地続き拡張）。
- 領有タイルは「放棄」可能（隣接経路の付け替え用）。

## 5. 永続化・オフライン設計

- セーブ: `localStorage["hakoslg_save_v1"]` にJSON一発保存。10秒ごと＋visibilitychange時に自動保存。
- オフライン収益: 起動時に `now − lastTickAt` を計算し、上限 `OFFLINE_CAP_HOURS`(12h) でキャップして一括加算。トーストで内訳表示。
- アップグレード・行軍は絶対時刻（`upgradeEndsAt` / `arriveAt`）で持つため、オフライン跨ぎでも自然に完了する。
- 画像: IndexedDB `hakoslg_assets` に `imageKey → Blob`。未登録キーは絵文字プレースホルダーで描画（画像なしで完動）。
- Service Worker: `sw.js` がキャッシュファースト配信（GitHub Pages でオフライン動作）。file:// では登録スキップ。

## 6. UI構成（モバイル最優先）

- 上部: 資源バー（食料/木材/石材/鉄/💎）固定
- 下部: 5タブ — マップ / 城 / カード / ガチャ / 同盟
- マップ: canvas 1枚。ドラッグでパン、＋/−ボタンでズーム、タップでタイル詳細シート（出兵/勧誘/放棄）
- 毎秒tickでヘッダー＋アクティブタブのみ再描画（軽量）
