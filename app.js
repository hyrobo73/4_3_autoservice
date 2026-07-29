// Google Sheets의 '웹에 게시'에서 복사한 embed URL을 입력하세요.
const GOOGLE_SHEETS_EMBED_URL = "";

const cards = document.querySelector("#cards");
const search = document.querySelector("#search");
const resultCount = document.querySelector("#result-count");
const empty = document.querySelector("#empty");

function escapeHtml(value) {
  return value.replace(/[&<>'\"]/g, (character) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#039;", '"': "&quot;"
  })[character]);
}

function draw(items) {
  resultCount.textContent = `결과 ${items.length}건`;
  empty.hidden = items.length !== 0;
  cards.innerHTML = items.map((item) => `
    <article class="card">
      <p class="department">${escapeHtml(item.department)}</p>
      <h3>${escapeHtml(item.title)}</h3>
      <div class="card-bottom">
        <span>보도자료 ${escapeHtml(item.code)}</span>
        <a href="${encodeURI(item.file)}" target="_blank" rel="noopener">원문 보기 <span aria-hidden="true">↗</span></a>
      </div>
    </article>`).join("");
}

async function init() {
  try {
    const response = await fetch("data/press-releases.json");
    if (!response.ok) throw new Error("자료를 불러오지 못했습니다.");
    const releases = await response.json();
    draw(releases);
    search.addEventListener("input", (event) => {
      const keyword = event.target.value.trim().toLowerCase();
      draw(releases.filter(({ title, department }) =>
        `${title} ${department}`.toLowerCase().includes(keyword)
      ));
    });
  } catch (error) {
    resultCount.textContent = "자료를 불러오지 못했습니다.";
  }
}

if (GOOGLE_SHEETS_EMBED_URL) {
  const frame = document.querySelector("#sheet-frame");
  frame.src = GOOGLE_SHEETS_EMBED_URL;
  frame.hidden = false;
  document.querySelector("#sheet-placeholder").hidden = true;
}

init();
