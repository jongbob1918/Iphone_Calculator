https://docs.google.com/presentation/d/1dImJsHzd4QwMWpMc3vhF3w50E9WGPHR4emFxLQAeuMI/edit?usp=sharing

# 프로젝트 : PyQt6를 활용하여 Iphone 계산기 구현 

## 1. 프로젝트 목표
- *사용자 UX를 위한 GUI 설계** : 실제 전자계산기와 동일한 입력 흐름(괄호·음수·우선순위·오류 메시지) 구현으로 *입력 오류 0 %* 달성  
- **디자인패턴 학습** : **State / Strategy / Factory** 패턴 통합 적용으로 기능 확장·유지보수 난이도 최소화  
- **정밀 계산** : Shunting-Yard(중위→후위) + `decimal.Decimal` 스택 평가로 부동소수점 오차 제거  
- **테스트 주도 개발** : 정상·예외 흐름 45 개 시나리오 전부 통과(성공률 100 %)

---

## 2. 실행 방법
```bash
# 1) 저장소 클론
git clone https://github.com/<your-id>/qt-calculator.git
cd qt-calculator

# 2) 의존성 설치
pip install -r requirements.txt   # PyQt6 포함

# 3) 실행
python main.py
Windows 사용자는 python -m venv venv 로 가상환경을 권장합니다.

3. 주요 기능
ID	분류	기능 요약	핵심 UX 규칙
SR-1	필수	숫자 입력	다자리·선행 0 제거, 20자리 제한
SR-2	추가	소수점 처리	중복 입력 차단, 선행 0. 자동 보정
SR-3	추가	음수 처리	± 부호 전환, 연산자 뒤 - → 음수 인식
SR-4	필수	사칙연산	+ − × ÷, 우선순위·연속 계산
SR-5	추가	나머지 연산	%, 곱/나눗셈과 동일 우선순위
SR-6	필수	결과 출력	= 버튼, 0 나누기 등 오류 메시지 표시
SR-7	추가	듀얼 디스플레이	상단: 입력식, 하단: 현재값/결과
SR-8	필수	삭제·초기화	Backspace 1단계 삭제, AC 전체 리셋
SR-9	추가	상태 기반 흐름	READY / INPUT / RESULT / ERROR 전이 제어

4. 설계
4-1. 컴포넌트 & 클래스 다이어그램
컴포넌트 다이어그램 : main.py → ui_module.py → calculator_module.py → {operator,state}_module.py 의존 관계를 시각화

클래스 다이어그램 : Calculator, OperatorStrategy 파생, CalculatorState 파생 관계로 객체 책임·패턴 적용 위치 명확화

실제 이미지는 doc/component_diagram.png, doc/class_diagram.png 참고

4-2. 설계 패턴 적용
패턴	적용 이유	대표 클래스
State	입력 단계별 허용 동작 분리·예외 방어	ReadyState, InputState
Strategy	연산 알고리즘 캡슐화·교체 용이	AddStrategy, DivStrategy
Factory	연산자 객체 중앙 생성·재사용	OperatorFactory

4-3. GUI 인터페이스 설계
PyQt6 듀얼 디스플레이(상단 수식·하단 결과)

숫자·연산자·괄호·소수점·±·AC·Backspace 총 26 버튼

하단 토스트 영역에 실시간 오류/안내 메시지 표시

터치 환경 고려: 버튼 크기·간격 최적화

5. 테스트 케이스 개요
카테고리	케이스 수	예시
기본 입력	9	12345 입력 → 12345 표시
오류 복구	9	0 나누기 후 숫자 입력 → 자동 초기화
계산 흐름	9	5+3= → 이어서 ×2=
괄호·우선순위	8	5+3×2= → 11
에러 처리	6	연산자 중복 입력 시 한 개만 남김
초기화	4	AC → 화면 0
합계	45	성공률 100 %

모든 테스트는 pytest 자동화 스크립트(tests/)로 실행됩니다.

6. 맺음말
본 프로젝트는 UX 기반 설계와 State / Strategy / Factory 패턴 학습을 겸한 데모입니다.
더 깊이 있는 코드 리뷰나 AI 코딩 팁이 필요하다면 언제든 문의 주세요!

7. 작성자
항목	내용
이름	김종명 (Kim Jong-Myeong)
GitHub	<your-github-id>
Email	(작성 예정)
