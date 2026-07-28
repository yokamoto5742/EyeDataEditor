"""EyeData.xml の <Code> / <Name> を一覧化し、空き番号を表示するスクリプト。"""

import argparse
import csv
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from xml.etree.ElementTree import Element

XML_ENCODING = "cp932"
CODE_PATTERN = re.compile(r"^(\d+)(.*)$")


def load_root(xml_path: Path) -> Element:
    return ET.fromstring(xml_path.read_bytes().decode(XML_ENCODING))


def iter_code_entries(element: Element) -> list[tuple[str, str, str]]:
    """(要素名, コード, 名称) を再帰的に収集する。カンマ区切りのコードは分割する。"""
    entries: list[tuple[str, str, str]] = []
    for child in element:
        raw_code = (child.findtext("Code") or "").strip()
        if raw_code:
            name = (child.findtext("Name") or "").strip()
            for code in raw_code.split(","):
                if code.strip():
                    entries.append((child.tag, code.strip(), name))
        entries.extend(iter_code_entries(child))
    return entries


def aggregate_by_number(
    entries: list[tuple[str, str, str]],
) -> dict[int, tuple[set[str], set[str], set[str]]]:
    """数値部分をキーに (名称, 要素名, 接尾辞) を集約する。"""
    aggregated: dict[int, tuple[set[str], set[str], set[str]]] = {}
    for tag, code, name in entries:
        matched = CODE_PATTERN.match(code)
        if matched is None:
            continue
        number = int(matched.group(1))
        names, tags, suffixes = aggregated.setdefault(number, (set(), set(), set()))
        if name:
            names.add(name)
        tags.add(tag)
        if matched.group(2):
            suffixes.add(matched.group(2))
    return aggregated


def find_free_ranges(used: set[int], maximum: int) -> list[tuple[int, int]]:
    """1 から maximum までの未使用番号を連続範囲にまとめる。"""
    ranges: list[tuple[int, int]] = []
    start: int | None = None
    for number in range(1, maximum + 1):
        if number in used:
            if start is not None:
                ranges.append((start, number - 1))
                start = None
        elif start is None:
            start = number
    if start is not None:
        ranges.append((start, maximum))
    return ranges


def write_csv(
    csv_path: Path, aggregated: dict[int, tuple[set[str], set[str], set[str]]]
) -> None:
    with csv_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["コード", "名称", "要素", "接尾辞"])
        for number in sorted(aggregated):
            names, tags, suffixes = aggregated[number]
            writer.writerow(
                [
                    number,
                    " / ".join(sorted(names)),
                    " / ".join(sorted(tags)),
                    " / ".join(sorted(suffixes)),
                ]
            )


def format_range(start: int, end: int) -> str:
    return str(start) if start == end else f"{start}-{end}"


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(
        description="EyeData.xml のコード一覧と空き番号を出力する"
    )
    parser.add_argument(
        "xml",
        nargs="?",
        type=Path,
        default=project_root / "EyeData.xml",
        help="EyeData.xml のパス",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("eyedata_codes.csv"),
        help="出力する CSV ファイル",
    )
    args = parser.parse_args()

    entries = iter_code_entries(load_root(args.xml))
    aggregated = aggregate_by_number(entries)
    write_csv(args.output, aggregated)

    used = set(aggregated)
    maximum = max(used)
    free_ranges = find_free_ranges(used, maximum)
    free_count = sum(end - start + 1 for start, end in free_ranges)

    print(f"コード一覧を {args.output.resolve()} に出力しました")
    print(f"使用中: {len(used)} 件 (1-{maximum})  空き: {free_count} 件")
    print("空き番号:")
    print(", ".join(format_range(start, end) for start, end in free_ranges))


if __name__ == "__main__":
    main()
