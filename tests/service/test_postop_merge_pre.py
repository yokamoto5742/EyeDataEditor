from datetime import date

from service.postop_merge_pre import (
    REF_REQUIRED_COLUMNS,
    VAIOP_REQUIRED_COLUMNS,
    select_latest_preop_row,
)

SURGERY_DATE = date(2026, 1, 1)


def make_row(day: str, seq: str = "1", **values: str) -> dict[str, str]:
    return {"日付": day, "ID": "1", "SEQ": seq, **values}


def select_ref(rows: list[dict[str, str]], eye: str = "R") -> dict[str, str] | None:
    return select_latest_preop_row(rows, SURGERY_DATE, eye, REF_REQUIRED_COLUMNS)


def test_select_latest_preop_row_excludes_surgery_date() -> None:
    before = make_row("25/12/31", R_S="1.0")
    same_day = make_row("26/01/01", R_S="1.0")
    after = make_row("26/01/02", R_S="1.0")
    assert select_ref([before, same_day, after]) == before
    assert select_ref([same_day]) is None


def test_select_latest_preop_row_picks_closest_before() -> None:
    old = make_row("24/05/01", R_S="1.0")
    recent = make_row("25/12/20", R_S="1.0")
    assert select_ref([recent, old]) == recent


def test_select_latest_preop_row_picks_smallest_seq_on_same_day() -> None:
    later_seq = make_row("25/12/20", seq="3", R_S="1.0")
    earlier_seq = make_row("25/12/20", seq="2", R_S="1.0")
    assert select_ref([later_seq, earlier_seq]) == earlier_seq


def test_select_latest_preop_row_skips_rows_without_operated_eye_value() -> None:
    measured = make_row("25/12/01", R_S="1.0", L_S="")
    other_eye_only = make_row("25/12/20", R_S="", L_S="-0.5")
    assert select_ref([measured, other_eye_only], eye="R") == measured
    assert select_ref([measured, other_eye_only], eye="L") == other_eye_only


def test_select_latest_preop_row_accepts_either_vaiop_column() -> None:
    only_109 = make_row("25/12/20", **{"102R": "", "109R": "15"})
    only_102 = make_row("25/12/10", **{"102R": "0.5", "109R": ""})
    neither = make_row("25/12/30", **{"102R": "", "109R": ""})
    rows = [only_102, only_109, neither]
    assert select_latest_preop_row(rows, SURGERY_DATE, "R", VAIOP_REQUIRED_COLUMNS) == only_109
    assert select_latest_preop_row([only_102], SURGERY_DATE, "R", VAIOP_REQUIRED_COLUMNS) == only_102
