import argparse
import csv
import xml.etree.ElementTree as ET
from pathlib import Path
from xml.etree.ElementTree import Element

# data/EyeData.xml は BOM 付き UTF-8
XML_ENCODING = "utf-8-sig"
# Excel で文字化けせずに開けるよう BOM 付きで出力する
CSV_ENCODING = "utf-8-sig"
CSV_HEADER = ["種別", "ページ名", "コード", "項目名"]
# (種別, ページ要素名, 項目要素名)
CATEGORIES = (
    ("検査", "KensaPage", "KensaItem"),
    ("手術", "OpeTab", "OpeTabItem"),
)
PAGE_NAME_SEPARATOR = " / "


def load_root(xml_path: Path) -> Element:
    return ET.fromstring(xml_path.read_bytes().decode(XML_ENCODING))


def collect_item_codes(root: Element) -> list[list[str]]:
    """(種別, ページ名, コード, 項目名) の行を出現順に返す。

    同じ種別で同じコードが複数ページにある場合は 1 行にまとめ、ページ名を連結する。
    コードが空の要素（ラベル）は除外する。
    """
    rows: list[list[str]] = []
    for category, page_tag, item_tag in CATEGORIES:
        pages_by_code: dict[str, list[str]] = {}
        names_by_code: dict[str, str] = {}
        for page in root.iter(page_tag):
            page_name = (page.findtext("Name") or "").strip()
            for item in page.findall(item_tag):
                code = (item.findtext("Code") or "").strip()
                if not code:
                    continue
                names_by_code.setdefault(code, (item.findtext("Name") or "").strip())
                page_names = pages_by_code.setdefault(code, [])
                if page_name not in page_names:
                    page_names.append(page_name)
        for code, page_names in pages_by_code.items():
            rows.append(
                [category, PAGE_NAME_SEPARATOR.join(page_names), code, names_by_code[code]]
            )
    return rows


def write_csv(csv_path: Path, rows: list[list[str]]) -> None:
    with csv_path.open("w", encoding=CSV_ENCODING, newline="") as file:
        writer = csv.writer(file)
        writer.writerow(CSV_HEADER)
        writer.writerows(rows)


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(
        description="EyeData.xml の検査・手術項目のコードと項目名を CSV に出力する"
    )
    parser.add_argument(
        "xml",
        nargs="?",
        type=Path,
        default=project_root / "data" / "EyeData.xml",
        help="EyeData.xml のパス",
    )
    args = parser.parse_args()

    rows = collect_item_codes(load_root(args.xml))
    csv_path = args.xml.with_name("item_codes.csv")
    write_csv(csv_path, rows)
    print(f"{len(rows)} 件を {csv_path.resolve()} に出力しました")


if __name__ == "__main__":
    main()
