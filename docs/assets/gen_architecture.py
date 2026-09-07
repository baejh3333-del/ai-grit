# -*- coding: utf-8 -*-
W, H = 1480, 1200
FONT = "NanumGothic, 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif"

C = dict(
    ink="#0F172A", sub="#475569", mute="#64748B", line="#94A3B8", rule="#E2E8F0",
    s1="#0F766E", s1b="#F0FDFA", s2="#6D28D9", s2b="#F5F3FF",
    s3="#1D4ED8", s3b="#EFF6FF", s4="#64748B", s4b="#F8FAFC",
    s5="#C2410C", s5b="#FFF7ED", box="#FFFFFF", boxb="#CBD5E1", soft="#F8FAFC",
)
o = []
def esc(t): return t.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
def rect(x,y,w,h,fill,stroke=None,rx=8,sw=1.4,dash=None):
    s=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"'
    if stroke: s+=f' stroke="{stroke}" stroke-width="{sw}"'
    if dash: s+=f' stroke-dasharray="{dash}"'
    o.append(s+'/>')
def txt(x,y,t,size=12,fill=C["ink"],weight="400",anchor="start",ls=0,op=1):
    o.append(f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" fill="{fill}" '
             f'font-weight="{weight}" text-anchor="{anchor}" letter-spacing="{ls}" opacity="{op}">{esc(t)}</text>')
def lines(x,y,arr,size=11.5,fill=C["sub"],lh=17,weight="400",anchor="start"):
    for i,t in enumerate(arr): txt(x,y+i*lh,t,size,fill,weight,anchor)
