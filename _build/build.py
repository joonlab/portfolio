#!/usr/bin/env python3
"""projects.json → projects/index.html + projects/<slug>/index.html 정적 생성.

사용: python3 _build/build.py   (레포 루트 기준 경로를 스스로 계산한다)
"""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "_build" / "projects.json").read_text(encoding="utf-8"))
OUT = ROOT / "projects"
MEDIA = ROOT / "media"

E = lambda s: html.escape(str(s), quote=True)

CATEGORY_ORDER = [
    "AI 에이전트·자동화", "음성·오디오", "모바일·디바이스", "웹앱·대시보드",
    "데이터·크롤링·API", "교육·콘텐츠 제작", "영상·모션", "컨설팅·업무설계", "연구·평가", "기타",
]

CSS = """
@font-face{font-family:'Pretendard';src:url('/assets/fonts/PretendardVariable.subset.woff2') format('woff2');font-weight:100 900;font-display:swap}
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
:root{--accent:#A50034;--accent-soft:#f7e6ec;--gold:#85714D;--text:#1A1A1A;--sub:#555;--muted:#6B6B6B;--line:#e4e4e4;--bg:#fff;--alt:#fafafa;--ink:#141414}
html{scroll-behavior:smooth}
body{font-family:'Pretendard',-apple-system,BlinkMacSystemFont,'Apple SD Gothic Neo','Malgun Gothic',sans-serif;color:var(--text);background:var(--bg);line-height:1.7;font-size:15px;word-break:keep-all;-webkit-font-smoothing:antialiased}
a{color:inherit}
.wrap{max-width:1040px;margin:0 auto;padding:0 24px}
.topbar{border-bottom:1px solid var(--line);background:#fff;position:sticky;top:0;z-index:50}
.topbar .wrap{display:flex;align-items:center;justify-content:space-between;height:56px;gap:16px}
.brand{font-weight:800;letter-spacing:-.2px;text-decoration:none;font-size:.98rem}
.brand span{color:var(--accent)}
.toplinks{display:flex;gap:18px;font-size:.88rem}
.toplinks a{text-decoration:none;color:var(--sub)}
.toplinks a:hover,.toplinks a[aria-current]{color:var(--accent)}
.eyebrow{font-size:.78rem;font-weight:700;letter-spacing:.14em;color:var(--accent);text-transform:uppercase}
.hero{padding:64px 0 36px}
.hero h1{font-size:2.5rem;line-height:1.25;letter-spacing:-.8px;margin:12px 0 16px;font-weight:800}
.hero p.lead{font-size:1.08rem;color:var(--sub);max-width:720px}
.stats{display:flex;flex-wrap:wrap;gap:36px;margin-top:32px}
.stat b{display:block;font-size:2rem;font-weight:800;letter-spacing:-.5px;line-height:1.1}
.stat b small{font-size:1rem;color:var(--accent);margin-left:2px}
.stat span{font-size:.85rem;color:var(--muted)}
.filters{display:flex;flex-wrap:wrap;gap:8px;padding:18px 0 22px;border-top:1px solid var(--line);margin-top:28px}
.chip{border:1px solid var(--line);background:#fff;border-radius:999px;padding:6px 14px;font:inherit;font-size:.85rem;color:var(--sub);cursor:pointer}
.chip:hover{border-color:var(--accent);color:var(--accent)}
.chip[aria-pressed=true]{background:var(--ink);border-color:var(--ink);color:#fff}
.chip em{font-style:normal;color:var(--muted);margin-left:4px;font-size:.78rem}
.chip[aria-pressed=true] em{color:#cfcfcf}
.case[hidden]{display:none}
.cases{display:grid;gap:20px;padding-bottom:56px}
.case{display:grid;grid-template-columns:1fr;border:1px solid var(--line);border-radius:14px;overflow:hidden;text-decoration:none;background:#fff;transition:border-color .2s,box-shadow .2s}
.case:hover{border-color:#cfcfcf;box-shadow:0 8px 28px rgba(0,0,0,.07)}
.case:focus-visible{outline:2px solid var(--accent);outline-offset:3px}
.case-body{padding:26px 28px 24px}
.case-top{display:flex;flex-wrap:wrap;align-items:center;gap:6px 8px;margin-bottom:14px}
.tag{font-size:.75rem;padding:3px 10px;border-radius:6px;background:#f3f3f3;color:#333;font-weight:600}
.tag.cat{background:var(--accent-soft);color:var(--accent)}
.meta-inline{font-size:.8rem;color:var(--muted);margin-left:auto}
.case h2{font-size:1.35rem;letter-spacing:-.3px;line-height:1.35;margin-bottom:6px}
.case .one{color:var(--sub);font-size:.95rem}
.ps{display:grid;grid-template-columns:1fr;gap:14px;margin-top:18px}
.ps h3{font-size:.72rem;letter-spacing:.14em;color:var(--muted);font-weight:700;margin-bottom:4px}
.ps p{font-size:.9rem;color:#333;line-height:1.65}
.metrics{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:1px;background:var(--line);border-top:1px solid var(--line)}
.metric{background:var(--alt);padding:16px 20px}
.metric b{font-size:1.6rem;font-weight:800;letter-spacing:-.5px;line-height:1.15;display:block}
.metric b small{font-size:.85rem;font-weight:700;color:var(--accent);margin-left:2px}
.metric span{font-size:.8rem;color:var(--muted);line-height:1.4;display:block;margin-top:2px;overflow-wrap:anywhere}
.metric b{overflow-wrap:anywhere}
.more{display:inline-block;margin-top:16px;font-size:.85rem;font-weight:700;color:var(--accent)}
.section-h{font-size:1.25rem;font-weight:800;margin:8px 0 18px;letter-spacing:-.3px}
.minor{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:12px;padding-bottom:72px}
.minor div{border:1px solid var(--line);border-radius:10px;padding:14px 16px}
.minor b{display:block;font-size:.95rem}
.minor span{font-size:.84rem;color:var(--sub);display:block;margin-top:2px;overflow-wrap:anywhere}
.minor i{font-style:normal;font-size:.72rem;color:var(--gold);font-weight:700}
footer{border-top:1px solid var(--line);padding:32px 0 48px;color:var(--muted);font-size:.85rem}
footer .wrap{display:flex;flex-wrap:wrap;justify-content:space-between;gap:12px}
/* detail */
.crumb{font-size:.85rem;color:var(--muted);padding-top:28px}
.crumb a{text-decoration:none;color:var(--sub)}
.crumb a:hover{color:var(--accent)}
.d-hero{padding:22px 0 30px}
.d-hero h1{font-size:2.3rem;line-height:1.25;letter-spacing:-.7px;margin:14px 0 12px;font-weight:800}
.d-hero .lead{font-size:1.08rem;color:var(--sub);max-width:760px}
.facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:0;border:1px solid var(--line);border-radius:12px;margin-top:26px;overflow:hidden}
.facts div{padding:14px 18px;border-right:1px solid var(--line)}
.facts div:last-child{border-right:0}
.facts dt{font-size:.72rem;letter-spacing:.12em;color:var(--muted);font-weight:700}
.facts dd{font-size:.95rem;font-weight:600;margin-top:2px}
.d-metrics{border:1px solid var(--line);border-radius:12px;overflow:hidden;margin:8px 0 8px}
.d-metrics .metrics{border-top:0}
.d-sec{padding:34px 0;border-top:1px solid var(--line)}
.d-sec:first-of-type{border-top:0}
.d-grid{display:grid;grid-template-columns:1fr;gap:10px 40px}
.d-grid h2{font-size:.78rem;letter-spacing:.14em;color:var(--accent);font-weight:800;text-transform:uppercase;padding-top:4px}
.d-grid .body p{margin-bottom:10px;color:#2a2a2a}
.d-grid .body ul{padding-left:18px;color:#2a2a2a}
.d-grid .body li{margin-bottom:6px}
.flow{display:flex;flex-direction:column;gap:0;counter-reset:s}
.step{position:relative;border:1px solid var(--line);border-radius:10px;padding:12px 16px 12px 52px;background:#fff}
.step::before{counter-increment:s;content:counter(s);position:absolute;left:14px;top:12px;width:24px;height:24px;border-radius:50%;background:var(--ink);color:#fff;font-size:.78rem;font-weight:700;display:grid;place-items:center}
.step b{display:block;font-size:.95rem}
.step span{font-size:.86rem;color:var(--sub)}
.arrow{width:2px;height:16px;background:#cfcfcf;margin-left:26px}
.feats{display:grid;grid-template-columns:1fr;gap:12px}
.feat{border:1px solid var(--line);border-radius:10px;padding:14px 16px}
.feat b{display:block;font-size:.95rem;margin-bottom:2px}
.feat span{font-size:.88rem;color:var(--sub)}
.stack{display:flex;flex-wrap:wrap;gap:8px}
.stack span{font-size:.82rem;padding:4px 12px;background:#f3f3f3;border-radius:6px;font-weight:500}
.note{font-size:.82rem;color:var(--muted);margin-top:10px}
.pager{display:grid;grid-template-columns:1fr 1fr;gap:12px;padding:30px 0 64px;border-top:1px solid var(--line)}
.pager a{border:1px solid var(--line);border-radius:10px;padding:14px 16px;text-decoration:none}
.pager a:hover{border-color:var(--accent)}
.pager small{display:block;font-size:.75rem;color:var(--muted)}
.pager b{font-size:.92rem}
.pager .next{text-align:right}
/* mockups */
.mock{border-radius:12px;overflow:hidden;border:1px solid #2a2a2a;background:#161616;color:#e8e8e8;font-size:.82rem;box-shadow:0 18px 40px rgba(0,0,0,.12);margin-top:30px}
.mock-bar{display:flex;align-items:center;gap:6px;padding:10px 14px;background:#202020;border-bottom:1px solid #2c2c2c}
.mock-bar i{width:10px;height:10px;border-radius:50%;background:#3a3a3a;display:block}
.mock-bar span{margin-left:8px;color:#9a9a9a;font-size:.76rem}
.mock-term{padding:16px 18px;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;line-height:1.75;white-space:pre-wrap;word-break:normal;overflow-wrap:anywhere}
.mock-term .p{color:#e0607e}.mock-term .c{color:#8a8a8a}.mock-term .ok{color:#7fcf9a}
.mock-chat{padding:16px;display:flex;flex-direction:column;gap:10px;background:#f6f6f6;color:var(--text)}
.bubble{max-width:82%;padding:9px 13px;border-radius:14px;font-size:.86rem;line-height:1.55}
.bubble.u{align-self:flex-end;background:var(--ink);color:#fff;border-bottom-right-radius:4px}
.bubble.a{align-self:flex-start;background:#fff;border:1px solid var(--line);border-bottom-left-radius:4px}
.mock-dash{background:#fff;color:var(--text);padding:16px}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(110px,1fr));gap:10px;margin-bottom:12px}
.kpi{border:1px solid var(--line);border-radius:8px;padding:10px 12px}
.kpi small{display:block;font-size:.72rem;color:var(--muted)}
.kpi b{font-size:1.15rem}
.rows div{display:flex;justify-content:space-between;gap:12px;padding:8px 2px;border-top:1px solid #f0f0f0;font-size:.84rem}
.rows div span:last-child{color:var(--muted);text-align:right}
.phone-row{display:flex;gap:14px;justify-content:center;padding:22px 12px;background:#f3f3f3;flex-wrap:wrap}
.phone{width:180px;border-radius:26px;background:#111;padding:8px;box-shadow:0 10px 24px rgba(0,0,0,.15)}
.phone .scr{background:#fff;color:var(--text);border-radius:19px;min-height:330px;padding:16px 12px;font-size:.78rem}
.phone .scr b{display:block;font-size:.9rem;margin-bottom:8px}
.phone .scr div{border:1px solid var(--line);border-radius:8px;padding:7px 9px;margin-bottom:6px;line-height:1.45}
.mock-dark .mock{margin-top:0}
.case-mock{display:none}
/* demo video — 목록 카드는 영상이 주인공: 좁은 폭에선 위, 넓은 폭에선 왼쪽 큰 칸 */
.page-list .wrap{max-width:1240px}
.case-media{position:relative;background:#f4f4f4;border-bottom:1px solid var(--line);order:-1}
.case-media video{display:block;width:100%;aspect-ratio:16/10;object-fit:cover;background:#f4f4f4}
.case.has-media .case-wrap{display:flex;flex-direction:column}
.case.has-media .case-body{flex:1}
.case.has-media .metrics{grid-template-columns:repeat(3,minmax(0,1fr))}
.case.has-media:hover .case-media video{filter:saturate(1.05)}
.case.has-media:hover h2{color:var(--accent)}
.tag.src{background:#fff;border:1px solid var(--line);color:var(--muted);font-weight:600}.tag.src-real{border-color:#cfe6d6;color:#2f7a4b}
.src-tag{position:absolute;left:12px;top:12px;font-size:.72rem;font-weight:700;line-height:1;background:rgba(255,255,255,.94);border:1px solid var(--line);border-radius:999px;padding:5px 10px;color:var(--sub);pointer-events:none}
.demo{margin:30px 0 0;border:1px solid var(--line);border-radius:14px;overflow:hidden;background:#f3f3f3;position:relative;box-shadow:0 18px 40px rgba(0,0,0,.08)}
.demo video{display:block;width:100%;aspect-ratio:16/10;object-fit:cover;cursor:pointer;background:#f3f3f3}
.demo figcaption{display:flex;justify-content:space-between;gap:12px;padding:10px 16px;font-size:.8rem;color:var(--muted);background:#fff;border-top:1px solid var(--line)}
.demo .pp{position:absolute;right:12px;top:12px;width:34px;height:34px;border-radius:50%;background:rgba(20,20,20,.62);color:#fff;font-size:.8rem;display:grid;place-items:center;pointer-events:none;opacity:0;transition:opacity .2s}
.demo.paused .pp{opacity:1}
@media (prefers-reduced-motion:reduce){.case,.demo .pp{transition:none}}
@media (min-width:760px){
 .ps{grid-template-columns:1fr 1fr;gap:24px}
 .d-grid{grid-template-columns:180px 1fr}
 .feats{grid-template-columns:1fr 1fr}
 .case.has-mock{grid-template-columns:1.25fr 1fr}
 .case-mock{display:flex;flex-direction:column;justify-content:center;background:var(--alt);border-left:1px solid var(--line);padding:22px;align-self:stretch}
 .case-mock .mock{margin-top:0;font-size:.74rem}
 .case-mock .phone{width:150px}.case-mock .phone .scr{min-height:250px}
}
@media (min-width:980px){
 .cases{gap:28px}
 .case.has-media{grid-template-columns:minmax(0,1.55fr) minmax(0,1fr)}
 .case-media{order:-1;border-bottom:0;border-right:1px solid var(--line);background:#fff}
 .case-media video{position:sticky;top:16px}
 .case.has-media .case-body{padding:28px 30px 22px}
 .case.has-media .ps{grid-template-columns:1fr;gap:12px}
 .case.has-media h2{font-size:1.4rem}
 .case.has-media .metric{padding:14px 16px}
 .case.has-media .metric b{font-size:1.35rem}
}
@media (max-width:640px){
 .case.has-media .metric{padding:12px 12px}
 .case.has-media .metric b{font-size:1.15rem}
 .case.has-media .metric span{font-size:.74rem}
 .wrap{padding:0 16px}
 .hero h1,.d-hero h1{font-size:1.85rem}
 .case-body{padding:20px 18px}
 .facts div{border-right:0;border-bottom:1px solid var(--line)}
 .toplinks{gap:12px;font-size:.82rem}
 .pager{grid-template-columns:1fr}
 .pager .next{text-align:left}
}
@media print{.topbar,.filters{display:none}.case{break-inside:avoid}}
"""


