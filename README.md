# 快感！配管クラフト（matsushita-pipe-craft）

松下工業様向けの採用・認知獲得用スマホWebゲーム。静的HTML 1枚で動き、Cloudflare Pages で配信する。

- 公開URL: https://matsushita-pipe-craft.pages.dev/
- 配信対象: `public/` のみ（`wrangler.toml` の `pages_build_output_dir`）

## 構成

```
public/
  index.html            ゲーム本体（OGP / X カード設定込み）
  ogp.png               リンクカード画像 1200x630
  apple-touch-icon.png  ホーム画面アイコン 180x180
tools/make_ogp.py       上記2画像の生成スクリプト（Pillow + 游ゴシック）
wrangler.toml           Cloudflare Pages 設定（将来の Functions / KV もここに追記）
```

## デプロイ

```sh
npx wrangler pages deploy
```

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
