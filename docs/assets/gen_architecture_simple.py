# -*- coding: utf-8 -*-
"""수행계획서 인쇄용 간략 도식. python3 docs/assets/gen_architecture_simple.py"""
W,H = 1400, 632
F = "NanumGothic, 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif"
INK="#111827"; SUB="#4B5563"; LINE="#6B7280"
A="#0F766E"; AB="#F0FDFA"; B="#15803D"; BB="#F0FDF4"; NB="#F9FAFB"; NL="#9CA3AF"
o=[]
def esc(t): return t.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
def rect(x,y,w,h,fill,stroke,rx=10,sw=2.4):
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
def txt(x,y,t,size=19,fill=INK,weight="400",anchor="start"):
    o.append(f'<text x="{x}" y="{y}" font-family="{F}" font-size="{size}" fill="{fill}" '
             f'font-weight="{weight}" text-anchor="{anchor}">{esc(t)}</text>')
def path(d,col=LINE,sw=2.6,mk="a"):
    o.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{sw}" marker-end="url(#{mk})"/>')
def arrow(x,y1,y2,col=LINE,sw=2.6,mk="a"):
    o.append(f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="{col}" stroke-width="{sw}" marker-end="url(#{mk})"/>')

o.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
o.append('<defs>'
 f'<marker id="a" markerWidth="10" markerHeight="10" refX="5" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{LINE}"/></marker>'
 f'<marker id="ga" markerWidth="10" markerHeight="10" refX="5" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{B}"/></marker>'
 f'<marker id="ta" markerWidth="10" markerHeight="10" refX="5" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{A}"/></marker>'
 '</defs>')
o.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="#FFFFFF"/>')

AX,AW = 44,580        # 축 A          44..624   center 334
RX,RW = 756,600       # 우측 컬럼     756..1356 center 1056
CC    = 695           # 하단 중심

# 입력
rect(390,18,620,54,NB,NL)
txt(700,53,"입력 이미지 — 원본 해상도 유지 (리사이즈 금지)",22,INK,"700","middle")
o.append(f'<path d="M700,72 V96 M334,96 H1056" fill="none" stroke="{LINE}" stroke-width="2.6"/>')
arrow(334,96,128); arrow(1056,96,128)

# 축 A
rect(AX,134,AW,286,AB,A)
o.append(f'<path d="M{AX},{134+10} a10,10 0 0 1 10,-10 h{AW-20} a10,10 0 0 1 10,10 v36 h-{AW} z" fill="{A}"/>')
txt(AX+22,170,"축 A · 생성 흔적",25,"#FFFFFF","800")
txt(AX+AW-22,170,"원본 전체를 본다",15,"#CCFBF1","400","end")
y=214
for c,n,dd in [("A1","VAE 재구성 오차",["확산 · 플로우매칭 · 증류"]),
               ("A2","주파수 이상",["GAN"]),
               ("A4","마스크 안팎 대조",["실험실 작물 + 현장 배경 결합",
                                        "현장 작물 + 다른 현장 배경 결합"]),
               ("A5","전역 분류기",["전 유형 안전망"])]:
    txt(AX+22,y,c,21,A,"800"); txt(AX+68,y,n,21,INK,"700")
    for j,d in enumerate(dd): txt(AX+280,y+j*23,d,15.5,SUB)
    y += 46 if len(dd)==1 else 70

# 작물 분할
rect(RX,134,RW,60,"#111827","#111827")
txt(RX+RW/2,166,"작물 분할 — 마스크 1개",23,"#FFFFFF","800","middle")
txt(RX+RW/2,186,"분할은 한 번, 용도는 두 개",15,"#9CA3AF","400","middle")

# 분할 → 축 A (영역 정의)
path(f"M{RX},163 H668 V{214+94} H{AX+AW+8}",A,2.8,"ta")
txt(714,186,"영역 정의",16,A,"800","middle")
# 분할 → 축 B (누끼)
arrow(1160,194,224,B,2.8,"ga")
txt(1178,216,"누끼",16,B,"800")

# 축 B
rect(RX,228,RW,192,BB,B)
o.append(f'<path d="M{RX},{228+10} a10,10 0 0 1 10,-10 h{RW-20} a10,10 0 0 1 10,10 v34 h-{RW} z" fill="{B}"/>')
txt(RX+22,262,"축 B · 농업 정합성",25,"#FFFFFF","800")
for i,(c,n) in enumerate([("B1","잎맥 위상 구조"),("B2","시설 구조물 직선·주기성"),("B3","병징·생육 정합")]):
    yy=302+i*34
    txt(RX+22,yy,c,21,B,"800"); txt(RX+68,yy,n,21,INK,"700")
txt(RX+22,402,"실제 이미지만으로 학습 → 미지 생성 모델과 무관 · 재압축에 강함",15,SUB)

# 수렴
o.append(f'<path d="M334,420 V442 M1056,420 V442 M334,442 H1056" fill="none" stroke="{LINE}" stroke-width="2.6"/>')
arrow(CC,442,466)

# 가중합
rect(CC-300,468,600,62,NB,NL)
txt(CC,498,"가 중 합",24,INK,"800","middle")
txt(CC,520,"가중치는 Leave-One-Generator-Out 교차검증으로 결정",15,SUB,"400","middle")
arrow(CC,530,554)

# 판정
rect(CC-190,556,380,54,"#111827","#111827",rx=27)
txt(CC,591,"임계값 → 실제 / 생성 판정",23,"#FFFFFF","700","middle")
o.append('</svg>')
open("docs/assets/architecture_simple.svg","w",encoding="utf-8").write("\n".join(o))
print("SVG",W,H)
