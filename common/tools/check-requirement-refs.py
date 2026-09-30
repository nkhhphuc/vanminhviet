#!/usr/bin/env python3
"""Kiểm tra tham chiếu giữa đặc tả, tài liệu thiết kế và các luồng thiết kế.

Quy trình: common/requirements-design-sync.md mục 2.3, 2.4, 2.5 và 5.
Chạy từ bất kỳ đâu:  python common/tools/check-requirement-refs.py [--luong <tên luồng>]
  --luong  chỉ báo lỗi trong các file của một luồng (system-design, admin-web, partner-web,
           public-web); vẫn đọc toàn bộ đặc tả và tài liệu thiết kế để đối chiếu.
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

SEC = r"\d+(?:\.\d+)*"
RID = r"R-[A-Z]+-\d{3}"
DID = r"D-(?:SD0[1-9]|ADM|PRT|PUB)-\d{3}"

# Định nghĩa trong đặc tả: "## 2.2. [R-KB-001]" hoặc "- **2.2.3.12.** [R-KB-014]"
SPEC_DEF_RE = re.compile(rf"(?:^#+\s+|^\s*-\s+\*\*)({SEC})\.(?:\*\*)?\s+\[({RID})\]", re.M)
# Tiêu đề trong tài liệu thiết kế: "### 2.1. [D-SD03-001] ..." hoặc "## 4.1 Màn hình ..."
HEAD_RE = re.compile(rf"^#+\s+({SEC})\.?\s+(?:\[([^\]]+)\])?")
# Trích dẫn kèm ID: "R-KB-014 (§2.2.3.12)", "D-ADM-019 (¶4.19)"
R_CITE_RE = re.compile(rf"({RID})(?:\s*\(([§¶])\s*({SEC}))?")
D_CITE_RE = re.compile(rf"({DID})(?:\s*\(([§¶])\s*({SEC}))?")
SYM_RE = re.compile(rf"([§¶])\s*({SEC})")
# Tên tài liệu thiết kế đứng ngay trước "¶": `03`, `03-….md`, system-design/03-….md, admin-web, …
FILE_TAG = (r"(?:`(0[1-9])`|(0[1-9])-[a-z0-9-]+(?:\.md)?`?"
            r"|`?((?:admin|partner|public)-web)(?:/[a-z0-9-]+\.md)?`?)")
TAG_BEFORE_SYM_RE = re.compile(FILE_TAG + r"\s*$")
# Dạng cũ "admin-web 4.19", "`admin-web` 4.19"
OLD_WEB_RE = re.compile(r"`?\b((?:admin|partner|public)-web)`?\s+(\d+\.\d+)")
MUC_RE = re.compile(rf"\b[Mm]ục\s+({SEC})")
# Tên file/tài liệu đứng gần "mục N" để xác định "mục N" thuộc tài liệu nào
NEAR_RE = re.compile(r"`(0[1-9])`|\b(0[1-9])-[a-z0-9-]+\.md|tài liệu (0[1-9])\b"
                     r"|\b((?:admin|partner|public)-web)\b(?!/00)"
                     r"|(business-requirements|đặc tả|\bBR\b)"
                     r"|([\w./-]+\.md)")
# operationId (mục 2.5): tiền tố theo đoạn đầu của path
OP_PREFIXES = ["auth", "identity", "knowledge", "encyclopedia", "assistant", "shared", "public",
               "clientSettings", "internal", "gateway"]
OP = rf"(?:{'|'.join(OP_PREFIXES)})\.[a-z][A-Za-z0-9]*"
OP_FMT_RE = re.compile(r"[a-z][A-Za-z]*\.[a-z][A-Za-z0-9]*")
METHOD = r"(?:GET|POST|PUT|PATCH|DELETE)"
EP_HEAD_RE = re.compile(r"^\|\s*Method\s*\|\s*Path\s*\|")
EP_HEAD06_RE = re.compile(r"^\|.*\|\s*Endpoint\s*\|")
EP_ROW_RE = re.compile(rf"^\|\s*({METHOD})\s*\|\s*`([^`]+)`\s*\|([^|]*)\|")
EP_ROW06_RE = re.compile(rf"^\|\s*\d+\s*\|[^|]*\|\s*`({METHOD}) ([^`]+)`\s*\|([^|]*)\|")
OP_BULLET_RE = re.compile(r"^- operationId: `([^`]+)`")
OP_INLINE_RE = re.compile(rf"`({METHOD}) ([^`]+)` \(operationId `([^`]+)`\)")
OP_CITE_RE = re.compile(rf"`({OP})`(\s*\(({DID})\))?")
# Trích endpoint bằng method + path: `POST /knowledge/...`, `GET .../{id}`
MP_RE = re.compile(rf"`({METHOD}) ((?:/|\.\.\.|…)[^`\s]*)[^`]*`")
MP_AFTER_OP_RE = re.compile(rf"`{OP}`\s*—\s*$")
TRACKER_R_RE = re.compile(r"\|\s*([A-Z]+)\s*\|\s*(R-[A-Z]+-(\d{3}))\s*\|")
TRACKER_D_RE = re.compile(r"\|\s*((?:SD0[1-9]|ADM|PRT|PUB))\s*\|\s*(D-[A-Z0-9]+-(\d{3}))\s*\|")

WEB_FILES = {"ADM": "admin-web/admin-web-design.md",
             "PRT": "partner-web/partner-web-design.md",
             "PUB": "public-web/public-web-layout.md"}
WEB_CODE = {"admin-web": "ADM", "partner-web": "PRT", "public-web": "PUB"}


def design_files():
    """{mã file: Path} của các tài liệu thiết kế (mục 2.4)."""
    files = {}
    for p in sorted((DOCS / "system-design").glob("0[1-9]-*.md")):
        files[f"SD{p.name[:2]}"] = p
    for code, rel in WEB_FILES.items():
        if (DOCS / rel).exists():
            files[code] = DOCS / rel
    return files


def load_spec():
    ids, errors = {}, []
    for m in SPEC_DEF_RE.finditer(SPEC.read_text(encoding="utf-8")):
        sec, rid = m.group(1), m.group(2)
        if rid in ids:
            errors.append(f"Đặc tả: ID {rid} bị trùng (§{ids[rid]} và §{sec})")
        ids[rid] = sec
    return ids, errors


def load_design(files):
    """Trả về: did -> (mã file, số mục); mã file -> {số mục: did hoặc None}."""
    dids, secs, errors = {}, {}, []
    for code, path in files.items():
        secs[code] = {}
        rel = path.relative_to(DOCS).as_posix()
        for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            m = HEAD_RE.match(line)
            if not m:
                continue
            sec, tag = m.group(1), m.group(2)
            did = tag if tag and re.fullmatch(DID, tag) else None
            if tag and tag.startswith("D-") and not did:
                errors.append(f"{rel}:{n}: ID [{tag}] sai định dạng D-<mã file>-NNN")
            secs[code].setdefault(sec, did)
            if not did:
                continue
            if did.split("-")[1] != code:
                errors.append(f"{rel}:{n}: {did} đặt trong file mã {code}, sai mã file")
            if did in dids:
                errors.append(f"{rel}:{n}: ID {did} bị trùng (¶{dids[did][1]} và ¶{sec})")
            dids[did] = (code, sec)
    return dids, secs, errors


def op_prefix(path):
    """Tiền tố operationId đúng theo path (mục 2.5)."""
    seg = path.strip("/").split("/")[0]
    if seg == "v1":
        return "gateway"
    return re.sub(r"-([a-z])", lambda m: m.group(1).upper(), seg)


_last_head = {}  # tiêu đề gần nhất theo file, để đọc endpoint của dòng "- operationId: …"


def norm_path(p):
    """Bỏ tiền tố nhóm route, query và tên tham số để so path."""
    p = re.sub(r"^/api/v1/(?:admin|partner|public)(?=/)", "", p.split("?")[0].rstrip("/"))
    return re.sub(r"\{[^}]+\}", "{}", p)


def load_endpoints():
    """operationId -> (ID mục chứa endpoint, vị trí khai báo); (method, path) -> operationId;
    kèm danh sách lỗi."""
    ops, paths, errors = {}, {}, []
    for path in sorted((DOCS / "system-design").glob("0[1-9]-*.md")):
        rel = path.relative_to(DOCS).as_posix()
        did, in_table = None, False
        for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            where = f"{rel}:{n}"
            h = HEAD_RE.match(line)
            if h:
                tag = h.group(2)
                did = tag if tag and re.fullmatch(DID, tag) else None
            if not line.startswith("|"):
                in_table = False
            found = []  # (method, path, ô operationId)
            if EP_HEAD_RE.match(line) or (path.name.startswith("06") and EP_HEAD06_RE.match(line)):
                in_table = True
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                k = cells.index("Path") if "Path" in cells else cells.index("Endpoint")
                if k + 1 >= len(cells) or cells[k + 1] != "operationId":
                    errors.append(f"{where}: bảng endpoint thiếu cột operationId ngay sau cột {cells[k]}")
                continue
            if in_table:
                m = EP_ROW_RE.match(line) or EP_ROW06_RE.match(line)
                if m:
                    found.append((m.group(1), m.group(2), m.group(3).strip()))
            m = OP_BULLET_RE.match(line)
            if m and h is None:
                hm = re.search(rf"`({METHOD}) ([^`]+)`", _last_head.get(rel, ""))
                found.append((hm.group(1), hm.group(2), f"`{m.group(1)}`") if hm else ("", "", f"`{m.group(1)}`"))
            for m in OP_INLINE_RE.finditer(line):
                found.append((m.group(1), m.group(2), f"`{m.group(3)}`"))
            if h:
                _last_head[rel] = line
            for method, epath, cell in found:
                cm = re.fullmatch(r"`([^`]+)`", cell)
                if not cm:
                    errors.append(f"{where}: endpoint {method} {epath} thiếu operationId")
                    continue
                op = cm.group(1)
                if not OP_FMT_RE.fullmatch(op):
                    errors.append(f"{where}: operationId {op} sai định dạng <tiền tố>.<tênCamelCase>")
                elif epath and op.split(".")[0] != op_prefix(epath):
                    errors.append(f"{where}: operationId {op} sai tiền tố — path {epath} dùng tiền tố {op_prefix(epath)}")
                if op in ops:
                    errors.append(f"{where}: operationId {op} bị trùng (đã khai báo ở {ops[op][1]})")
                elif did is None:
                    errors.append(f"{where}: endpoint {op} nằm trong mục chưa có ID thiết kế")
                ops.setdefault(op, (did, where))
                if epath:
                    paths.setdefault((method, norm_path(epath)), op)
    return ops, paths, errors


def endpoint_of(method, path, paths):
    """operationId của endpoint được trích bằng method + path; path viết tắt ("…/x") chỉ tính
    khi khớp đúng một endpoint (khớp nhiều endpoint là mô tả mẫu chung, không phải trích dẫn)."""
    if path[0] == "/":
        return paths.get((method, norm_path(path)))
    suffix = norm_path("/" + path.lstrip(".…").lstrip("/"))
    found = [op for (m, p), op in paths.items() if m == method and p.endswith(suffix)]
    return found[0] if len(found) == 1 else None



def check_tracker(ids, dids):
    errors = []
    if not TRACKER.exists():
        return errors
    text = TRACKER.read_text(encoding="utf-8")
    actual = {}
    for rid in ids:
        mod, num = rid[2:].rsplit("-", 1)
        actual[mod] = max(actual.get(mod, 0), int(num))
    for m in TRACKER_R_RE.finditer(text):
        mod, num = m.group(1), int(m.group(3))
        if actual.get(mod, 0) > num:
            errors.append(f"Sổ theo dõi: ID lớn nhất đã cấp của {mod} ghi R-{mod}-{num:03d}, "
                          f"nhưng đặc tả đã có R-{mod}-{actual[mod]:03d}")
    dactual = {}
    for did in dids:
        code, num = did[2:].rsplit("-", 1)
        dactual[code] = max(dactual.get(code, 0), int(num))
    recorded = {m.group(1): int(m.group(3)) for m in TRACKER_D_RE.finditer(text)}
    for code, num in dactual.items():
        if recorded.get(code, 0) < num:
            shown = f"D-{code}-{recorded[code]:03d}" if code in recorded else "—"
            errors.append(f"Sổ theo dõi: ID thiết kế lớn nhất đã cấp của {code} ghi {shown}, "
                          f"nhưng tài liệu đã có D-{code}-{num:03d}")
    return errors


def tag_code(m):
    """Mã file từ một match FILE_TAG / NEAR_RE (nhóm số 0X hoặc tên luồng web)."""
    for g in m.groups():
        if g and re.fullmatch(r"0[1-9]", g):
            return f"SD{g}"
        if g in WEB_CODE:
            return WEB_CODE[g]
    return None


def check_file(path, ids, dids, secs, own_code, ops, paths):
    errors = []
    rel = path.relative_to(DOCS).as_posix()
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        where = f"{rel}:{n}"
        head = HEAD_RE.match(line)
        body = line[head.end():] if head else line  # bỏ phần định nghĩa ID ở tiêu đề
        off = len(line) - len(body)
        covered = set()  # vị trí các §/¶ đã đi kèm ID

        for m in R_CITE_RE.finditer(body):
            rid, sym, sec = m.groups()
            if sym:
                covered.add(off + body.index(sym, m.start()))
            if rid not in ids:
                errors.append(f"{where}: {rid} không còn trong đặc tả (đã bỏ hoặc gõ sai)")
            elif sym == "¶":
                errors.append(f"{where}: {rid} là mục đặc tả, dùng § thay cho ¶")
            elif sec is not None and sec != ids[rid]:
                errors.append(f"{where}: {rid} ghi §{sec}, số mục hiện tại là §{ids[rid]}")

        for m in D_CITE_RE.finditer(body):
            did, sym, sec = m.groups()
            if sym:
                covered.add(off + body.index(sym, m.start()))
            if did not in dids:
                errors.append(f"{where}: {did} không có trong tài liệu thiết kế (đã bỏ hoặc gõ sai)")
            elif sym == "§":
                errors.append(f"{where}: {did} là mục thiết kế, dùng ¶ thay cho §")
            elif sec is not None and sec != dids[did][1]:
                errors.append(f"{where}: {did} ghi ¶{sec}, số mục hiện tại là ¶{dids[did][1]}")

        for m in SYM_RE.finditer(line):
            if m.start() in covered:
                continue
            sym, sec = m.groups()
            if sym == "§":
                errors.append(f"{where}: trích dẫn {m.group(0)} không kèm ID")
                continue
            t = TAG_BEFORE_SYM_RE.search(line[:m.start()])
            code = tag_code(t) if t else own_code
            if code is None:
                errors.append(f"{where}: trích dẫn {m.group(0)} không rõ thuộc tài liệu thiết kế nào")
            elif code not in secs or sec not in secs[code]:
                errors.append(f"{where}: trích dẫn {m.group(0)} — tài liệu mã {code} không có mục {sec}")
            elif secs[code][sec]:
                errors.append(f"{where}: trích dẫn {m.group(0)} không kèm ID — mục này là {secs[code][sec]}")

        for m in OP_CITE_RE.finditer(body):
            op, _, did = m.groups()
            if op not in ops:
                errors.append(f"{where}: operationId {op} không có trong bảng endpoint nào (đã bỏ hoặc gõ sai)")
            if did:
                errors.append(f"{where}: {op} kèm ID mục {did} — chỉ ghi operationId (mục 2.5)")

        # Tiêu đề mục và dòng bảng endpoint là nơi khai báo endpoint, không phải trích dẫn
        if not (head or EP_ROW_RE.match(line) or EP_ROW06_RE.match(line)):
            for m in MP_RE.finditer(body):
                if MP_AFTER_OP_RE.search(body[:m.start()]) or body[m.end():].startswith(" (operationId `"):
                    continue
                op = endpoint_of(m.group(1), m.group(2), paths)
                if op:
                    errors.append(f"{where}: trích endpoint {m.group(0)} chỉ bằng method + path — "
                                  f"dùng `{op}`")

        for m in OLD_WEB_RE.finditer(line):
            errors.append(f"{where}: dạng cũ \"{m.group(0).strip()}\" — dùng ID kèm ¶ hoặc \"{m.group(1)} ¶…\"")

        for m in MUC_RE.finditer(line):
            window = line[max(0, m.start() - 80):m.start()]
            before = list(NEAR_RE.finditer(window))
            # Tên tài liệu phía trước chỉ tính khi không bị ngắt bởi ")", ";", "—" (thuộc câu khác)
            if before and re.search(r"[);—]", window[before[-1].end():]):
                before = []
            after = re.match(r"\s*(?:của|trong|ở)?\s*(?:tài liệu (0[1-9])\b|`(0[1-9])`)", line[m.end():])
            near = after or (before[-1] if before else None)
            if near is None:
                if own_code:  # "mục N" trong chính tài liệu thiết kế
                    errors.append(f"{where}: dạng cũ \"{m.group(0)}\" — trích mục trong cùng file bằng D-… (¶…) hoặc ¶…")
                continue
            code = tag_code(near)
            if code:
                errors.append(f"{where}: dạng cũ \"{m.group(0)}\" của tài liệu mã {code} — dùng D-… (¶…) hoặc <tên file> ¶…")
            elif near.re is NEAR_RE and near.group(5):
                errors.append(f"{where}: trích đặc tả \"{m.group(0)}\" — dùng R-… (§…)")
    return errors


def main():
    only = None
    if "--luong" in sys.argv:
        only = sys.argv[sys.argv.index("--luong") + 1]
        if only not in DESIGN_DIRS:
            print(f"--luong phải là một trong: {', '.join(DESIGN_DIRS)}")
            return 2
    files = design_files()
    code_of = {p: c for c, p in files.items()}
    ids, errors = load_spec()
    dids, secs, derr = load_design(files)
    ops, paths, oerr = load_endpoints()
    errors += check_tracker(ids, dids)
    scanned = 0
    for d in DESIGN_DIRS:
        for path in sorted((DOCS / d).glob("*.md")):
            if path.name in SKIP_FILES:
                continue
            scanned += 1
            errors += check_file(path, ids, dids, secs, code_of.get(path), ops, paths)
    errors += derr + oerr
    if only:
        errors = [e for e in errors if e.startswith(only + "/")]
    for e in errors:
        print(e)
    scope = f" (chỉ báo lỗi luồng {only})" if only else ""
    print(f"\nĐặc tả: {len(ids)} ID. Thiết kế: {len(dids)} ID, {len(ops)} operationId. "
          f"Đã quét {scanned} file ở {', '.join(DESIGN_DIRS)}{scope}. Lỗi: {len(errors)}.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
