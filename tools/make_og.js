// 링크 공유용 대표 이미지(1200x630): node tools/make_og.js → site/assets/og.png  (site/assets/covers.svg 가 먼저 있어야 함)
const { chromium } = require("playwright");
const fs = require("fs"), path = require("path");
const root = path.join(__dirname, "..", "site", "assets");
const sprite = fs.readFileSync(path.join(root, "covers.svg"), "utf8").replace(/<svg[^>]*>/, '<svg xmlns="http://www.w3.org/2000/svg" width="0" height="0" style="position:absolute">');
const cv = (id, left, top, rot, z) => `<svg viewBox="0 0 300 400" style="position:absolute;left:${left}px;top:${top}px;width:230px;transform:rotate(${rot}deg);z-index:${z};box-shadow:0 30px 44px -18px rgba(0,0,0,.8),0 0 0 1px rgba(244,241,235,.12)"><use href="#c-${id}"/></svg>`;
const html = `<!doctype html><meta charset="utf-8"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+KR:wght@400;500;600&family=Nanum+Myeongjo:wght@700;800&family=IBM+Plex+Mono:wght@500&display=swap">
<style>*{box-sizing:border-box}body{margin:0;width:1200px;height:630px;position:relative;overflow:hidden;background:radial-gradient(ellipse 55% 80% at 78% 50%,rgba(186,165,140,.28),transparent 70%),linear-gradient(180deg,#3A3836,#242321);font-family:"IBM Plex Sans KR",sans-serif;color:#F4F1EB}
.grid{position:absolute;inset:0;background-image:linear-gradient(rgba(244,241,235,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(244,241,235,.05) 1px,transparent 1px);background-size:56px 56px}
.bar{position:absolute;left:0;right:0;bottom:0;height:10px;background:#BAA58C}
.t{position:absolute;left:72px;top:150px;width:600px}.eb{font-family:"IBM Plex Mono",monospace;font-size:20px;letter-spacing:.2em;color:#BAA58C;margin-bottom:24px}
h1{font-family:"Nanum Myeongjo",serif;font-weight:800;font-size:150px;line-height:1;margin:0;letter-spacing:-.04em;color:#fff}
p{font-size:34px;margin:28px 0 0;color:#D2CCC2;line-height:1.5}.r{height:3px;width:96px;background:#BAA58C;margin:30px 0 0}</style>
${sprite}<div class="grid"></div><div class="t"><div class="eb">TRANSFER EXAM WORKBOOKS</div><h1>편입샘</h1><div class="r"></div><p>대학 편입시험 전문 PDF 문제집<br>필요한 문제만, 정확하게.</p></div>
${cv("p13", 690, 120, -6, 1)}${cv("p27", 800, 70, -1, 2)}${cv("u01", 910, 150, 5, 3)}<div class="bar"></div>`;
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1200, height: 630 } });
  await p.setContent(html, { waitUntil: "networkidle" }); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(600);
  await p.screenshot({ path: path.join(root, "og.png") }); await b.close(); console.log("ok");
})();
