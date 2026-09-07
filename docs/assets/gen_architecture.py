# -*- coding: utf-8 -*-
"""02 §4 아키텍처 도식 생성. 수정 후: python3 docs/assets/gen_architecture.py"""
W, H = 1480, 1372
FONT = "NanumGothic, 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif"
C = dict(ink="#0F172A", sub="#475569", mute="#64748B", line="#94A3B8", rule="#E2E8F0",
         a1="#0F766E", a1b="#F0FDFA", a4="#1D4ED8", a4b="#EFF6FF", a2="#6D28D9", a2b="#F5F3FF",
         a3="#64748B", a3b="#F8FAFC", a5="#C2410C", a5b="#FFF7ED",
         bg_="#15803D", bgb="#F0FDF4", boxb="#CBD5E1", soft="#F8FAFC")
o=[]
def esc(t): return t.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
def rect(x,y,w,h,fill,stroke=None,rx=8,sw=1.4,dash=None):
    s=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"'
    if stroke: s+=f' stroke="{stroke}" stroke-width="{sw}"'
    if dash: s+=f' stroke-dasharray="{dash}"'
    o.append(s+'/>')
def txt(x,y,t,size=12,fill=C["ink"],weight="400",anchor="start",ls=0):
    o.append(f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" fill="{fill}" '
             f'font-weight="{weight}" text-anchor="{anchor}" letter-spacing="{ls}">{esc(t)}</text>')
def lines(x,y,arr,size=11,fill=C["sub"],lh=15.5,weight="400"):
    for i,t in enumerate(arr): txt(x,y+i*lh,t,size,fill,weight)
