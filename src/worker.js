// 편입샘 Worker: 정적 사이트(ASSETS)는 그대로 서빙하고 /api/* 만 처리한다.
// 출시 알림·문의 저장소(KV)가 연결된 경우에만 접수가 활성화된다. 연결 방법은 tools/README.md 참고.
const JSON_HEADERS = { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" };
const TTL = 60 * 60 * 24 * 365; // 보관 12개월 후 자동 삭제(개인정보 처리방침과 동일)
const EMAIL = /^[^@\s]{1,64}@[^@\s]{1,255}\.[^@\s]{2,}$/;

const json = (body, status = 200) => new Response(JSON.stringify(body), { status, headers: JSON_HEADERS });

async function readBody(request) {
  const text = await request.text();
  if (text.length > 8000) throw new Error("too_large");
  return JSON.parse(text || "{}");
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (!url.pathname.startsWith("/api/")) return env.ASSETS.fetch(request);

    const store = env.SUBSCRIBERS; // KV 네임스페이스 바인딩 (없으면 접수 비활성)
    if (url.pathname === "/api/status") return json({ notify: !!store, contact: !!store });

    if (request.method !== "POST") return json({ message: "허용되지 않는 요청입니다." }, 405);
    if (!store) return json({ message: "접수 시스템이 연결되지 않았습니다." }, 501);
    if (!(request.headers.get("content-type") || "").includes("application/json")) return json({ message: "잘못된 요청입니다." }, 415);

    let d;
    try { d = await readBody(request); } catch { return json({ message: "요청을 읽을 수 없습니다." }, 400); }
    if (d.website) return json({ message: "접수되었습니다." }); // 허니팟: 봇은 성공한 것처럼 응답 후 저장하지 않음
    const email = String(d.email || "").trim().toLowerCase();
    if (!EMAIL.test(email)) return json({ message: "이메일 주소를 확인해 주세요." }, 400);
    if (d.consent !== true) return json({ message: "개인정보 수집·이용에 동의해 주세요." }, 400);
    const now = new Date().toISOString();

    if (url.pathname === "/api/notify") {
      const product = String(d.product || "").replace(/[^a-z0-9]/gi, "").slice(0, 16);
      if (!product) return json({ message: "상품 정보가 없습니다." }, 400);
      await store.put(`notify:${product}:${email}`, JSON.stringify({ email, product, consent: true, at: now }), { expirationTtl: TTL });
      return json({ message: "출시 알림 신청이 접수되었습니다. 해당 상품이 출시되면 안내해 드립니다." });
    }
    if (url.pathname === "/api/contact") {
      const message = String(d.message || "").trim().slice(0, 2000);
      if (!message) return json({ message: "문의 내용을 입력해 주세요." }, 400);
      const id = crypto.randomUUID();
      await store.put(`contact:${now}:${id}`, JSON.stringify({ email, name: String(d.name || "").slice(0, 80), message, consent: true, at: now }), { expirationTtl: TTL });
      return json({ message: "문의가 접수되었습니다. 입력하신 이메일로 답변드립니다." });
    }
    return json({ message: "찾을 수 없는 요청입니다." }, 404);
  },
};