def head(title, desc, depth, body_cls=""):
    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<link rel="preload" href="/assets/fonts/PretendardVariable.subset.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{'../' * depth}assets/portfolio.css">
</head>
<body{f' class="{body_cls}"' if body_cls else ''}>
<header class="topbar"><div class="wrap">
<a class="brand" href="{'../' * depth}">박준 <span>·</span> PARK JOON</a>
<nav class="toplinks"><a href="{'../' * depth}">개요</a><a href="{'../' * (depth - 1) or './'}"{' aria-current="page"' if depth == 1 else ''}>프로젝트</a><a href="mailto:wns9133@gmail.com">연락</a></nav>
</div></header>
"""


FOOT = """<footer><div class="wrap"><span>박준 | PARK JOON · <a href="mailto:wns9133@gmail.com">wns9133@gmail.com</a></span><span>고객사 정보는 익명화해 컨셉과 결과 위주로 소개합니다.</span></div></footer>
"""


def media_info(slug):
    """portfolio/media/<slug>/ 에 card·poster 가 있으면 영상 정보를, 없으면 None(아직 영상 없는 케이스는 정적 목업 유지)."""
    d = MEDIA / slug
    if not ((d / "card.mp4").exists() and (d / "poster.webp").exists()):
        return None
    meta = {}
    if (d / "meta.json").exists():
        meta = json.loads((d / "meta.json").read_text(encoding="utf-8"))
    return {"source": meta.get("source", "mock"), "demo": (d / "demo.mp4").exists()}


def video_html(prefix, slug, kind, label, cls=""):
    """muted·playsinline·loop·preload=none + poster. 재생은 PLAYER_JS 가 화면에 보일 때만 한다."""
    base = f"{prefix}media/{slug}/"
    return (f'<video class="pv{(" " + cls) if cls else ""}" muted playsinline loop preload="none" '
            f'poster="{E(base)}poster.webp" aria-label="{E(label)}"><source src="{E(base)}{kind}.mp4" type="video/mp4"></video>')


SRC_LABEL = {"real": "실제 화면", "mock": "재구성 목업"}

# 화면에 보일 때만 재생(IntersectionObserver), 벗어나면 일시정지. prefers-reduced-motion 이면 poster 만 보인다.
# 상세 demo 는 클릭으로 일시정지/재생(사용자가 누르면 reduced-motion 이어도 재생).
PLAYER_JS = """<script>
(function(){var vs=[].slice.call(document.querySelectorAll('video.pv'));if(!vs.length)return;
var mq=window.matchMedia?matchMedia('(prefers-reduced-motion: reduce)'):null;
function reduced(){return !!(mq&&mq.matches)}
function play(v){var p=v.play();if(p&&p.catch)p.catch(function(){})}
function auto(v){if(!reduced()&&!v.dataset.user)play(v)}
if('IntersectionObserver' in window){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting)auto(e.target);else e.target.pause()})},{threshold:0.35});vs.forEach(function(v){io.observe(v)})}
else vs.forEach(auto);
vs.forEach(function(v){var f=v.closest('.demo');if(!f)return;
 v.addEventListener('click',function(){if(v.paused){v.dataset.user='';play(v)}else{v.pause();v.dataset.user='1'}});
 v.addEventListener('pause',function(){f.classList.add('paused')});v.addEventListener('play',function(){f.classList.remove('paused')});f.classList.add('paused')});
