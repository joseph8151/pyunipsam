// 샘플 PDF 생성: 먼저 `python3 tools/build_site.py` 로 site/sample/*.html 을 만든 뒤 실행한다.
//   node tools/make_sample_pdfs.js   → site/samples/{eng,math,univ}-{problem,solution}.pdf
const { chromium } = require("playwright");
const path = require("path");
const { execFileSync } = require("child_process");
const fs = require("fs");
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
  await b.close();
  // 브라우저 쪽 나눔 때문에 생기는 맨 끝의 글자 없는 쪽을 제거한다(poppler 의 pdfinfo/pdftotext/pdfseparate/pdfunite 필요)
  for (const k of ["eng", "math", "univ"]) for (const name of ["problem", "solution"]) {
    const file = path.join(root, "samples", `${k}-${name}.pdf`);
    let n = parseInt(/Pages:\s+(\d+)/.exec(execFileSync("pdfinfo", [file]).toString())[1], 10);
    const keep = n;
    while (n > 1 && execFileSync("pdftotext", ["-f", String(n), "-l", String(n), file, "-"]).toString().trim() === "") n--;
    if (n < keep) {
      const tmp = fs.mkdtempSync(path.join(require("os").tmpdir(), "pdf-"));
      execFileSync("pdfseparate", ["-f", "1", "-l", String(n), file, path.join(tmp, "p-%d.pdf")]);
      const parts = Array.from({ length: n }, (_, i) => path.join(tmp, `p-${i + 1}.pdf`));
      execFileSync("pdfunite", [...parts, file + ".tmp"]); fs.renameSync(file + ".tmp", file);
    }
  }
  console.log("ok");
})();
