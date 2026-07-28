---
description: テスト実行コマンドとテスト方針
---

## テスト実行コマンド

```bash
# 全件
uv run pytest tests/ -v --tb=short

# 単一ファイル
uv run pytest tests/services/test_summary_service.py -v

# 単一テスト
uv run pytest tests/services/test_summary_service.py::test_generate_summary -v

# カバレッジ付き
uv run pytest tests/ -v --tb=short --cov=app --cov-report=html
```
