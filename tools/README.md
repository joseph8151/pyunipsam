# 편입샘 사이트 관리 안내

사이트는 `tools/build_site.py` 가 `site/` 폴더를 생성하고, Cloudflare Workers(`wrangler.jsonc`)가 `site/`를 서빙합니다.
`main` 브랜치에 푸시하면 Cloudflare 가 `npx wrangler deploy` 로 자동 배포합니다. **`site/`는 생성물이므로 직접 고치지 말고 아래 원본을 수정한 뒤 다시 빌드하세요.**

```bash
python3 tools/build_site.py      # site/ 재생성 (데이터 검증 포함)
npx wrangler dev --local         # 로컬 확인 (http://localhost:8787)
```

## 원본 파일
| 무엇을 바꾸나 | 파일 |
|---|---|
| 상품 정보(이름·설명·문항 수·쪽수·상태 기본값) | `tools/catalog_products.py` |
| 대학별 편입정보·확인 수준·공식 링크 | `tools/catalog_univ.py` |
| 표지 시안 디자인 | `tools/covers.py` |
| 페이지 구성 | `tools/build_site.py` |
| 스타일·스크립트 | `tools/assets/style.css`, `tools/assets/app.js` |
| **가격·할인** | `data/prices.json` |
| **상품 상태 변경** | `data/status_overrides.json` |
| 샘플 PDF 등록 | `data/samples.json` (파일은 `site/samples/` 에 둠) |

## 상품 상태
`draft`(기획 중) / `coming_soon`(출시 예정) / `sample_ready`(샘플 공개) / `on_sale`(판매 중) / `discontinued`(판매 종료)

- 구매·장바구니 버튼은 **`on_sale` 이면서 `price` 가 설정된 상품에만** 나타납니다. 그 외에는 가격을 표시하지 않습니다.
- `on_sale` 인데 `price` 가 없거나 `salePrice` 가 `price` 이상이면 빌드가 실패합니다(가짜 할인 방지).
- `sample_ready` 인데 샘플 파일이 없으면 빌드가 실패합니다.

### 가격 설정 예
```json
// data/prices.json
{ "p27": { "price": 59000, "salePrice": 49000 } }
// data/status_overrides.json
{ "p27": "on_sale" }
```
검토용 가격대(사업적 가설이며 검증된 시장 가격이 아님): 소형 29~39천 / 전문 단일 39~69천 / 종합 79~99천 / 대학별 모의 49~69천 / 패키지 129~179천 원.

## 출시 알림·문의 접수 활성화 (선택)
접수 API(`/api/notify`, `/api/contact`)는 코드가 준비되어 있으나, **저장소(KV)가 연결되기 전에는 폼이 자동으로 비활성**입니다.

1. `npx wrangler kv namespace create SUBSCRIBERS` 로 KV 를 만들고 출력된 `id` 를 확인합니다.
2. `wrangler.jsonc` 에 추가합니다.
   ```jsonc
   "kv_namespaces": [{ "binding": "SUBSCRIBERS", "id": "<위에서 받은 id>" }]
   ```
3. 커밋·푸시하면 배포 후 폼이 활성화됩니다. 데이터는 12개월 후 자동 삭제됩니다(`개인정보 처리방침`과 동일).

수집한 이메일 확인: `npx wrangler kv key list --binding SUBSCRIBERS --remote`

## 결제
결제는 아직 연결되어 있지 않습니다. 장바구니는 브라우저 저장소만 사용하며 결제 버튼은 비활성입니다. 결제 연동 시 환불·청약철회 규정, 사업자 정보, 개인정보 처리방침을 확정해 `이용 안내`·푸터·`privacy.html` 에 반영해야 합니다.

## 대학별 정보 갱신
시험 정보는 매년 바뀝니다. 2027학년도 모집요강이 공개되면 `catalog_univ.py` 의 각 대학 항목(`exam`, `level`, `links`)과 `CHECKED` 날짜를 갱신하세요.
확인 수준: `official`(공식 문서) / `partial`(공식 공지 일부) / `secondary`(2차 자료) / `none`(미확인).

## 샘플 문제집·해설집
- 샘플은 편입샘이 새로 쓴 **독창 문항**이며 전문가 검수 전 시안입니다(`tools/sample_content.py`). 수학·대학별 샘플의 정답은 수치 계산으로 검증했습니다.
- 과목마다 문제집·해설집 PDF가 한 세트입니다: `site/samples/{eng,math,univ}-{problem,solution}.pdf`, 오답노트 `ohdap-note.pdf`.
- 샘플 내용을 고치면 다음 순서로 다시 만드세요.
  ```bash
  python3 tools/build_site.py          # 샘플 화면(site/sample/*.html) 생성
  node tools/make_sample_pdfs.js       # 화면에서 PDF 생성 (문제집/해설집)
  node tools/make_note_pdf.js          # 오답노트 양식 PDF
  python3 tools/build_site.py          # PDF 존재 여부를 반영해 다시 빌드
  ```
- `data/samples.json` 의 `products`(상품 상세 연결)와 `free`(무료 샘플 버튼)에 등록된 파일이 실제로 있을 때만 다운로드 버튼이 활성화됩니다.

## 디자인 시스템
차콜 `#33312F` / 다크 차콜 `#242321` / 웜 아이보리 `#F4F1EB` / 샌드 베이지 `#BAA58C`(강조에만) / 보조 텍스트 `#77726D` / 테두리 `#DED9D0`. 블루 계열은 사용하지 않습니다. 변수는 `tools/assets/style.css` 상단 `:root` 에 있고, 표지 색은 `tools/covers.py` 에 있습니다.
