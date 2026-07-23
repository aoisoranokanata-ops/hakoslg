# 引き継ぎドキュメント（Opus向け）

このファイルだけで全体像と続きを把握できるように書いてある。コード全読は不要。
迷ったらまず [DESIGN.md](DESIGN.md)（設計意図）→ 本書（現状と次の一手）の順で読むこと。

## 0. ファイル構成

| ファイル | 役割 |
|---|---|
| `index.html` | ゲーム本体。CSS/JS完全インライン。**これ1枚で動く** |
| `sw.js` | Service Worker（唯一の分離ファイル。ブラウザ仕様上の必須例外） |
| `DESIGN.md` | 基本設計（データモデル・バランス方針・ゲームルール） |
| `IMAGE_PROMPTS.md` | ChatGPT画像生成用プロンプト集（imageKey対応表つき） |
| `HANDOVER.md` | 本書 |

## 1. アーキテクチャ概要

### モジュール構成
`index.html` 内の `<script>` はセクション `[S01]`〜`[S16]` に分割。**「[Sxx]」で検索すれば飛べる**。

```
[S01] CONFIG          全バランス定数。調整はここだけ触る
[S02] STATIC DEFS     建物/カード/役職/タイル種別の静的定義（セーブに含めない）
[S03] UTILS           $/fmt/toast等の汎用ヘルパー
[S04] PERSISTENCE     saveGame/loadGame(localStorage) + AssetDB(IndexedDB画像)
[S05] WORLD GEN       generateWorld / generateAIUsers（新規ゲーム時のみ実行）
[S06] STATE INIT      ★セーブデータ完全スキーマのコメントはここ。newGameState()
[S07] ECONOMY         getProdPerHour / applyEconomy / grantOfflineGains
[S08] BUILDINGS       getUpgradeCost / startUpgrade / finishUpgrades
[S09] MILITARY        getArmyPower / getTileDefense / startMarch / resolveMarches
[S10] GACHA           rollRarity(天井込み) / doGacha
[S11] ALLIANCE        recruitAI / setMemberRole / getAllianceBuffs
[S12] AI USERS        aiTickAll — ルールベース状態機械
[S13] UI: PANELS      renderHeader/City/Cards/Gacha/Alliance（タブ別DOM描画）
[S14] UI: MAP CANVAS  MapView（描画・パン・ズーム・タップ）+ openTileSheet
[S15] UI: ACTIONS     UIA.* — ボタンonclickの入口。全操作はここ経由
[S16] GAME LOOP       tick(1秒) / switchTab / boot
```

### データフロー（一方向）
```
ユーザー操作 → UIA.*（S15）→ ロジック関数（S07-S12）が S を変更
                                         ↓
毎秒 tick（S16）→ applyEconomy / finishUpgrades / resolveMarches / aiTickAll
                                         ↓
render*（S13-S14）が S を読んで DOM/canvas を再構築（差分更新なし・全再構築）
                                         ↓
10秒ごと saveGame → localStorage["hakoslg_save_v1"] に S をJSON一発保存
```

### 状態管理方針（最重要）
- **可変状態はグローバル `S` ただ1つ**。`S` をJSON.stringifyしたものがそのままセーブデータ。
- 静的定義（`BUILDING_DEFS`, `CARD_POOL`, `ROLE_DEFS` 等）は `S` に入れない。
  `S` 側は id/type/level 等の最小参照のみ持ち、コスト・生産量・戦力などの**派生値は毎回計算**（キャッシュ禁止）。
- 時刻は全て `Date.now()` のエポックms絶対値（`upgradeEndsAt`, `arriveAt`, `nextActionAt`）。
  → オフライン跨ぎ・タブ非アクティブでも自然に整合する。
- tickの dt は実測（`t - S.lastTickAt`）。起動時は `grantOfflineGains()` が12h上限で一括精算。

## 2. データスキーマ一覧

完全なフィールド仕様コメントは **[S06] の先頭コメントブロック** と各生成関数にある。要約:

```
S = {
  version, createdAt, lastSavedAt, lastTickAt,
  world: { size:40, tiles:[{x,y,type,level,ownerId}] },   // index = y*40+x
  //   type: empty|food|wood|stone|iron|holy|castle / ownerId: null|"player"|"ai_N"
  player: {
    castleLevel,                    // buildings内castle.levelのミラー
    buildings: [{id,type,level,upgradeEndsAt|null}],
    resources: {food,wood,stone,iron},   // float。表示floor。倉庫容量でキャップ
    diamonds,                       // float。キャップなし
    ownedTiles: [tileIndex],        // 自城タイルは含まない（ダイヤ計算対象）
    cards: [{uid,defId,obtainedAt}],// 重複所持可
    allianceId, marches: [{id,targetIdx,power,departAt,arriveAt}],
    gacha: {sinceSSR,total},
  },
  alliance: { id, name, members:[{id,role}] },   // プレイヤー同盟1つのみ
  aiUsers: [{id,name,color,x,y,castleLevel,personality,recruitable,
             allianceId,ownedTiles,nextActionAt,nextRecruitAt}],
  flags: { holyWon },
}
```

静的定義: `BUILDING_DEFS`（8種、cost/growth/time/prodBase）、`CARD_POOL`（20枚 N6/R5/SR5/SSR4）、
`ROLE_DEFS`（6役職とバフ乗数）、`TILE_DEFS`（描画定義）。

## 3. 命名規約・セクション見出し規約

