# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## コマンド

依存関係は uv で管理する。すべてのツールは `uv run` 経由で実行する。

```bash
uv sync                    # 依存関係の同期
uv run pyright             # 型チェック
uv run ruff check .        # lint
uv run ruff format .       # フォーマット
```

テストコマンドは `.claude/rules/testing.md` を参照（同じく `uv run` 経由）。

## 構成と注意点

- `app/` `service/` はまだ骨組み。実装済みは `utils/config_manager.py` と `utils/log_rotation.py` のみ。
- 設定ファイルは `utils/config.ini`。PyInstaller で凍結すると `sys._MEIPASS` 直下に配置されるため、パスを直書きせず `utils.config_manager.ConfigManager` / `CONFIG_PATH` を経由して解決する。
- ログは `utils.log_rotation.setup_logging()` で初期化する。`logs/` は gitignore 済み。
- バージョンは `app/__init__.py` の `__version__` / `__date__` に定義する。
- pyright は standard モードで、未使用の import・変数がエラーになる。対象は `app` `service` `utils` `tests` で、`scripts/` は対象外。

## Git

- `main` に直接コミットする（ブランチ・PR 運用はしない）。
- 変更は `docs/CHANGELOG.md`（Keep a Changelog 準拠）の `[Unreleased]` に追記する。
