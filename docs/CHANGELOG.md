# 変更履歴

このプロジェクトのすべての重要な変更は、このファイルに記録されます。

フォーマットは [Keep a Changelog](https://keepachangelog.com/ja/1.1.0/) に基づいており、
バージョン番号は [Semantic Versioning](https://semver.org/lang/ja/) に従っています。

## [Unreleased]

### 追加
- `service/postop_merge.py`: targetdata.xlsx の手術日から 21〜180 日後で最も近い vaiop.csv・refkeratometer.csv の行を右端に追加し、`targetdata_yyyymmdd_HHmmss.xlsx` として出力する処理を追加
- `service/item_codes.py`: EyeData.xml の検査（KensaItem）・手術（OpeTabItem）項目のコードと項目名を `item_codes.csv`（BOM 付き UTF-8）に一覧出力する処理を追加

### 変更
- `service/postop_merge.py`: 対象範囲を術後 21〜90 日に変更し、術後日数が 28 日に最も近い行（差が同じ場合は術後日数の大きい行）を選ぶように変更

### 修正
- `service/postop_merge.py`: CSV の「日付」列が 2 桁年（例: `24/03/23`）のため `ValueError` になる不具合を修正

## [1.0.0] - 2026-04-24
- 初版リリース
