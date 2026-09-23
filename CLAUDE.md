# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.必ず日本語で回答してください。

## 概要

眼科マスタ `EyeData.xml`（cp932）を解析し、XML タグごとにコードと名称を集計して
タグ別シートの Excel を出力し、未使用のコード番号を標準出力に表示するツール。

## コマンド

依存関係は uv で管理する。すべてのツールは `uv run` 経由で実行する。

```bash
uv sync                # 依存関係の同期
uv run pyright         # 型チェック
uv run pytest -v       # テスト（詳細は .claude/rules/testing.md）
```

lint / formatter は導入していない（ruff・black・mypy いずれも未設定）。
型チェックは pyright のみで行う。

実行:

```bash
uv run python -m service.eyedata_codes path\to\EyeData.xml
```

## 構成と注意点

- `service/` が業務ロジック、`utils/` が基盤（設定・ログ）、`app/` はバージョン定義のみ。
  `scripts/` は開発用のツリー生成スクリプトで pyright の対象外。
- 設定ファイルのパスを直書きしない。PyInstaller で凍結すると `sys._MEIPASS` 直下に
  配置されるため、必ず `utils.config_manager.ConfigManager` / `CONFIG_PATH` を経由する。
- `get_config_value` は `fallback` の型から戻り値の型を推論する。`int` や `bool` が
  必要なときは必ずその型の `fallback` を渡す。
- ログは `utils.log_rotation.setup_logging()` で初期化する（現時点ではどこからも
  呼ばれていない）。`logs/` は gitignore 済み。
- バージョンは `app/__init__.py` の `__version__` に定義する。
- pyright は standard モード。未使用の import・変数はエラーになる。
  対象は `app` `service` `utils` `tests`。

## Git

- `main` に直接コミットする（ブランチ・PR 運用はしない）。
- 変更は `docs/CHANGELOG.md`（Keep a Changelog 準拠）の `[Unreleased]` に追記する。

## 規約

コーディング規約・コミットメッセージ・テストコマンド・応答スタイルは
`.claude/rules/` 配下に分割して定義している（自動で読み込まれる）。
