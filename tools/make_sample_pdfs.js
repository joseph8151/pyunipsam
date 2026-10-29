// 샘플 PDF 생성: 먼저 `python3 tools/build_site.py` 로 site/sample/*.html 을 만든 뒤 실행한다.
//   node tools/make_sample_pdfs.js   → site/samples/{eng,math,univ}-{problem,solution}.pdf
const { chromium } = require("playwright");
const path = require("path");
const root = path.join(__dirname, "..", "site");
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.emulateMedia({ media: "print" });
  for (const k of ["eng", "math", "univ"]) {
    await p.goto("file://" + path.join(root, "sample", k + ".html"), { waitUntil: "load" });
    await p.waitForTimeout(500);
    for (const [cls, name] of [["hide-sol", "problem"], ["hide-prob", "solution"]]) {
      await p.evaluate((c) => { document.body.classList.remove("hide-sol", "hide-prob"); document.body.classList.add(c); }, cls);
      await p.pdf({ path: path.join(root, "samples", `${k}-${name}.pdf`), format: "A4", printBackground: true, margin: { top: "12mm", bottom: "12mm", left: "12mm", right: "12mm" } });
    }
  }
  await b.close(); console.log("ok");
})();