if(mq&&mq.addEventListener)mq.addEventListener('change',function(){if(reduced())vs.forEach(function(v){v.pause()})});
})();
</script>
"""


def metric_html(m):
    return f'<div class="metric"><b>{E(m["value"])}<small>{E(m.get("unit", ""))}</small></b><span>{E(m["label"])}</span></div>'


def mock_html(mk, title="", max_phones=3):
    if not mk:
        return ""
    kind = mk.get("kind")
    bar = f'<div class="mock-bar"><i></i><i></i><i></i><span>{E(mk.get("title", title))}</span></div>'
    if kind == "terminal":
        lines = []
        for ln in mk.get("lines", []):
            t = E(ln)
            if ln.startswith("$ "):
                t = f'<span class="p">$</span> {E(ln[2:])}'
            elif ln.startswith("# "):
                t = f'<span class="c">{E(ln)}</span>'
            elif ln.startswith(("✓", "OK", "PASS")):
                t = f'<span class="ok">{E(ln)}</span>'
            lines.append(t)
        return f'<div class="mock">{bar}<div class="mock-term">' + "\n".join(lines) + "</div></div>"
    if kind == "chat":
        bs = "".join(f'<div class="bubble {"u" if r == "user" else "a"}">{E(t)}</div>' for r, t in mk.get("messages", []))
        return f'<div class="mock">{bar}<div class="mock-chat">{bs}</div></div>'
    if kind == "dashboard":
        k = "".join(f'<div class="kpi"><small>{E(a)}</small><b>{E(b)}</b></div>' for a, b in mk.get("kpis", []))
        r = "".join(f"<div><span>{E(a)}</span><span>{E(b)}</span></div>" for a, b in mk.get("rows", []))
        return f'<div class="mock">{bar}<div class="mock-dash"><div class="kpis">{k}</div><div class="rows">{r}</div></div></div>'
    if kind == "phone":
        ph = ""
        for sc in mk.get("screens", [])[:max_phones]:
            items = "".join(f"<div>{E(x)}</div>" for x in sc.get("items", []))
            ph += f'<div class="phone"><div class="scr"><b>{E(sc.get("title", ""))}</b>{items}</div></div>'
        return f'<div class="mock" style="background:#f3f3f3;border-color:var(--line)"><div class="phone-row">{ph}</div></div>'
    return ""


def build_index(projects, minor):
    cats = {}
    for p in projects:
        cats[p["category"]] = cats.get(p["category"], 0) + 1
    order = [c for c in CATEGORY_ORDER if c in cats]
    chips = f'<button class="chip" aria-pressed="true" data-f="*">전체<em>{len(projects)}</em></button>' + "".join(
        f'<button class="chip" aria-pressed="false" data-f="{E(c)}">{E(c)}<em>{cats[c]}</em></button>' for c in order
    )
    cards = []
    for p in projects:
        tags = f'<span class="tag cat">{E(p["category"])}</span>' + "".join(f'<span class="tag">{E(t)}</span>' for t in p.get("tags", [])[:3])
        mets = "".join(metric_html(m) for m in p.get("metrics", [])[:3])
        mi = media_info(p["slug"])
        if mi:
            tags += f'<span class="tag src src-{E(mi["source"])}">{SRC_LABEL.get(mi["source"], "")}</span>'
        mk = "" if mi else mock_html(p.get("mock"), p["title"], max_phones=2)
        side = (f'<div class="case-media">{video_html("../", p["slug"], "card", p["title"] + " 데모 영상")}</div>' if mi
                else (f'<div class="case-mock" aria-hidden="true">{mk}</div>' if mk else ''))
        cards.append(f"""<a class="case{' has-media' if mi else (' has-mock' if mk else '')}" href="{E(p['slug'])}/" data-cat="{E(p['category'])}" aria-label="{E(p['title'])} — 자세히 보기">
