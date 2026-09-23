---
description: テスト実行コマンドとテスト方針
---

## テスト実行コマンド

依存関係は uv で管理しているため、pytest も `uv run` 経由で実行する。

```bash
# 全件
uv run pytest tests/ -v --tb=short

# 単一ファイル
uv run pytest tests/service/test_eyedata_codes.py -v

# 単一テスト
uv run pytest tests/service/test_eyedata_codes.py::test_find_free_ranges -v

# カバレッジ付き
uv run pytest tests/ -v --tb=short --cov=service --cov=utils --cov-report=html
```