- セクション見出し: `/* === [Sxx] 名前 === */` 形式。新セクションは番号を続けて追加
- 定数・静的定義: `UPPER_SNAKE`（`CONFIG`, `BUILDING_DEFS`）
- 関数: `camelCase` 動詞始まり。取得系 `getXxx`、描画系 `renderXxx`、開始系 `startXxx`
- ロジック関数の失敗は **「理由文字列を返す / 成功はnull」** 規約（`startUpgrade`等）。throwしない
- UI操作の入口は必ず `UIA.動詞`（inline onclickから呼ぶ）。ロジックを直接onclickに書かない
- localStorage/IndexedDBキーは必ず `hakoslg_` プレフィックス
- DOM id: タブページは `page-<tab名>`、その他はcamelCase

## 4. 実装済み / 未実装 / 次にやるべきこと

### ✅ 実装済み（動作確認済みの土台）
- [x] 40×40ワールド生成（距離帯レベル・資源分布・聖地×4・AI城10）
- [x] 資源生産（建物＋領有タイル）、倉庫キャップ、研究所の生産バフ
- [x] オフライン精算（12h上限・トースト表示）、10秒自動保存、visibilitychange保存
- [x] 建物アップグレード（コスト・実時間タイマー・本城レベルゲート）
- [x] 出兵→制圧（隣接ルール・防御力計算・行軍時間・失敗判定）、放棄
- [x] 領有→ダイヤ自動加算（レベル比例＋制圧ボーナス）、聖地勝利判定＋バナー
- [x] ガチャ（単発/10連・天井50・10連SR保証・排出結果UI）
- [x] AI状態機械（3性格の拡張/成長）、勧誘（成功率・クールダウン）、役職とバフ実装（将軍/都督/斥候）
- [x] マップUI（canvas・パン・ズーム・タップ詳細シート・出兵アニメーション）
- [x] 5タブUI（マップ/城/カード/ガチャ/同盟）、モバイル対応（safe-area・touch-action）
- [x] IndexedDB画像ストア＋取り込みUI（絵文字プレースホルダーで画像なしでも完動）
- [x] Service Worker（sw.js、file://ではスキップ）
- [x] **[S17] 城タブ箱庭ビュー** — 城塞区画に8棟配置、ドラッグ移動（グリッド吸着＋衝突回避）、
  座標を `S.player.buildings[].x/y` に保存、タップで強化シート、Lv6/11で外観ティア2/3化（`CONFIG.CITY_TIER_UP`）
- [x] **SAVE_VERSION 2 + migrateSave()** — 旧セーブの建物へ城内座標を非破壊補完

> ⚠️ 実装状況の最新・正本は **CLAUDE.md §5**。本リストはS16土台完成時点の記録＋S17追記。

### ⬜ 未実装（次にやるべきこと・優先度順）
1. **戦闘の深掘り**: 兵種・兵数の概念、出兵時のカード手動編成UI、複数部隊（`CONFIG.MAX_MARCHES`を兵舎Lvで増加）
2. **AI城への攻撃・AIからの反撃**: 現在AIはプレイヤー領を奪わない（`aiExpand`参照）。対人感を出すならここ
3. **研究ツリー**: 研究所は現状「生産+2%/Lv」のみ。`lab` 用の研究ツリーと軍師バフの有効化
4. **カード重複の救済**: 重複→強化素材/限界突破。現状は枚数表示のみ
5. **同盟の深掘り**: 同盟名変更、同盟ミッション、加入AIが援軍を出す等の実利
6. **チュートリアル/クエスト導線**: 初回起動時の誘導が皆無。目標リスト（本城Lv5にせよ等）
7. **セーブのエクスポート/インポートUI**（現状リセットのみ。localStorage直コピーで代用可）
8. **効果音・演出**: ガチャ演出（SSR時の勿体つけ）、制圧エフェクト
9. **画像アセット反映**: IMAGE_PROMPTS.md で生成→取り込みUIで登録（仕組みは動作済み）

### 変更時の注意
- バランス調整は `CONFIG` のみで完結させること（式に定数を直書きしない）
- `S` のスキーマを変えたら `CONFIG.SAVE_VERSION` を上げ、`loadGame()` にマイグレーション処理を書く
- `sw.js` の `CACHE` バージョンも `index.html` 更新時に上げる（更新が配信されない事故防止）

## 5. 既知の未確定点・設計上の判断保留

- **帰還行軍の省略**: 出兵は到着時に即解決・即帰還扱い。往復にするかは未決
- **敗北時のペナルティなし**: 出兵失敗は食料コストのみ。部隊損耗の概念は未導入
- **AIのオフライン進行**: AIの `nextActionAt` はオフライン中に1回分しか発火しない（まとめ実行しない）。
  意図的な簡略化（放置でAIに埋め尽くされるのを防ぐ）だが、要検討
- **役職の重複可**: 同役職を複数人に付与できるがバフは重複しない（`Math.max`）。制限するか未決
- **勝利後の継続プレイ**: 聖地1つでバナー表示のみ。「4聖地全制覇」「天下統一」等のエンドコンテンツ未設計
- **空地タイルのダイヤ寄与**: level×0.25で微量加算にした（[S07]）。0にするか未決
- **タイル資源分布が完全ランダム**: 偏りで序盤に特定資源が枯れる可能性。クラスタ生成にするか未決
- **file:// と GitHub Pages で localStorage が別オリジン**になる点はユーザー周知事項（セーブは引き継がれない）
