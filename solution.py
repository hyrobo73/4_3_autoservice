"""보도자료 마크다운 파일을 담당 부서별로 분류하는 도구.

실행: python solution.py
입력: 보도자료/*.md
출력: 출력_부서별/<부서명>/, 결과_분류현황.csv
"""

from __future__ import annotations

import csv
import re
import shutil
from collections import Counter
from pathlib import Path

INPUT_DIR = Path("보도자료")
OUTPUT_DIR = Path("출력_부서별")
RESULT_CSV = Path("결과_분류현황.csv")
DEPARTMENT_PATTERN = re.compile(r"부서:\s*([^|>]+?)\s*\|\s*코드:")


def read_text(path: Path) -> str:
    """UTF-8 우선으로 읽고, 필요할 경우 한글 레거시 인코딩을 시도한다."""
    for encoding in ("utf-8-sig", "utf-8", "cp949", "euc-kr"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    raise UnicodeError(f"파일 인코딩을 읽을 수 없습니다: {path}")


def get_department(path: Path) -> str:
    match = DEPARTMENT_PATTERN.search(read_text(path))
    if not match:
        raise ValueError(f"부서 정보를 찾을 수 없습니다: {path.name}")
    return match.group(1).strip()


def main() -> None:
    if not INPUT_DIR.is_dir():
        raise FileNotFoundError(f"입력 폴더가 없습니다: {INPUT_DIR}")

    counts: Counter[str] = Counter()
    files = sorted(INPUT_DIR.glob("*.md"))

    for source in files:
        department = get_department(source)
        target_dir = OUTPUT_DIR / department
        target_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target_dir / source.name)
        counts[department] += 1

    ordered_counts = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    with RESULT_CSV.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["부서명", "건수"])
        writer.writerows(ordered_counts)

    print(f"총 {len(files)}건 분류 완료")
    for department, count in ordered_counts:
        print(f"{department}: {count}건")
    print(f"집계 파일 저장: {RESULT_CSV}")


if __name__ == "__main__":
    main()
