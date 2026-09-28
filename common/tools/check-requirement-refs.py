#!/usr/bin/env python3
"""Kiểm tra tham chiếu yêu cầu giữa đặc tả và các luồng thiết kế.

Quy trình: common/requirements-design-sync.md mục 5.
Chạy từ bất kỳ đâu:  python common/tools/check-requirement-refs.py
Mã thoát: 0 = không có lỗi, 1 = có lỗi.
"""
import re
import sys
from pathlib import Path

DOCS = Path(__file__).resolve().parents[2]
SPEC = DOCS / "requirements" / "business-requirements.md"
TRACKER = DOCS / "common" / "requirements-change-tracker.md"
DESIGN_DIRS = ["system-design", "admin-web", "partner-web", "public-web"]
SKIP_FILES = {"changelog.md"}  # nhật ký lịch sử, không phải tài liệu hiện hành

ID = r"R-[A-Z]+-\d{3}"
SEC = r"\d+(?:\.\d+)*"
# Định nghĩa trong đặc tả: "## 2.2. [R-KB-001]" hoặc "- **2.2.3.12.** [R-KB-014]"
DEF_RE = re.compile(rf"(?:^#+\s+|^\s*-\s+\*\*)({SEC})\.(?:\*\*)?\s+\[({ID})\]", re.M)
# Trích dẫn chuẩn: "R-KB-014 (§2.2.3.12)"
CITE_RE = re.compile(rf"({ID})(?:\s*\(§\s*({SEC}))?")
SECT_RE = re.compile(rf"§\s*{SEC}")
TRACKER_MAX_RE = re.compile(r"\|\s*([A-Z]+)\s*\|\s*(R-[A-Z]+-(\d{3}))\s*\|")


def load_spec():
    ids, errors = {}, []
    for m in DEF_RE.finditer(SPEC.read_text(encoding="utf-8")):
        sec, rid = m.group(1), m.group(2)
        if rid in ids:
            errors.append(f"Đặc tả: ID {rid} bị trùng (§{ids[rid]} và §{sec})")
        ids[rid] = sec
    return ids, errors


def check_tracker(ids):
    errors = []
    if not TRACKER.exists():
        return errors
    actual = {}
    for rid in ids:
        mod, num = rid[2:].rsplit("-", 1)
        actual[mod] = max(actual.get(mod, 0), int(num))
    for m in TRACKER_MAX_RE.finditer(TRACKER.read_text(encoding="utf-8")):
        mod, num = m.group(1), int(m.group(3))
        if actual.get(mod, 0) > num:
            errors.append(f"Sổ theo dõi: ID lớn nhất đã cấp của {mod} ghi R-{mod}-{num:03d}, "
                          f"nhưng đặc tả đã có R-{mod}-{actual[mod]:03d}")
    return errors


def check_file(path, ids):
    errors = []
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        where = f"{path.relative_to(DOCS).as_posix()}:{n}"
        covered = []  # vị trí các § đã đi kèm ID
        for m in CITE_RE.finditer(line):
            rid, sec = m.group(1), m.group(2)
            if m.group(2) is not None:
                covered.append(line.index("§", m.start()))
            if rid not in ids:
                errors.append(f"{where}: {rid} không còn trong đặc tả (đã bỏ hoặc gõ sai)")
            elif sec is not None and sec.rstrip(".") != ids[rid]:
                errors.append(f"{where}: {rid} ghi §{sec}, số mục hiện tại là §{ids[rid]}")
        for m in SECT_RE.finditer(line):
            if m.start() not in covered:
                errors.append(f"{where}: trích dẫn {m.group(0)} không kèm ID")
    return errors


def main():
    ids, errors = load_spec()
    errors += check_tracker(ids)
    files = 0
    for d in DESIGN_DIRS:
        for path in sorted((DOCS / d).glob("*.md")):
            if path.name in SKIP_FILES:
                continue
            files += 1
            errors += check_file(path, ids)
    for e in errors:
        print(e)
    print(f"\nĐặc tả: {len(ids)} ID. Đã quét {files} file ở {', '.join(DESIGN_DIRS)}. "
          f"Lỗi: {len(errors)}.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
