"""보도자료를 부서별로 정리하고 웹페이지용 데이터를 생성합니다.

실행: python scripts/organize_press.py
원본 `보도자료` 폴더는 변경하지 않습니다.
"""

from __future__ import annotations

import csv
import json
import re
import shutil
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "보도자료"
SORTED = ROOT / "정리본"
DATA = ROOT / "site" / "data"

META_PATTERN = re.compile(r"부서:\s*([^|>]+?)\s*\|\s*코드:\s*([^|>]+?)\s*(?:\||-->)")
PDF_TITLE_PATTERN = re.compile(r"원본PDF:\s*[^|>]*?\)\s*(.*?)\(([^()]+)\)\s*(?:\.pdf)?\s*-->")


def read_markdown(path: Path) -> str:
    """UTF-8 우선, 과거 한글 인코딩도 보조적으로 처리합니다."""
    for encoding in ("utf-8-sig", "utf-8", "cp949", "euc-kr"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    raise UnicodeError(f"읽을 수 없는 인코딩입니다: {path}")


def clean_title(value: str) -> str:
    return re.sub(r"\s+", " ", value.replace("**", "").replace("\\", "").strip(" -–—"))


def extract_title(text: str, path: Path) -> str:
    """원본 PDF 제목을 우선 사용하고, 없으면 첫 굵은 문장을 제목으로 씁니다."""
    pdf_title = PDF_TITLE_PATTERN.search(text)
    if pdf_title:
        return clean_title(pdf_title.group(1))

    for line in text.splitlines():
        candidate = clean_title(line)
        if candidate and len(candidate) >= 12 and not candidate.startswith(("<!--", "|", ">>")):
            return candidate
    return path.stem.replace("_", " ")


def main() -> None:
    if not SOURCE.exists():
        raise FileNotFoundError(f"원본 폴더가 없습니다: {SOURCE}")

    SORTED.mkdir(exist_ok=True)
    DATA.mkdir(parents=True, exist_ok=True)
    records = []

    for path in sorted(SOURCE.glob("*.md")):
        text = read_markdown(path)
        meta = META_PATTERN.search(text)
        if not meta:
            print(f"[건너뜀] 메타정보 없음: {path.name}")
            continue

        department, code = (value.strip() for value in meta.groups())
        destination = SORTED / department
        destination.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, destination / path.name)

        records.append({
            "code": code,
            "title": extract_title(text, path),
            "department": department,
            "file": f"../보도자료/{path.name}",
        })

    records.sort(key=lambda item: item["code"], reverse=True)
    (DATA / "press-releases.json").write_text(
        json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    with (DATA / "department-summary.csv").open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.writer(handle)
        writer.writerow(["부서", "보도자료 건수"])
        writer.writerows(sorted(Counter(item["department"] for item in records).items()))

    print(f"완료: {len(records)}건 분류 / {len(set(x['department'] for x in records))}개 부서")


if __name__ == "__main__":
    main()
