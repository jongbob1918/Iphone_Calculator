# 📱 PyQt6 계산기 프로젝트
사용자경험(UX)을 고려하여 듀얼 디스플레이, 깔끔한 디자인으로 구현한 GUI 계산기입니다.</br> 
사용자 입력에 대한 다양한 예외처리와 상태, 팩토리, 전략패턴 같은 디자인 패턴을 도입하여 유지보수성과 확장성을 중심으로 구현하였습니다.
## 발표자료
[PPT 슬라이드 바로가기](https://docs.google.com/presentation/d/1dImJsHzd4QwMWpMc3vhF3w50E9WGPHR4emFxLQAeuMI/edit?usp=sharing)

---
## 1. 폴더 구조 
```bash
kimjongmyung/
├── main.py                # 애플리케이션 시작점 · 전체 초기화 & 실행
├── ui_module.py           # PyQt6 기반 GUI 구현 · 사용자 입력 처리 & 결과 표시
├── calculator_module.py   # 핵심 계산 로직 · 상태 관리 & 연산 수행
├── operator_module.py     # 다양한 연산자 클래스 정의 · Strategy 패턴 연산 구현
├── Calculator.ui          # Qt Designer XML · 버튼·디스플레이 레이아웃 정의
└── state_module.py        # 계산기의 상태 클래스 정의 · State 패턴 동작 관리

```

---

## 2. 실행 방법
```bash
# 1) 저장소 클론
[git clone https://github.com/<your-id>/qt-calculator.gi](https://github.com/jongbob1918/PyQt6_Calculator.git)
cd kimjongmyung

# 2) 의존성 설치
pip install PyQt6

# 3) 실행
python main.py

```
---


## 3. 주요 기능

![image](https://github.com/user-attachments/assets/946138a8-93df-434e-b7b2-728de09a9c04)
![image](https://github.com/user-attachments/assets/a614f6a8-3f78-42db-a14c-2c15e102c692)




---

## 4. 설계
### 4-1. 컴포넌트 & 클래스 다이어그램
**클래스 다이어그램** : 
- 역할에 따라 모듈화하여 유지보수성을 고려하여 설계
  
![image](https://github.com/user-attachments/assets/5eb9e5ab-3fd4-4480-9955-e60edeb4be64)

---

**클래스 다이어그램** : 
- Calculator, OperatorStrategy 파생, CalculatorState 파생 관계로 객체 책임과 패턴 적용 지점을 하여 설계
![image](https://github.com/user-attachments/assets/ecc42a42-dff8-4375-8199-eb3acd32b697)


### 4-2. 설계 패턴 적용
  | 패턴 | 적용 이유 | 대표 클래스 |
  |------|------------------------|------------------------|
  | State | 입력 단계별 허용 동작 분리| ReadyState, InputState |
  | Strategy | 연산 알고리즘 캡슐화하여 교체 용이 | AddStrategy, DivStrategy |
  | Factory | 연산자 객체 중앙 생성하여 재사용 용이 | OperatorFactory |






## 5. 테스트 케이스
테스트 주도 개발을 적용하여 실제 계산기 수준의 예외처리로 구현 가능하였음
![image](https://github.com/user-attachments/assets/c547f4fb-2d66-4eed-8a5d-35facea851bf)

