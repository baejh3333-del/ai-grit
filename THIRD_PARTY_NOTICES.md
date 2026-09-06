# 외부 자산 고지

공고문 p.5·p.9는 외부 데이터·공개 사전학습 모델·생성형 AI 도구·자체 생성 데이터의 **출처, 이용 조건, 생성 방법, 활용 방법**을 최종 제출자료에 명시할 것을 요구한다. 사용하는 모든 자산을 아래 표에 즉시 기록한다.

## 사전학습 모델 / 코드

| 자산 | 버전 | 라이선스 | 출처 URL | 용도 | 가중치 제출 포함 |
|---|---|---|---|---|---|
| FerretNet | | Apache-2.0 | https://github.com/xigua7105/FerretNet | B0 분류 브랜치 | 예정 |
| SPAI | | Apache-2.0 (코드+가중치) | https://github.com/mever-team/spai | B2 스펙트럼 브랜치 | 예정 |
| CLIP ViT-L/14 | | MIT | https://github.com/openai/CLIP | B1 특징 추출 | 예정 |
| SAM 계열 | | Apache-2.0 | | B3 영역 분할 | 예정 |

> ⚠️ **재배포 불가 라이선스 자산은 등재하지 않는다.** p.5가 가중치 제출을 예외 없이 요구하므로, 재배포가 금지된 가중치는 사용 자체가 불가능하다. (예: TruFor / Noiseprint++ — GRIP-UNINA 독자 라이선스, Ultralytics YOLO — AGPL-3.0)

## 외부 데이터

| 데이터셋 | 버전/취득일 | 이용 조건 | 접근 경로 | 활용·전처리 방법 |
|---|---|---|---|---|
| AI Hub #534 지능형 스마트팜(토마토) | | 재배포 제한 | https://aihub.or.kr/aihubdata/data/view.do?dataSetSn=534 | Real 풀. 원본 재제출 불가 → p.5 갈음 예외 원용 |
| AI Hub #535 지능형 스마트팜(파프리카) | | 재배포 제한 | https://aihub.or.kr/aihubdata/data/view.do?dataSetSn=535 | 동일 |
| AI Hub #71523 지능형 스마트팜(오이·딸기) | | 재배포 제한 | https://aihub.or.kr/aihubdata/data/view.do?dataSetSn=71523 | 동일 |
| AI Hub #71451 시설작물(딸기) 개체·질병 | | 재배포 제한 | https://aihub.or.kr/aihubdata/data/view.do?dataSetSn=71451 | 동일 |
| PlantVillage | | | | 유형 ① "실험실 작물" 소스 |

## 자체 생성 데이터

| 유형 | 생성 도구 / 버전 | 도구 라이선스 | 생성 방법 (파라미터) | 수량 |
|---|---|---|---|---|
| ① 실험실 작물 + 현장 배경 | | | | |
| ② 현장 작물 + 다른 현장 배경 | | | | |
| ③ 스타일 변환 | | | | |
| ④ 전체 생성 | | | | |
