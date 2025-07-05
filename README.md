# 📱 PyQt6 계산기 프로젝트
사용경험을 고려한 GUI Interface와 디자인 패턴을 도입하여 유지보수성과 확장성을 중심으로 구현하였습니다.
## 0. 발표자료
[PPT 슬라이드 바로가기](https://docs.google.com/presentation/d/1dImJsHzd4QwMWpMc3vhF3w50E9WGPHR4emFxLQAeuMI/edit?usp=sharing)

---

## 1. 프로젝트 목표
i
1. **UX-기반 GUI**   
   괄호·음수·우선순위·오류 알림까지 “실제 전자계산기”와 동일한 입력 경험을 구현
2. **디자인 패턴 실습**   
   **State / Strategy / Factory** 패턴을 통합 적용해 기능 확장과 유지보수 난이도를 최소화합니다.  
3. **정밀 계산**   
   Shunting-Yard(중위→후위) 알고리즘과 `decimal.Decimal` 스택 평가로 부동소수점 오차를 제거합니다.  
4. **TDD 기반 품질 확보**   
   정상·예외 흐름 45 개 시나리오를 `pytest`로 자동화해 **100 %** 성공을 목표로 합니다.  

---

## 2. 실행 방법
```bash
# 1) 저장소 클론
git clone https://github.com/<your-id>/qt-calculator.git
cd qt-calculator

# 2) 의존성 설치
pip install -r requirements.txt     # PyQt6 포함

# 3) 실행
python main.py
Windows 사용자는 python -m venv venv로 가상환경을 권장합니다.

3. 주요 기능
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

4. 설계
4-1. 컴포넌트 & 클래스 다이어그램
컴포넌트 다이어그램 : main.py → ui_module.py → calculator_module.py → {operator,state}_module.py 의존 관계를 시각화합니다.

클래스 다이어그램 : Calculator, OperatorStrategy 파생, CalculatorState 파생 관계로 객체 책임과 패턴 적용 지점을 명확히 합니다.
이미지 파일 → doc/component_diagram.png, doc/class_diagram.png

4-2. 설계 패턴 적용
패턴	적용 이유	대표 클래스
State	입력 단계별 허용 동작 분리·예외 방어	ReadyState, InputState 등
Strategy	연산 알고리즘 캡슐화·교체 용이	AddStrategy, DivStrategy
Factory	연산자 객체 중앙 생성·재사용	OperatorFactory

4-3. GUI 인터페이스 설계
듀얼 디스플레이 (상단 수식 / 하단 결과)

26 개 버튼 : 숫자·연산자·괄호·소수점·±·AC·Backspace

토스트 메시지 : 하단에 실시간 오류·안내 출력

터치 최적화 : 버튼 크기·간격 조정

5. 테스트 케이스 개요
카테고리	케이스 수	예시
기본 입력	9	12345 입력 → 12345 표시
오류 복구	9	0 나누기 후 숫자 입력 → 자동 초기화
계산 흐름	9	5+3= → 이어서 ×2=
괄호·우선순위	8	5+3×2= → 11
에러 처리	6	연산자 중복 입력 시 한 개만 남김
초기화	4	AC → 화면 0
합계	45	성공률 100 %

모든 테스트는 pytest 스크립트(tests/)로 자동 실행될 예정입니다.

