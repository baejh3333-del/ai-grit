# -*- coding: utf-8 -*-
"""수행계획서 인쇄용 간략 도식. python3 docs/assets/gen_architecture_simple.py"""
W,H = 1400, 838
F = "NanumGothic, 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif"
INK="#111827"; SUB="#4B5563"; LINE="#6B7280"
A="#0F766E"; AB="#F0FDFA"; B="#15803D"; BB="#F0FDF4"; NB="#F9FAFB"; NL="#9CA3AF"
o=[]
def esc(t): return t.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
def rect(x,y,w,h,fill,stroke,rx=10,sw=2.2):
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
def txt(x,y,t,size=17,fill=INK,weight="400",anchor="start"):
    o.append(f'<text x="{x}" y="{y}" font-family="{F}" font-size="{size}" fill="{fill}" '
             f'font-weight="{weight}" text-anchor="{anchor}">{esc(t)}</text>')
def path(d,col=LINE,sw=2.4,mk="a"):
    o.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{sw}" marker-end="url(#{mk})"/>')

o.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
o.append('<defs>'
 f'<marker id="a" markerWidth="10" markerHeight="10" refX="5" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{LINE}"/></marker>'
 f'<marker id="ga" markerWidth="10" markerHeight="10" refX="5" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{B}"/></marker>'
 f'<marker id="ta" markerWidth="10" markerHeight="10" refX="5" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{A}"/></marker>'
 '</defs>')
o.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="#FFFFFF"/>')

# 입력
rect(350,36,700,58,NB,NL)
txt(700,72,"입력 이미지  —  원본 해상도 유지 (리사이즈 금지)",20,INK,"700","middle")
path("M700,94 V128 M340,128 H1050 M340,128 V166",LINE)
o.append(f'<line x1="1050" y1="128" x2="1050" y2="160" stroke="{LINE}" stroke-width="2.4" marker-end="url(#a)"/>')
o.append(f'<line x1="340" y1="128" x2="340" y2="160" stroke="{LINE}" stroke-width="2.4" marker-end="url(#a)"/>')

# 축 A
rect(60,168,560,300,AB,A)
o.append(f'<rect x="60" y="168" width="560" height="46" rx="10" fill="{A}"/>')
o.append(f'<rect x="60" y="196" width="560" height="18" fill="{A}"/>')
txt(84,200,"축 A · 생성 흔적",23,"#FFFFFF","800")
txt(596,200,"원본 전체를 본다",14,"#CCFBF1","400","end")
for i,(c,n,d) in enumerate([("A1","VAE 재구성 오차","확산 · 플로우매칭 · 증류"),
                            ("A2","주파수 이상","GAN"),
                            ("A4","마스크 안팎 대조","합성 유형 ①②"),
                            ("A5","전역 분류기","전 유형 안전망")]):
    y=254+i*54
    txt(84,y,c,19,A,"800"); txt(128,y,n,19,INK,"700"); txt(360,y,d,15,SUB)

# 작물 분할
rect(760,168,580,78,"#111827","#111827")
txt(1050,200,"작물 분할  —  마스크 1개",21,"#FFFFFF","800","middle")
txt(1050,224,"분할은 한 번, 용도는 두 개",14,"#9CA3AF","400","middle")

# 분할 → 축 A (영역 정의) — 축 B를 피해 바깥으로 우회
path("M760,207 H680 V362 H628",A,2.6,"ta")
txt(720,197,"영역 정의",15,A,"800","middle")
# 분할 → 축 B (누끼)
o.append(f'<line x1="1160" y1="246" x2="1160" y2="302" stroke="{B}" stroke-width="2.6" marker-end="url(#ga)"/>')
txt(1176,282,"누끼",16,B,"800")

# 축 B
rect(760,310,580,240,BB,B)
o.append(f'<rect x="760" y="310" width="580" height="46" rx="10" fill="{B}"/>')
o.append(f'<rect x="760" y="338" width="580" height="18" fill="{B}"/>')
txt(784,342,"축 B · 농업 정합성",23,"#FFFFFF","800")
for i,(c,n) in enumerate([("B1","잎맥 위상 구조"),("B2","시설 구조물 직선·주기성"),("B3","병징·생육 정합")]):
    y=396+i*44
    txt(784,y,c,19,B,"800"); txt(828,y,n,19,INK,"700")
txt(784,532,"실제 이미지만으로 학습  →  미지 생성 모델과 무관 · 재압축에 강함",14,SUB)

# 수렴
o.append(f'<path d="M340,468 V596 M1050,550 V596 M340,596 H1050" fill="none" stroke="{LINE}" stroke-width="2.4"/>')
o.append(f'<line x1="695" y1="596" x2="695" y2="626" stroke="{LINE}" stroke-width="2.4" marker-end="url(#a)"/>')

# 가중합
rect(425,634,540,66,NB,NL)
txt(695,662,"가 중 합",22,INK,"800","middle")
txt(695,686,"가중치는 Leave-One-Generator-Out 교차검증으로 결정",14,SUB,"400","middle")
o.append(f'<line x1="695" y1="700" x2="695" y2="730" stroke="{LINE}" stroke-width="2.4" marker-end="url(#a)"/>')

# 판정
rect(505,738,380,58,"#111827","#111827",rx=29)
txt(695,775,"임계값  →  실제 / 생성 판정",21,"#FFFFFF","700","middle")
o.append('</svg>')
open("docs/assets/architecture_simple.svg","w",encoding="utf-8").write("\n".join(o))
print("simple SVG written",W,H)
