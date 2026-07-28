# 変更履歴

このプロジェクトのすべての重要な変更は、このファイルに記録されます。

フォーマットは [Keep a Changelog](https://keepachangelog.com/ja/1.1.0/) に基づいており、
バージョン番号は [Semantic Versioning](https://semver.org/lang/ja/) に従っています。

## [Unreleased]

### Added
- `../service/eyedata_codes.py`: EyeData.xml の `<Code>` / `<Name>` を CSV に一覧化し、空き番号をコンソールに表示する

### Changed
- `../service/eyedata_codes.py`: `SumStaff` / `Kind4` 要素を出力対象から除外し、CSV を 要素・コード・名称・接尾辞 の列順で要素→コードの昇順に出力する

## [1.0.0] - 2026-04-24
- 初版リリース