def vline(x,y1,y2,col=C["line"],sw=1.6,dash=None):
    d=f' stroke-dasharray="{dash}"' if dash else ''
    o.append(f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="{col}" stroke-width="{sw}"{d}/>')
def hline(x1,x2,y,col=C["line"],sw=1.6,dash=None):
    d=f' stroke-dasharray="{dash}"' if dash else ''
    o.append(f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{col}" stroke-width="{sw}"{d}/>')
def arrow(x,y1,y2,col=C["line"],sw=1.8):
    o.append(f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2-7}" stroke="{col}" stroke-width="{sw}" marker-end="url(#ah)"/>')

o.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
o.append(f'<defs><marker id="ah" markerWidth="9" markerHeight="9" refX="4.5" refY="4.5" orient="auto">'
         f'<path d="M0,0 L9,4.5 L0,9 z" fill="{C["line"]}"/></marker>'
         f'<marker id="ahd" markerWidth="9" markerHeight="9" refX="4.5" refY="4.5" orient="auto">'
         f'<path d="M0,0 L9,4.5 L0,9 z" fill="{C["s1"]}"/></marker></defs>')
rect(0,0,W,H,"#FFFFFF",rx=0)

# ─── 헤더 ───
txt(40,52,"시설작물 이미지 신뢰성 판별 — 시스템 구조",26,C["ink"],"800")
txt(40,80,"생성 계열별 전문 지표 + 전역 판별 모델 → 가중합 → 임계값 판정",14,C["sub"])
hline(40,W-40,100,C["rule"],1.2)

# ─── 입력 ───
rect(480,124,520,46,C["soft"],C["boxb"])
txt(740,153,"입력 이미지 — 원본 해상도 유지 (리사이즈 금지, 크롭만 사용)",13.5,C["ink"],"700","middle")
arrow(740,170,196)

# ─── [0] 라우팅 ───
rect(390,196,700,58,"#FFFFFF",C["boxb"],dash="5 4")
txt(740,220,"[0] 작물 종 라우팅  —  조건부 (종 구성 확정 시)",13.5,C["ink"],"700","middle")
txt(740,240,"종 분류기 → 종별 경량 어댑터  ·  라우터 실패 시 전역 어댑터로 폴백",11.5,C["mute"],"400","middle")
arrow(740,254,286)

# ─── 그룹 라벨 ───
txt(42,304,"[ 1 ]  계열별 전문 지표 — 각 계열이 이미지를 만드는 방식에서 유도",12.5,C["ink"],"700",ls=0.2)
txt(1178,304,"[ 2 ]  전역 판별 모델",12.5,C["ink"],"700",ls=0.2)
hline(42,1150,312,C["rule"],1.2); hline(1178,1440,312,C["rule"],1.2)

# ─── 지표 카드 ───
CY, CH, CW = 326, 250, 262
cards = [
 (42,   "S1", "잠재-디코더", C["s1"], C["s1b"],
  ["확산-잠재 · 플로우 매칭","증류 · 잠재 인페인팅"],
  ["잠재 생성 모델의 출력은","예외 없이 VAE 디코더를","통과한다. 그 디코더로","재구성하면 자기 계열","생성물을 더 정확히 복원"],
  "학습 불요", "1순위"),
 (324,  "S3", "영역 대조", C["s3"], C["s3b"],
  ["편집·합성 (픽셀 공간)","= 공고문 유형 ①②"],
  ["픽셀 합성은 배경을 건드","리지 않으므로 작물 마스크","안팎의 노이즈·색온도·","초점·조명·압축 이력이","서로 어긋난다"],
  "자체 학습", "2순위"),
 (606,  "S2", "스펙트럼", C["s2"], C["s2b"],
  ["GAN · 픽셀 확산"],
  ["업샘플 연산이 주파수","영역에 스펙트럼 복제를","남기고, 생성 이미지는","자연 이미지의 고주파","감쇠 곡선을 못 따라간다"],
  "학습 불요", "3순위"),
 (888,  "S4", "양자화", C["s4"], C["s4b"],
  ["오토리그레시브","(토큰 예측 방식)"],
  ["유한 코드북으로 양자화","하므로 그 오차의 구조가","실제 촬영 이미지와","다르다. 노이즈에서","출발하지 않는 계열"],
  "학습 불요", "선택"),
 (1178, "S5", "전역 판별 모델", C["s5"], C["s5b"],
  ["전 유형 (안전망)"],
  ["계열 지식 없이 이미지를","통째로 입력받는 학습","기반 이진 분류.","계열 지표가 원리적으로","놓치는 것을 받아낸다"],
  "파인튜닝", "1주차 단독 제출"),
]
for x,code,name,col,bg,aim,why,b1,b2 in cards:
    rect(x,CY,CW,CH,bg,col,sw=1.6)
    o.append(f'<path d="M{x},{CY+8} a8,8 0 0 1 8,-8 h{CW-16} a8,8 0 0 1 8,8 v26 h-{CW} z" fill="{col}"/>')
    txt(x+16,CY+24,code,16.5,"#FFFFFF","800")
    txt(x+16+len(code)*11+9,CY+24,name,14,"#FFFFFF","700")
    txt(x+16,CY+58,"겨냥",9.5,col,"700",ls=1.2)
    lines(x+16,CY+75,aim,11.5,C["ink"],16,"700")
    ly=CY+75+len(aim)*16+12
    txt(x+16,ly,"판별 원리",9.5,col,"700",ls=1.2)
    lines(x+16,ly+18,why,11,C["sub"],15.5)
    by=CY+CH-20
    rect(x+16,by-13,62,19,"#FFFFFF",col,rx=9,sw=1)
    txt(x+47,by,b1,9.5,col,"700","middle")
    txt(x+86,by,b2,9.5,C["mute"],"700")

# ─── 수렴 ───
RAIL = CY+CH+30
for x,*_ in cards: vline(x+CW/2, CY+CH, RAIL)
hline(42+CW/2, 1178+CW/2, RAIL)
arrow(740, RAIL, RAIL+34)

# ─── [3] 가중합 ───
GY = RAIL+34
rect(390,GY,700,62,C["soft"],C["boxb"])
txt(740,GY+27,"[3]   score  =  w1·S1 + w2·S2 + w3·S3 + w4·S4 + w5·S5",14.5,C["ink"],"800","middle")
txt(740,GY+47,"가중치 w 는 Leave-One-Generator-Out 교차검증으로 결정 · 각 지표는 검증셋 기준 정규화 후 합산",11,C["mute"],"400","middle")
arrow(740,GY+62,GY+94)
rect(540,GY+94,400,44,"#0F172A",rx=22)
txt(740,GY+122,"score ≥ 임계값 τ   →   생성 이미지",15,"#FFFFFF","700","middle")

# ─── 하단 근거 패널 ───
PY_ = GY+186
hline(40,W-40,PY_-30,C["rule"],1.2)
txt(40,PY_,"핵심 근거 — 왜 이렇게 나누는가",17,C["ink"],"800")

# ① VAE 공용
bx, by0, bw = 40, PY_+22, 690
rect(bx,by0,bw,280,"#FFFFFF",C["boxb"])
o.append(f'<rect x="{bx}" y="{by0}" width="5" height="280" rx="2.5" fill="{C["s1"]}"/>')
txt(bx+22,by0+30,"① VAE 디코더는 생성 계열을 가로지르는 공용 부품이다",13.5,C["s1"],"800")
fam=["확산-잠재  (SD1.5 · SDXL)","플로우 매칭  (SD3 · FLUX)","증류·소수스텝  (Turbo · schnell)","잠재 인페인팅  (유형 ①②의 절반)"]
fy=by0+58
for i,f in enumerate(fam):
    rect(bx+22,fy+i*34,236,26,C["s1b"],C["s1"],rx=6,sw=1)
    txt(bx+34,fy+i*34+18,f,11,C["s1"],"700")
    hline(bx+258,bx+300,fy+i*34+13,C["s1"],1.2)
vline(bx+300,fy+13,fy+3*34+13,C["s1"],1.6)
o.append(f'<line x1="{bx+300}" y1="{fy+55}" x2="{bx+352}" y2="{fy+55}" stroke="{C["s1"]}" stroke-width="2" marker-end="url(#ahd)"/>')
rect(bx+362,fy+30,150,52,C["s1"],rx=8)
txt(bx+437,fy+52,"VAE 디코더",13,"#FFFFFF","800","middle")
txt(bx+437,fy+70,"(잠재 → 픽셀)",10,"#CCFBF1","400","middle")
o.append(f'<line x1="{bx+512}" y1="{fy+55}" x2="{bx+560}" y2="{fy+55}" stroke="{C["s1"]}" stroke-width="2" marker-end="url(#ahd)"/>')
txt(bx+568,fy+59,"출력 픽셀",11.5,C["ink"],"700")
vline(bx+437,fy+118,fy+90,C["s1"],2)
o.append(f'<line x1="{bx+437}" y1="{fy+118}" x2="{bx+437}" y2="{fy+88}" stroke="{C["s1"]}" stroke-width="2" marker-end="url(#ahd)"/>')
rect(bx+372,fy+120,130,24,"#FFFFFF",C["s1"],rx=12,sw=1.5)
txt(bx+437,fy+137,"S1 이 여기를 본다",10.5,C["s1"],"800","middle")
lines(bx+22,by0+240,["지표 하나가 네 계열을 동시에 겨냥한다. 운영측 생성기가 비공개라는",
                     "본 대회의 근본 난제에 대한 우리의 주된 대비책이다."],11.5,C["sub"],17)

# ② 유형 ①② 분할
cx, cw = 750, 690
rect(cx,by0,cw,280,"#FFFFFF",C["boxb"])
o.append(f'<rect x="{cx}" y="{by0}" width="5" height="280" rx="2.5" fill="{C["s3"]}"/>')
txt(cx+22,by0+30,"② 유형 ①②는 두 갈래로 갈리고, 탐지 원리가 정반대다",13.5,C["s3"],"800")
rect(cx+22,by0+50,120,40,"#0F172A",rx=8)
txt(cx+82,by0+68,"공고문",11,"#FFFFFF","700","middle")
txt(cx+82,by0+83,"유형 ①②",12.5,"#FFFFFF","800","middle")
hline(cx+142,cx+172,by0+70,C["line"],1.6)
vline(cx+172,by0+70,by0+168,C["line"],1.6)
for i,(y,tag,col,bgc,t1,t2,t3) in enumerate([
    (by0+52,"G-1",C["s3"],C["s3b"],"픽셀 공간 합성","알파 · Poisson · 하모나이제이션",
     "배경 픽셀을 건드리지 않는다  →  영역 간 불일치가 남는다"),
    (by0+146,"G-2",C["s1"],C["s1b"],"잠재 공간 재생성","SD 인페인팅 · img2img",
     "마스크 밖까지 전체 재디코딩  →  영역 대조가 무력해진다")]):
    o.append(f'<line x1="{cx+172}" y1="{y+22}" x2="{cx+204}" y2="{y+22}" stroke="{C["line"]}" stroke-width="1.6" marker-end="url(#ah)"/>')
    rect(cx+212,y,300,46,bgc,col,rx=7,sw=1.4)
    txt(cx+226,y+19,tag,11.5,col,"800")
    txt(cx+262,y+19,t1,12,C["ink"],"700")
    txt(cx+226,y+36,t2,10.5,C["mute"])
    o.append(f'<line x1="{cx+512}" y1="{y+22}" x2="{cx+552}" y2="{y+22}" stroke="{col}" stroke-width="2" marker-end="url(#ah)"/>')
    rect(cx+560,y+6,60,32,col,rx=7)
    txt(cx+590,y+27,"S3" if i==0 else "S1",15,"#FFFFFF","800","middle")
    txt(cx+212,y+64,t3,10.5,col,"700")
lines(cx+22,by0+240,["둘 중 하나만으로는 유형 ①②의 절반만 잡는다. S1과 S3는 경쟁이",
                     "아니라 상호 보완 관계이며, 검증도 G-1/G-2로 쪼개서 측정한다."],11.5,C["sub"],17)

txt(40,H-22,"제1회 전국 농과계 대학 농업 AI 경진대회 · 이미지 데이터 신뢰성 판별 미션",10.5,C["mute"])
txt(W-40,H-22,"2026-09-07",10.5,C["mute"],anchor="end")
o.append('</svg>')
open("docs/assets/architecture.svg","w",encoding="utf-8").write("\n".join(o))
print("SVG written")
