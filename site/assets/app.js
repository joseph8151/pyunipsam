/* 편입샘 V2.0 클라이언트 스크립트 — 필터·비교·장바구니(로컬)·알림/문의 폼 */
(function () {
  "use strict";
  var ROOT = document.body.getAttribute("data-root") || "";
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  /* ── 저장소 (브라우저 저장소 접근 실패 시에도 동작) ── */
  var mem = {};
  function load(k) { try { return JSON.parse(localStorage.getItem("pyunipsam." + k) || "[]"); } catch (e) { return mem[k] || []; } }
  function save(k, v) { mem[k] = v; try { localStorage.setItem("pyunipsam." + k, JSON.stringify(v)); } catch (e) { /* 무시 */ } }

  var toastEl = $("#toast"), toastT;
  function toast(msg) {
    if (!toastEl) return;
    toastEl.textContent = msg; toastEl.hidden = false;
    clearTimeout(toastT); toastT = setTimeout(function () { toastEl.hidden = true; }, 2600);
  }

  function refreshCounts() {
    ["compare", "cart"].forEach(function (k) {
      var n = load(k).length;
      $$('[data-count="' + k + '"]').forEach(function (el) { el.textContent = n; el.hidden = n === 0; });
    });
    var cmp = load("compare");
    $$("[data-compare]").forEach(function (b) {
      var on = cmp.indexOf(b.getAttribute("data-compare")) > -1;
      b.setAttribute("aria-pressed", on ? "true" : "false");
      if (b.classList.contains("btn") || b.textContent.indexOf("비교") > -1) b.textContent = on ? (b.classList.contains("btn") && b.closest(".sticky") ? "비교 중" : "비교 담김") : (b.closest(".sticky") ? "비교" : "비교 담기");
    });
  }

  document.addEventListener("click", function (e) {
    var c = e.target.closest("[data-compare]");
    if (c) {
      var id = c.getAttribute("data-compare"), list = load("compare"), i = list.indexOf(id);
      if (i > -1) { list.splice(i, 1); toast("비교 목록에서 뺐습니다."); }
      else if (list.length >= 3) { toast("비교는 최대 3개까지 담을 수 있습니다."); return; }
      else { list.push(id); toast("비교 목록에 담았습니다. 상단의 비교 아이콘에서 확인하세요."); }
      save("compare", list); refreshCounts(); return;
    }
    var k = e.target.closest("[data-cart]");
    if (k) {
      var cid = k.getAttribute("data-cart"), cl = load("cart");
      if (cl.indexOf(cid) < 0) cl.push(cid);
      save("cart", cl); refreshCounts(); toast("장바구니에 담았습니다.");
    }
  });

  /* ── 헤더·드로어 ── */
  var drawer = $("#drawer"), mt = $("#menuToggle"), st = $("#searchToggle"), sf = $(".search");
  function closeDrawer() { if (drawer) { drawer.hidden = true; mt.setAttribute("aria-expanded", "false"); document.body.style.overflow = ""; } }
  if (mt && drawer) {
    mt.addEventListener("click", function () { drawer.hidden = false; mt.setAttribute("aria-expanded", "true"); document.body.style.overflow = "hidden"; });
    drawer.addEventListener("click", function (e) { if (e.target === drawer || e.target.closest("a")) closeDrawer(); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") closeDrawer(); });
  }
  if (st && sf) st.addEventListener("click", function () {
    var open = sf.classList.toggle("open"); st.setAttribute("aria-expanded", open ? "true" : "false");
    if (open) $("input", sf).focus();
  });

  /* ── 전체 상품 필터 ── */
  var plist = $("#plist");
  if (plist) {
    var cards = $$(".pc", plist), params = new URLSearchParams(location.search);
    var pq = $("#pq"), pu = $("#pu"), sortSel = $("#psort"), cnt = $("#rcount"), empty = $("#pempty");
    var diffOrder = { "입문": 0, "기본": 1, "중급": 2, "고난도": 3, "실전": 4 };
    cards.forEach(function (c, i) { c._i = i; });
    function checked(name) { return $$('input[name="' + name + '"]:checked').map(function (x) { return x.value; }); }
    function apply() {
      var q = (pq.value || "").trim().toLowerCase(), cat = checked("cat"), diff = checked("diff"), stt = checked("status"), u = pu.value, n = 0;
      cards.forEach(function (c) {
        var ok = (!q || c.dataset.hay.indexOf(q) > -1) && (!cat.length || cat.indexOf(c.dataset.cat) > -1) &&
          (!diff.length || diff.indexOf(c.dataset.diff) > -1) && (!stt.length || stt.indexOf(c.dataset.status) > -1) && (!u || c.dataset.univ === u);
        c.hidden = !ok; if (ok) n++;
      });
      cnt.textContent = n + "종"; empty.hidden = n > 0;
      var s = sortSel.value, vis = cards.slice();
      vis.sort(function (a, b) {
        if (s === "diff") return diffOrder[a.dataset.diff] - diffOrder[b.dataset.diff] || a._i - b._i;
        if (s === "pages") return (+(a.dataset.pages || 9999)) - (+(b.dataset.pages || 9999)) || a._i - b._i;
        return a._i - b._i;
      }).forEach(function (c) { plist.appendChild(c); });
    }
    if (params.get("q")) pq.value = params.get("q");
    if (params.get("cat")) $$('input[name="cat"]').forEach(function (x) { x.checked = x.value === params.get("cat"); });
    if (params.get("univ")) pu.value = params.get("univ");
    ["input", "change"].forEach(function (ev) { $("#fBody").addEventListener(ev, apply); });
    sortSel.addEventListener("change", apply);
    $("#fReset").addEventListener("click", function () { setTimeout(apply, 0); });
    var ft = $("#fToggle");
    if (ft) ft.addEventListener("click", function () { var o = $("#fBody").classList.toggle("open"); ft.setAttribute("aria-expanded", o ? "true" : "false"); });
    apply();
  }

  /* ── 대학 목록 필터 ── */
  var ulist = $("#ulist");
  if (ulist) {
    var us = $$(".uc", ulist), inp = $("#uq2"), ucount = $("#ucount"), uempty = $("#uempty");
    function uchecked(name) { return $$('.ufil input[name="' + name + '"]:checked').map(function (x) { return x.value; }); }
    function uapply() {
      var q = (inp.value || "").trim().toLowerCase(), t = uchecked("track"), s = uchecked("subj"), l = uchecked("level"), n = 0;
      us.forEach(function (c) {
        var ok = (!q || c.dataset.hay.indexOf(q) > -1) && (!t.length || t.some(function (x) { return c.dataset.track.indexOf(x) > -1; })) &&
          (!s.length || s.some(function (x) { return c.dataset.subj.indexOf(x) > -1; })) && (!l.length || l.indexOf(c.dataset.level) > -1);
        c.hidden = !ok; if (ok) n++;
      });
      ucount.textContent = n + "개 대학"; uempty.hidden = n > 0;
    }
    var uq = new URLSearchParams(location.search).get("q"); if (uq) inp.value = uq;
    inp.addEventListener("input", uapply); $$(".ufil input").forEach(function (x) { x.addEventListener("change", uapply); });
    uapply();
  }
  var itb = $("#itb"), iq = $("#iq");
  if (itb && iq) iq.addEventListener("input", function () {
    var q = iq.value.trim().toLowerCase();
    $$("tbody tr", itb).forEach(function (r) { r.hidden = !!q && r.dataset.hay.indexOf(q) < 0; });
  });

  /* ── 비교·장바구니 화면 ── */
  var cmpbox = $("#cmpbox"), cartbox = $("#cartbox");
  if (cmpbox || cartbox) {
    fetch(ROOT + "assets/products.json").then(function (r) { return r.json(); }).then(function (all) {
      var by = {}; all.forEach(function (p) { by[p.id] = p; });
      function priceOf(p) { return p.status === "on_sale" && p.price ? (p.sale || p.price).toLocaleString() + "원" : "출시 시 공지"; }
      if (cmpbox) {
        var ids = load("compare").filter(function (i) { return by[i]; });
        $("#cmpempty").hidden = ids.length > 0;
        if (ids.length) {
          var rows = [["분류", function (p) { return p.cat + " · " + p.sub; }], ["난도", function (p) { return p.diff; }], ["구성", function (p) { return p.q + " (설계안)"; }],
            ["쪽수", function (p) { return p.pages ? "약 " + p.pages + "쪽 (설계안)" : "—"; }], ["상태", function (p) { return p.statusLabel; }], ["가격", priceOf],
            ["추천 대상", function (p) { return p.who; }], ["포함 자료", function (p) { return p.inc; }]];
          var h = '<table class="tb"><thead><tr><th></th>' + ids.map(function (i) { return '<th><a href="' + ROOT + by[i].url + '">' + by[i].title + '</a><br><button class="lk" data-compare="' + i + '" data-rm="1">빼기</button></th>'; }).join("") + "</tr></thead><tbody>";
          rows.forEach(function (r) { h += "<tr><th scope='row'>" + r[0] + "</th>" + ids.map(function (i) { return "<td>" + r[1](by[i]) + "</td>"; }).join("") + "</tr>"; });
          cmpbox.innerHTML = h + "</tbody></table>";
          cmpbox.addEventListener("click", function (e) { if (e.target.getAttribute("data-rm")) setTimeout(function () { location.reload(); }, 50); });
        }
      }
      if (cartbox) {
        var cl = load("cart").filter(function (i) { return by[i] && by[i].status === "on_sale"; });
        save("cart", cl); refreshCounts();
        $("#cartempty").hidden = cl.length > 0;
        if (cl.length) cartbox.innerHTML = '<table class="tb"><tbody>' + cl.map(function (i) { return '<tr><td><a href="' + ROOT + by[i].url + '">' + by[i].title + "</a></td><td>" + priceOf(by[i]) + "</td></tr>"; }).join("") + "</tbody></table>";
      }
    }).catch(function () { if (cmpbox) cmpbox.textContent = "상품 정보를 불러오지 못했습니다."; });
  }

  /* ── 알림 신청·문의 폼: 백엔드가 연결된 경우에만 활성화 ── */
  var forms = $$("form[data-form]");
  if (forms.length) {
    fetch("/api/status", { headers: { accept: "application/json" } }).then(function (r) { return r.ok ? r.json() : {}; }).catch(function () { return {}; }).then(function (s) {
      forms.forEach(function (f) {
        var kind = f.getAttribute("data-form"), on = !!(s && s[kind]), btn = $("button[type=submit]", f), sm = $("[data-statusmsg]", f), msg = $(".msg", f);
        btn.disabled = !on;
        sm.textContent = on ? (kind === "notify" ? "이메일을 남기면 출시 시 한 번 안내해 드립니다." : "문의 내용을 남겨 주세요.")
          : (kind === "notify" ? "현재 알림 신청 접수 시스템이 연결되지 않아 신청을 받을 수 없습니다. 고객 문의 페이지의 이메일로 요청해 주세요." : "현재 문의 접수 시스템이 연결되지 않았습니다. 아래 이메일로 직접 보내 주세요.");
        f.addEventListener("submit", function (e) {
          e.preventDefault(); if (!on) return;
          var d = {}; new FormData(f).forEach(function (v, k) { d[k] = v; });
          d.consent = !!$("[name=consent]", f).checked; d.product = f.getAttribute("data-product") || "";
          if (!d.email || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(d.email)) { msg.className = "msg err"; msg.textContent = "이메일 주소를 확인해 주세요."; return; }
          if (!d.consent) { msg.className = "msg err"; msg.textContent = "개인정보 수집·이용에 동의해 주세요."; return; }
          btn.disabled = true; msg.className = "msg"; msg.textContent = "접수 중…";
          fetch("/api/" + kind, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify(d) })
            .then(function (r) { return r.json().then(function (j) { return { ok: r.ok, j: j }; }); })
            .then(function (x) { msg.className = "msg " + (x.ok ? "ok" : "err"); msg.textContent = x.j.message || (x.ok ? "접수되었습니다." : "접수하지 못했습니다."); if (x.ok) f.reset(); btn.disabled = !x.ok ? false : false; })
            .catch(function () { msg.className = "msg err"; msg.textContent = "네트워크 오류로 접수하지 못했습니다."; btn.disabled = false; });
        });
      });
    });
  }

  refreshCounts();
})();
