# 재난·안전 보도자료 아카이브

## 자료 갱신

1. `보도자료` 폴더에 마크다운 파일을 추가합니다. 파일에는 `<!-- 부서: 부서명 | 코드: 번호 -->` 메타정보가 필요합니다.
2. `python scripts/organize_press.py`를 실행합니다.
3. 생성된 `site/data/department-summary.csv`를 Google Sheets로 가져와 집계표 또는 피벗 테이블을 만듭니다.
4. Google Sheets에서 **파일 → 공유 → 웹에 게시**를 선택하고 iframe 주소를 복사합니다.
5. `site/app.js`의 `GOOGLE_SHEETS_EMBED_URL` 값에 주소를 넣으면 웹페이지에 표시됩니다.

`site` 폴더는 정적 호스팅(GitHub Pages, Netlify, Cloudflare Pages 등)에 그대로 배포할 수 있습니다. 웹서버 없이 HTML 파일을 직접 열면 브라우저 보안상 JSON을 읽지 못할 수 있으므로, 배포 또는 간단한 로컬 서버에서 확인하세요.
