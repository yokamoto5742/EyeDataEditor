import argparse
from datetime import date, datetime
from functools import partial
from pathlib import Path

from openpyxl import load_workbook
from openpyxl.worksheet.worksheet import Worksheet

from service.postop_merge import (
    CsvRow,
    append_columns,
    group_by_id,
    load_csv,
    parse_date,
)


# 術眼の列（{eye} は R / L）のいずれかに値がある行だけを採用する
VAIOP_REQUIRED_COLUMNS = ("102{eye}", "109{eye}")
REF_REQUIRED_COLUMNS = ("{eye}_S",)


def has_any_value(row: CsvRow, columns: tuple[str, ...], eye: str) -> bool:
    return any((row.get(column.format(eye=eye)) or "").strip() for column in columns)


def select_latest_preop_row(
    rows: list[CsvRow],
    surgery_date: date,
    eye: str,
    required_columns: tuple[str, ...],
) -> CsvRow | None:
    """術眼の必須列に値があり手術日より前（当日を含まない）の行のうち、手術日に最も近い行を返す。

    同じ日に複数行ある場合は SEQ の小さい行を採用する。
    """
    candidates = [
        row
        for row in rows
        if parse_date(row["日付"]) < surgery_date
        and has_any_value(row, required_columns, eye)
    ]
    if not candidates:
        return None

    def sort_key(row: CsvRow) -> tuple[int, int]:
        return (
            (surgery_date - parse_date(row["日付"])).days,
            int(row.get("SEQ") or 0),
        )

    return min(candidates, key=sort_key)


def merge_preop_data(
    target_path: Path, vaiop_path: Path, refkeratometer_path: Path
) -> Path:
    workbook = load_workbook(target_path)
    sheet = workbook.active
    if not isinstance(sheet, Worksheet):
        raise ValueError(f"{target_path} にワークシートがありません")

    for prefix, csv_path, required_columns in (
        ("vaiop_pre", vaiop_path, VAIOP_REQUIRED_COLUMNS),
        ("ref_pre", refkeratometer_path, REF_REQUIRED_COLUMNS),
    ):
        fieldnames, rows = load_csv(csv_path)
        select_row = partial(
            select_latest_preop_row, required_columns=required_columns
        )
        append_columns(sheet, prefix, fieldnames, group_by_id(rows), select_row)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = target_path.with_name(f"{target_path.stem}_{timestamp}.xlsx")
    workbook.save(output_path)
    return output_path


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(
        description="targetdata.xlsx に手術日より前で最も近い vaiop・refkeratometer データを追加する"
    )
    parser.add_argument(
        "data_dir",
        nargs="?",
        type=Path,
        default=project_root / "data",
        help="targetdata.xlsx・vaiop.csv・refkeratometer.csv のあるディレクトリ",
    )
    args = parser.parse_args()

    output_path = merge_preop_data(
        args.data_dir / "targetdata.xlsx",
        args.data_dir / "vaiop.csv",
        args.data_dir / "refkeratometer.csv",
    )
    print(f"{output_path.resolve()} に出力しました")


if __name__ == "__main__":
    main()