def vline(x,y1,y2,col=C["line"],sw=1.6,dash=None):
    d=f' stroke-dasharray="{dash}"' if dash else ''
    o.append(f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="{col}" stroke-width="{sw}"{d}/>')
def hline(x1,x2,y,col=C["line"],sw=1.6,dash=None):
    d=f' stroke-dasharray="{dash}"' if dash else ''
    o.append(f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{col}" stroke-width="{sw}"{d}/>')
def arrow(x,y1,y2,col=C["line"],sw=1.8,mk="ah"):
    o.append(f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2-7}" stroke="{col}" stroke-width="{sw}" marker-end="url(#{mk})"/>')

o.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
o.append('<defs>'
 f'<marker id="ah" markerWidth="9" markerHeight="9" refX="4.5" refY="4.5" orient="auto"><path d="M0,0 L9,4.5 L0,9 z" fill="{C["line"]}"/></marker>'
 f'<marker id="ag" markerWidth="9" markerHeight="9" refX="4.5" refY="4.5" orient="auto"><path d="M0,0 L9,4.5 L0,9 z" fill="{C["bg_"]}"/></marker>'
 f'<marker id="at" markerWidth="9" markerHeight="9" refX="4.5" refY="4.5" orient="auto"><path d="M0,0 L9,4.5 L0,9 z" fill="{C["a1"]}"/></marker>'
 f'<marker id="ab" markerWidth="9" markerHeight="9" refX="4.5" refY="4.5" orient="auto"><path d="M0,0 L9,4.5 L0,9 z" fill="{C["a4"]}"/></marker>'
 '</defs>')
rect(0,0,W,H,"#FFFFFF",rx=0)

txt(40,52,"시설작물 이미지 신뢰성 판별 — 시스템 구조",26,C["ink"],"800")
txt(40,80,"생성 흔적(축 A) + 농업적 정합성(축 B) 두 축을 가중합해 판정 · 작물 분할은 1회, 용도는 2개",14,C["sub"])
hline(40,W-40,100,C["rule"],1.2)

rect(460,122,560,44,C["soft"],C["boxb"])
txt(740,150,"입력 이미지 — 원본 해상도 유지 (리사이즈 금지, 크롭만 사용)",13.5,C["ink"],"700","middle")
arrow(740,166,196)

# ── 축 A ──
txt(41,214,"축 A · 생성 흔적",15,C["ink"],"800")
txt(180,214,"각 생성 계열이 이미지를 만드는 방식에서 지표를 유도 · 원본 전체를 본다",11.5,C["mute"])
hline(41,1439,224,C["rule"],1.2)
AY,AH,AW = 238,214,262
A=[(41,"A1","잠재-디코더",C["a1"],C["a1b"],["확산-U-Net · 플로우매칭(DiT)","증류 · 잠재 인페인팅"],
    ["잠재 생성 모델의 출력은","예외 없이 VAE 디코더를","통과한다. 재구성 오차가","실제 촬영물보다 작다"],"학습 불요","1순위",False),
   (325,"A4","영역 대조",C["a4"],C["a4b"],["픽셀 공간 합성","= 공고문 유형 ①②"],
    ["배경을 건드리지 않으므로","마스크 안팎의 노이즈·색온도·","초점·조명·압축 이력이","서로 어긋난다"],"자체 학습","2순위",True),
   (609,"A2","스펙트럼",C["a2"],C["a2b"],["GAN · 픽셀 확산"],
    ["업샘플이 주파수 영역에","스펙트럼 복제를 남기고,","자연 이미지의 고주파","감쇠 곡선을 못 따라간다"],"학습 불요","3순위",False),
   (893,"A3","양자화",C["a3"],C["a3b"],["오토리그레시브","(토큰 예측)"],
    ["유한 코드북 양자화 오차의","구조가 다르다. 노이즈에서","출발하지 않아 A1·A2가","원리적으로 통하지 않는다"],"학습 불요","선택",False),
   (1177,"A5","전역 판별 모델",C["a5"],C["a5b"],["전 유형 (안전망)"],
    ["계열 지식 없이 이미지를","통째로 입력받는 학습","기반 이진 분류. 지표가","놓치는 것을 받아낸다"],"파인튜닝","1주차 단독",False)]
for x,code,name,col,bg,aim,why,b1,b2,usemask in A:
    rect(x,AY,AW,AH,bg,col,sw=1.6)
    o.append(f'<path d="M{x},{AY+8} a8,8 0 0 1 8,-8 h{AW-16} a8,8 0 0 1 8,8 v26 h-{AW} z" fill="{col}"/>')
    txt(x+15,AY+24,code,16.5,"#FFFFFF","800"); txt(x+15+len(code)*11+9,AY+24,name,14,"#FFFFFF","700")
    txt(x+15,AY+56,"겨냥",9.5,col,"700",ls=1.2); lines(x+15,AY+73,aim,11.5,C["ink"],16,"700")
    ly=AY+73+len(aim)*16+12
    txt(x+15,ly,"판별 원리",9.5,col,"700",ls=1.2); lines(x+15,ly+18,why,11,C["sub"],15.5)
    by=AY+AH-18
    rect(x+15,by-13,62,19,"#FFFFFF",col,rx=9,sw=1); txt(x+46,by,b1,9.5,col,"700","middle")
    txt(x+85,by,b2,9.5,C["mute"],"700")
    if usemask:
        rect(x+AW-92,AY+40,84,20,"#FFFFFF",col,rx=10,sw=1.3)
        txt(x+AW-50,AY+54,"마스크 사용",9.5,col,"800","middle")

# ── 작물 분할 ──
SY=AY+AH+34
for x,*_ in A: vline(x+AW/2,AY+AH,SY-16)
hline(41+AW/2,1177+AW/2,SY-16)
rect(520,SY,440,52,"#0F172A",rx=9)
txt(740,SY+22,"작물 분할 (SAM 계열, Apache-2.0)  →  마스크 M",13,"#FFFFFF","800","middle")
txt(740,SY+40,"1회 실행 · 실패 시 균일 패치 격자로 폴백",10.5,"#94A3B8","400","middle")
# 마스크 → A4 (점선, 위로)
o.append(f'<path d="M960,{SY+26} H1010 V{AY+AH+12} H456 V{AY+AH}" fill="none" stroke="{C["a4"]}" '
         f'stroke-width="1.8" stroke-dasharray="5 4" marker-end="url(#ab)"/>')
txt(1018,SY+20,"영역 정의 → A4",10.5,C["a4"],"800")
# 마스크 → 축 B
o.append(f'<line x1="740" y1="{SY+52}" x2="740" y2="{SY+82}" stroke="{C["bg_"]}" stroke-width="2" marker-end="url(#ag)"/>')
txt(752,SY+76,"누끼 → 축 B",10.5,C["bg_"],"800")

# ── 축 B ──
BLY=SY+112
txt(41,BLY,"축 B · 농업적 정합성",15,C["bg_"],"800")
txt(230,BLY,"실제 작물이라면 지켜야 할 규칙 — 실제 이미지만으로 학습 → 미지 생성기와 무관 · 후처리에 강함",11.5,C["mute"])
hline(41,1439,BLY+10,C["rule"],1.2)
BY,BH,BW=BLY+24,168,452
B=[(41,"B1","형태 정합성",["잎맥 위상 · 엽서(phyllotaxis) 배열 · 과실–잎 스케일"],
    ["잎맥은 임의의 그물이 아니라 통수 효율과 손상 내성이","제약하는 계층 네트워크다. 무방향 그래프로 추출해","분기 차수 분포 · 폐루프 비율 · 세맥 길이 비율을 계산"],"종 확정 후"),
   (515,"B2","시설 구조물",["점적관수 라인 · 유인줄 · 하이와이어 · 피복재 격자"],
    ["Hough 직선 검출 개수·길이 분포, 자기상관/FFT 주기","피크의 선명도. 생성 모델은 긴 직선과 등간격 반복에서","실패한다"],"종 무관 · 우선"),
   (989,"B3","생육 정합성",["병징의 해부학적 일관성 · 착과 순서 · 생육단계"],
    ["병반이 잎맥을 따라 번지는가 무작위로 찍혀 있는가.","마스크 내 병반 분포와 잎맥 골격의 정렬도를 측정"],"종 확정 후")]
for x,code,name,aim,why,badge in B:
    rect(x,BY,BW,BH,C["bgb"],C["bg_"],sw=1.6)
    o.append(f'<path d="M{x},{BY+8} a8,8 0 0 1 8,-8 h{BW-16} a8,8 0 0 1 8,8 v26 h-{BW} z" fill="{C["bg_"]}"/>')
    txt(x+15,BY+24,code,16.5,"#FFFFFF","800"); txt(x+15+len(code)*11+9,BY+24,name,14,"#FFFFFF","700")
    rect(x+BW-104,BY+40,94,20,"#FFFFFF",C["bg_"],rx=10,sw=1.3)
    txt(x+BW-57,BY+54,badge,9.5,C["bg_"],"800","middle")
    txt(x+15,BY+56,"대상",9.5,C["bg_"],"700",ls=1.2); lines(x+15,BY+73,aim,11.5,C["ink"],16,"700")
    txt(x+15,BY+99,"계량 방법",9.5,C["bg_"],"700",ls=1.2); lines(x+15,BY+117,why,10.5,C["sub"],15)

# ── 가중합 ──
GRAIL=BY+BH+28
for x,*_ in B: vline(x+BW/2,BY+BH,GRAIL)
hline(41+BW/2,989+BW/2,GRAIL)
arrow(740,GRAIL,GRAIL+34)
GY=GRAIL+34
rect(330,GY,820,62,C["soft"],C["boxb"])
txt(740,GY+27,"score  =  w1·A1 + w2·A2 + w3·A3 + w4·A4 + w5·A5  +  v1·B1 + v2·B2 + v3·B3",14,C["ink"],"800","middle")
txt(740,GY+47,"가중치는 Leave-One-Generator-Out 교차검증으로 결정 · 축 A와 축 B의 배분은 별도 관리",11,C["mute"],"400","middle")
arrow(740,GY+62,GY+94)
rect(540,GY+94,400,44,"#0F172A",rx=22)
txt(740,GY+122,"score ≥ 임계값 τ   →   생성 이미지",15,"#FFFFFF","700","middle")

# ── 하단 근거 ──
PY_=GY+186
hline(40,W-40,PY_-30,C["rule"],1.2)
txt(40,PY_,"핵심 근거 — 왜 이렇게 나누는가",17,C["ink"],"800")
by0=PY_+22; PH=246

bx,bw=40,690
rect(bx,by0,bw,PH,"#FFFFFF",C["boxb"])
o.append(f'<rect x="{bx}" y="{by0}" width="5" height="{PH}" rx="2.5" fill="{C["a1"]}"/>')
txt(bx+22,by0+30,"① VAE 디코더는 생성 계열을 가로지르는 공용 부품이다",13.5,C["a1"],"800")
fam=["확산-U-Net  (SD1.5 · SDXL)","플로우 매칭 DiT  (SD3 · FLUX)","증류·소수스텝  (Turbo · schnell)","잠재 인페인팅  (유형 ①②의 절반)"]
fy=by0+56
for i,f in enumerate(fam):
    rect(bx+22,fy+i*32,240,25,C["a1b"],C["a1"],rx=6,sw=1); txt(bx+34,fy+i*32+17,f,10.5,C["a1"],"700")
    hline(bx+262,bx+300,fy+i*32+12,C["a1"],1.2)
vline(bx+300,fy+12,fy+3*32+12,C["a1"],1.6)
o.append(f'<line x1="{bx+300}" y1="{fy+52}" x2="{bx+350}" y2="{fy+52}" stroke="{C["a1"]}" stroke-width="2" marker-end="url(#at)"/>')
rect(bx+360,fy+28,148,48,C["a1"],rx=8)
txt(bx+434,fy+48,"VAE 디코더",13,"#FFFFFF","800","middle"); txt(bx+434,fy+65,"(잠재 → 픽셀)",9.5,"#CCFBF1","400","middle")
o.append(f'<line x1="{bx+508}" y1="{fy+52}" x2="{bx+556}" y2="{fy+52}" stroke="{C["a1"]}" stroke-width="2" marker-end="url(#at)"/>')
txt(bx+564,fy+56,"출력 픽셀",11,C["ink"],"700")
o.append(f'<line x1="{bx+434}" y1="{fy+112}" x2="{bx+434}" y2="{fy+84}" stroke="{C["a1"]}" stroke-width="2" marker-end="url(#at)"/>')
rect(bx+374,fy+114,120,23,"#FFFFFF",C["a1"],rx=11,sw=1.5)
txt(bx+434,fy+130,"A1 이 여기를 본다",10,C["a1"],"800","middle")
lines(bx+22,by0+212,["지표 하나가 네 계열을 동시에 겨냥한다. 운영측 생성기가 비공개라는 본 대회의",
                     "근본 난제에 대한 주된 대비책이다."],11,C["sub"],16)

cx,cw=750,690
rect(cx,by0,cw,PH,"#FFFFFF",C["boxb"])
o.append(f'<rect x="{cx}" y="{by0}" width="5" height="{PH}" rx="2.5" fill="{C["a4"]}"/>')
txt(cx+22,by0+30,"② 작물 분할은 한 번, 용도는 두 개",13.5,C["a4"],"800")
rect(cx+22,by0+52,116,40,"#0F172A",rx=8)
txt(cx+80,by0+70,"마스크 M",11.5,"#FFFFFF","800","middle"); txt(cx+80,by0+85,"분할 1회",9.5,"#94A3B8","400","middle")
hline(cx+138,cx+166,by0+72,C["line"],1.6); vline(cx+166,by0+54,by0+112,C["line"],1.6)
for y,col,mk,t1,t2 in [(by0+54,C["bg_"],"ag","누끼  →  축 B 농업 정합성","작물만 남겨 형태·구조를 본다"),
                       (by0+96,C["a4"],"ab","영역 정의  →  A4 영역 대조","안팎 통계를 대조한다 (자르지 않는다)")]:
    o.append(f'<line x1="{cx+166}" y1="{y+18}" x2="{cx+196}" y2="{y+18}" stroke="{col}" stroke-width="1.8" marker-end="url(#{mk})"/>')
    rect(cx+204,y,452,36,"#FFFFFF",col,rx=7,sw=1.4)
    txt(cx+218,y+16,t1,11.5,col,"800"); txt(cx+218,y+30,t2,10,C["mute"])
txt(cx+22,by0+156,"유형 ①② 분담",10,C["ink"],"800",ls=0.8)
for i,(tag,col,t1,t2) in enumerate([("G-1",C["a4"],"픽셀 공간 합성 (알파·Poisson·하모나이제이션)","영역 불일치가 남는다  →  A4"),
                                     ("G-2",C["a1"],"잠재 공간 재생성 (SD 인페인팅·img2img)","전체 재디코딩  →  영역 대조 무력  →  A1")]):
    yy=by0+166+i*24
    rect(cx+22,yy,38,19,col,rx=5); txt(cx+41,yy+14,tag,10,"#FFFFFF","800","middle")
    txt(cx+68,yy+14,t1,10.5,C["ink"],"700"); txt(cx+352,yy+14,t2,10.5,col,"700")
lines(cx+22,by0+232,["분할 비용은 1회인데 판별 근거는 둘이 된다. 유형 ①②는 두 갈래로 갈리고 탐지 원리가 정반대라, A4와 A1이 나눠 담당한다."],11,C["sub"],16)

txt(40,H-24,"제1회 전국 농과계 대학 농업 AI 경진대회 · 이미지 데이터 신뢰성 판별 미션",10.5,C["mute"])
txt(W-40,H-24,"2026-09-07",10.5,C["mute"],anchor="end")
o.append('</svg>')
open("docs/assets/architecture.svg","w",encoding="utf-8").write("\n".join(o))
print("SVG written", W, H)