<div class="case-wrap"><div class="case-body">
<div class="case-top">{tags}<span class="meta-inline">{E(p['period'])} · {E(p['maturity'])}</span></div>
<h2>{E(p['title'])}</h2><p class="one">{E(p['subtitle'])}</p>
<div class="ps"><div><h3>PROBLEM</h3><p>{E(p['problem_short'])}</p></div><div><h3>SOLUTION</h3><p>{E(p['solution_short'])}</p></div></div>
<span class="more">자세히 보기 →</span>
</div>{f'<div class="metrics">{mets}</div>' if mets else ''}</div>
{side}
</a>""")
    delivered = sum(1 for p in projects if p["maturity"] in ("납품 완료", "배포·운영 중"))
    minor_html = "".join(
        f'<div><i>{E(m["category"])}</i><b>{E(m["title"])}</b><span>{E(m["one_liner"])}</span></div>' for m in minor
    )
    desc = "박준이 직접 설계·구현한 AI 에이전트·자동화·앱·음성·교육 프로젝트 케이스 모음"
    out = head("프로젝트 — 박준 | PARK JOON", desc, 1, "page-list") + f"""<main>
<section class="hero"><div class="wrap">
<div class="eyebrow">Case Studies</div>
<h1>아이디어를 실제로 돌아가는<br>결과물로 만듭니다</h1>
<p class="lead">외주·기업 컨설팅·사이드 프로젝트에서 직접 설계하고 구현한 것들입니다. 누구의 일이었는지보다 <b>어떤 문제를 어떤 구조로 풀었고 무엇이 나왔는지</b>를 중심으로 정리했습니다.</p>
<div class="stats"><div class="stat"><b>{len(projects)}</b><span>대표 프로젝트</span></div><div class="stat"><b>{len(order)}</b><span>분야</span></div><div class="stat"><b>{delivered}</b><span>납품·운영 중</span></div><div class="stat"><b>{len(projects) + len(minor)}<small>+</small></b><span>전체 결과물</span></div></div>
<div class="filters" role="group" aria-label="분야 필터">{chips}</div>
</div></section>
<section><div class="wrap"><div class="cases" id="cases">
{''.join(cards)}
</div></div></section>
<section><div class="wrap"><h2 class="section-h">그 밖에 만든 것</h2><div class="minor">{minor_html}</div></div></section>
</main>
{FOOT}<script>
(function(){{var cs=document.querySelectorAll('.chip'),cards=document.querySelectorAll('.case');
function apply(f){{cs.forEach(function(c){{c.setAttribute('aria-pressed',c.dataset.f===f?'true':'false')}});
cards.forEach(function(k){{k.hidden=!(f==='*'||k.dataset.cat===f)}});}}
cs.forEach(function(c){{c.addEventListener('click',function(){{apply(c.dataset.f);try{{history.replaceState(null,'',c.dataset.f==='*'?location.pathname:'#'+encodeURIComponent(c.dataset.f))}}catch(e){{}}}})}});
function fromHash(){{var h=decodeURIComponent(location.hash.slice(1));apply(h&&[].some.call(cs,function(c){{return c.dataset.f===h}})?h:'*')}}
window.addEventListener('hashchange',fromHash);if(location.hash)fromHash();}})();
</script>
{PLAYER_JS}</body></html>
"""
    (OUT / "index.html").write_text(out, encoding="utf-8")


def ul(items):
    return "<ul>" + "".join(f"<li>{E(i)}</li>" for i in items) + "</ul>"


def build_detail(p, prev, nxt):
    tags = f'<span class="tag cat">{E(p["category"])}</span>' + "".join(f'<span class="tag">{E(t)}</span>' for t in p.get("tags", []))
    facts = [("기간", p["period"]), ("형태", p["origin"]), ("상태", p["maturity"]), ("역할", p.get("role", "기획·설계·개발"))]
    facts_html = "".join(f"<div><dt>{E(a)}</dt><dd>{E(b)}</dd></div>" for a, b in facts)
    mets = "".join(metric_html(m) for m in p.get("metrics", []))
    secs = []
    secs.append(("문제", "".join(f"<p>{E(x)}</p>" for x in p["problem"])))
    secs.append(("접근", ul(p["approach"])))
    if p.get("flow"):
        steps = '<div class="arrow"></div>'.join(f'<div class="step"><b>{E(s["label"])}</b><span>{E(s["desc"])}</span></div>' for s in p["flow"])
        secs.append(("구조", f'<div class="flow">{steps}</div>'))
    if p.get("features"):
        secs.append(("주요 기능", '<div class="feats">' + "".join(f'<div class="feat"><b>{E(f["title"])}</b><span>{E(f["desc"])}</span></div>' for f in p["features"]) + "</div>"))
    secs.append(("결과", ul(p["results"])))
    if p.get("insight"):
        secs.append(("포인트", "".join(f"<p>{E(x)}</p>" for x in p["insight"])))
    secs.append(("기술", '<div class="stack">' + "".join(f"<span>{E(t)}</span>" for t in p["tech"]) + "</div>"))
    body = "".join(f'<section class="d-sec"><div class="d-grid"><h2>{E(h)}</h2><div class="body">{b}</div></div></section>' for h, b in secs)
    pager = ""
    if prev:
        pager += f'<a href="../{E(prev["slug"])}/"><small>← 이전</small><b>{E(prev["title"])}</b></a>'
    else:
        pager += "<span></span>"
    if nxt:
        pager += f'<a class="next" href="../{E(nxt["slug"])}/"><small>다음 →</small><b>{E(nxt["title"])}</b></a>'
    mi = media_info(p["slug"])
    if mi and mi["demo"]:
        cap = ("실제 화면 녹화 · 개인정보와 내부 주소는 가렸습니다" if mi["source"] == "real"
               else "재구성 목업 · 실제 화면이 아니라 흐름을 보여 주는 애니메이션입니다")
        hero_media = (f'<figure class="demo">{video_html("../../", p["slug"], "demo", p["title"] + " 데모 영상", "demo-v")}'
                      f'<span class="pp" aria-hidden="true">▶</span><figcaption><span>{E(cap)}</span><span>클릭하면 멈춤·재생</span></figcaption></figure>')
        note = ("상단 영상은 실제 화면을 녹화한 것입니다." if mi["source"] == "real"
                else "상단 영상은 실제 화면이 아니라 구조를 보여 주는 재구성 목업입니다.")
    else:
        hero_media = mock_html(p.get('mock'), p['title'])
        note = "화면 이미지는 실제 화면이 아니라 구조를 보여 주는 재구성 목업입니다."
    out = head(f'{p["title"]} — 박준 프로젝트', p["subtitle"], 2) + f"""<main><div class="wrap">
