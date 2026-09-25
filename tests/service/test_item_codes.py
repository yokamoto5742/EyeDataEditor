import csv
import xml.etree.ElementTree as ET
from pathlib import Path

from service.item_codes import CSV_HEADER, collect_item_codes, write_csv

XML_TEXT = """<EyeCenter>
  <KensaPage>
    <Name>視力</Name>
    <KensaItem><Code></Code><Name></Name></KensaItem>
    <KensaItem><Code>101R</Code><Name>裸眼視力R</Name></KensaItem>
    <KensaItem><Code>1611R</Code><Name>CFF R</Name></KensaItem>
  </KensaPage>
  <KensaPage>
    <Name>CFF</Name>
    <KensaItem><Code>1611R</Code><Name>CFF R</Name></KensaItem>
    <KensaPage>
      <Name>子ページ</Name>
      <KensaItem><Code>910</Code><Name>910</Name></KensaItem>
    </KensaPage>
  </KensaPage>
  <OpeTab>
    <Name>術前</Name>
    <OpeTabItem><Code></Code><Name>術前視力_RLabel</Name></OpeTabItem>
    <OpeTabItem><Code>101</Code><Name>術前視力_R</Name></OpeTabItem>
  </OpeTab>
</EyeCenter>"""


def test_collect_item_codes() -> None:
    rows = collect_item_codes(ET.fromstring(XML_TEXT))
    assert rows == [
        ["検査", "視力", "101R", "裸眼視力R"],
        ["検査", "視力 / CFF", "1611R", "CFF R"],
        ["検査", "子ページ", "910", "910"],
        ["手術", "術前", "101", "術前視力_R"],
    ]


def test_write_csv_with_bom(tmp_path: Path) -> None:
    csv_path = tmp_path / "item_codes.csv"
    write_csv(csv_path, [["検査", "視力", "101R", "裸眼視力R"]])

    assert csv_path.read_bytes().startswith(b"\xef\xbb\xbf")
    with csv_path.open(encoding="utf-8-sig", newline="") as file:
        assert list(csv.reader(file)) == [CSV_HEADER, ["検査", "視力", "101R", "裸眼視力R"]]
