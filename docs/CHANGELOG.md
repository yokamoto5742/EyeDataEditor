# 変更履歴

このプロジェクトのすべての重要な変更は、このファイルに記録されます。

フォーマットは [Keep a Changelog](https://keepachangelog.com/ja/1.1.0/) に基づいており、
バージョン番号は [Semantic Versioning](https://semver.org/lang/ja/) に従っています。

## [Unreleased]

### 追加
- `service/postop_merge.py`: targetdata.xlsx の手術日から 21〜180 日後で最も近い vaiop.csv・refkeratometer.csv の行を右端に追加し、`targetdata_yyyymmdd_HHmmss.xlsx` として出力する処理を追加

## [1.0.0] - 2026-04-24
- 初版リリース