<div class="crumb"><a href="../">프로젝트</a> / {E(p['category'])}</div>
<section class="d-hero">
<div class="case-top">{tags}</div>
<h1>{E(p['title'])}</h1>
<p class="lead">{E(p['subtitle'])}</p>
<dl class="facts">{facts_html}</dl>
{hero_media}
</section>
{f'<div class="d-metrics"><div class="metrics">{mets}</div></div>' if mets else ''}
{body}
<p class="note">{note}{' 고객 정보는 익명화했습니다.' if p['origin'] in ('의뢰 프로젝트', '기업 프로젝트') else ''}</p>
<nav class="pager" aria-label="프로젝트 이동">{pager}</nav>
</div></main>
{FOOT}{PLAYER_JS}</body></html>
"""
    d = OUT / p["slug"]
    d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(out, encoding="utf-8")


def inject_featured(projects, n=6):
    idx = ROOT / "index.html"
    s = idx.read_text(encoding="utf-8")
    a, b = "<!-- FEATURED:START -->", "<!-- FEATURED:END -->"
    cards = []
    for p in projects[:n]:
        m = (p.get("metrics") or [None])[0]
        mh = f'<div class="fc-metric"><b>{E(m["value"])}{E(m.get("unit", ""))}</b> {E(m["label"])}</div>' if m else ""
        mi = media_info(p["slug"])
        vid = f'<div class="fc-media">{video_html("", p["slug"], "card", p["title"] + " 데모 영상")}</div>' if mi else ""
        cards.append(f'<a class="feat-card{" has-media" if mi else ""}" href="projects/{E(p["slug"])}/">{vid}<div class="fc-cat">{E(p["category"])}</div><div class="fc-title">{E(p["title"])}</div><div class="fc-desc">{E(p["subtitle"])}</div>{mh}</a>')
    style = ("<style>.feat-card.has-media{padding-top:0;overflow:hidden}.fc-media{margin:0 -20px 14px;border-bottom:1px solid var(--card-border);background:#f3f3f3}"
             ".fc-media video{display:block;width:100%;aspect-ratio:16/10;object-fit:cover}"
             ".feat-card.has-media:hover .fc-title{color:var(--accent)}"
             "@media (min-width:700px){.feat-grid{grid-template-columns:1fr 1fr;gap:18px}}</style>")
    block = a + "\n" + style + '\n<div class="feat-grid">' + "".join(cards) + "</div>\n" + PLAYER_JS + b
    s = s[: s.index(a)] + block + s[s.index(b) + len(b):]
    idx.write_text(s, encoding="utf-8")


def main():
    projects = DATA["projects"]
    projects.sort(key=lambda p: (-p.get("weight", 0), CATEGORY_ORDER.index(p["category"]) if p["category"] in CATEGORY_ORDER else 99))
    OUT.mkdir(exist_ok=True)
    (ROOT / "assets").mkdir(exist_ok=True)
    (ROOT / "assets" / "portfolio.css").write_text(CSS.strip() + "\n", encoding="utf-8")
    minor_path = ROOT / "_build" / "minor.json"
    minor = [{"category": c, "title": t, "one_liner": o} for c, t, o in json.loads(minor_path.read_text(encoding="utf-8"))] if minor_path.exists() else DATA.get("minor", [])
    DATA["minor"] = minor
    build_index(projects, minor)
    inject_featured(projects)
    for i, p in enumerate(projects):
        build_detail(p, projects[i - 1] if i > 0 else None, projects[i + 1] if i + 1 < len(projects) else None)
    print(f"built {len(projects)} detail pages + index, minor {len(DATA.get('minor', []))}")


if __name__ == "__main__":
    main()
