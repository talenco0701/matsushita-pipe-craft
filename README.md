# 快感！配管クラフト（matsushita-pipe-craft）

松下工業様向けの採用・認知獲得用スマホWebゲーム。部材（直管・エルボ・T字管・立体交差）を選んで予算内で家まで配管する3Dパズル。
静的HTML 1枚で動き（3D描画は Three.js を CDN から読み込み）、Cloudflare Pages で配信する。

- 公開URL: https://matsushita-pipe-craft.pages.dev/
- 配信対象: `public/` のみ（`wrangler.toml` の `pages_build_output_dir`）

## 構成

```
public/
  index.html            ゲーム本体（Three.js 0.160 / OGP / X カード設定込み）
  ogp.png               リンクカード画像 1200x630
  apple-touch-icon.png  ホーム画面アイコン 180x180
tools/make_ogp.py       上記2画像の生成スクリプト（Pillow + 游ゴシック）
tools/ogp_scene.jpg     OGP画像の右側に使うゲーム画面のキャプチャ
wrangler.toml           Cloudflare Pages 設定（将来の Functions / KV もここに追記）
```

## デプロイ

```sh
npx wrangler pages deploy
```

Windows PowerShell でスクリプト実行が禁止されている環境では `npx` が `npx.ps1` の読み込みで失敗するため、`npx.cmd wrangler ...` と打つ（`wrangler login` も同様）。

Pages プロジェクトは作成済み（wrangler 4.151 以降は Workers へ委譲されるため、作成時のみ `--force` で旧来の Pages として作成した）。以降のコマンドに `--force` は不要。

`main` ブランチから実行すると本番（上記URL）に反映される。別ブランチ名を付けるとプレビューURLになる:

```sh
npx wrangler pages deploy --branch=preview
```

## OGP画像の作り直し

```sh
python tools/make_ogp.py
```

公開URLが変わった場合は `public/index.html` の `canonical` / `og:url` / `og:image` / `twitter:image` を書き換える。
SNS側はキャッシュするため、更新後は各サービスのカード確認ツールで再取得させる。

## ゲームの調整箇所（public/index.html）

- `PARTS`：部材の値段
- `STAGES`：盤面・予算・プロの見積り・曲がりの目安
- `BONUSES`：職人ボーナスの点数と理由の文言（現場の考え方として松下工業様に確認してもらう）
- `MEMOS`：クリア時の「松下社長の現場メモ」
- `RECRUIT_URL`：最終画面の「求人を見る」ボタンのリンク先（空なら非表示）
