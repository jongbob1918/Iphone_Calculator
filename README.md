# 📱 PyQt6 계산기 프로젝트
사용자경험(UX)을 고려하여 듀얼 디스플레이, 깔끔한 디자인으로 구현한 GUI 계산기입니다.</br> 
사용자 입력에 대한 다양한 예외처리와 상태, 팩토리, 전략패턴 같은 디자인 패턴을 도입하여 유지보수성과 확장성을 중심으로 구현하였습니다.
## 0. 발표자료
[PPT 슬라이드 바로가기](https://docs.google.com/presentation/d/1dImJsHzd4QwMWpMc3vhF3w50E9WGPHR4emFxLQAeuMI/edit?usp=sharing)

---

## 2. 실행 방법
```bash
# 1) 저장소 클론
git clone https://github.com/<your-id>/qt-calculator.git
cd qt-calculator

# 2) 의존성 설치
pip install -r requirements.txt

# 3) 실행
python main.py

```
---


## 3. 주요 기능

ID	분류	기능 요약	핵심 UX 규칙
SR-1	필수	숫자 입력	다자리·선행 0 제거, 20자리 제한
SR-2	추가	소수점 처리	중복 입력 차단, 선행 0. 자동 보정
SR-3	추가	음수 처리	± 부호 전환, 연산자 뒤 - → 음수 인식
SR-4	필수	사칙연산	+ − × ÷, 우선순위·연속 계산
SR-5	추가	나머지 연산	%, 곱·나눗셈과 동일 우선순위
SR-6	필수	결과 출력	= 버튼, 0 나누기 등 오류 메시지 표시
SR-7	추가	듀얼 디스플레이	상단: 입력식, 하단: 현재값/결과
SR-8	필수	삭제·초기화	Backspace 1단계 삭제, AC 전체 리셋
SR-9	추가	상태 기반 입력 흐름	READY / INPUT / RESULT / ERROR 전이 제어



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

