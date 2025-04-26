from abc import ABC, abstractmethod

### 상태 관리 모듈
# 상태 패턴: 계산기 상태 인터페이스 및 공통 메서드
class CalculatorState(ABC):
        
    # 추상매서드로 사용(구현 강제하도록 설정, 상태마다 함수설정을 다르게 하기위해서)
    @abstractmethod
    def input_number(self, calculator, number: str): pass
    @abstractmethod
    def input_operator(self, calculator, operator: str): pass
    @abstractmethod
    def input_decimal(self, calculator): pass

    # 백스페이스 처리
    def backspace_common(self, calculator, always_reset=False):
        #눌렀을때 하나만있었거나 아무것도없다면 리셋
        if always_reset or len(calculator.display) <= 1:
            calculator.reset()
        else:
            calculator.display = calculator.display[:-1]
            calculator.expression = calculator.expression[:-1]
            calculator.update_state_after_backspace()

        return calculator.display, calculator.history_display

    # 상태마다 공통으로  수행이 많은 함수는 기본으로 설정하고 오버라이딩으로 씀.
    def input_backspace(self, calculator): 
        return self.backspace_common(calculator)
    def input_clear(self, calculator):
        calculator.reset()
        return calculator.display, calculator.history_display
    def input_equals(self, calculator):
        return calculator.display, calculator.history_display


## 상태 구현 클래스들 : 이전 입력상태에 따른 입력 예외처리 
# 초기상태일때 입력값들 예외처리
class InitialState(CalculatorState):

    def input_number(self, calc, number):
        calc.display = number
        calc.expression = number
        calc.set_state('NumberState')
        return calc.display, calc.history_display

    def input_operator(self, calc, operator):
        if operator == '-':
            calc.display = '-'
            calc.expression = '-'
            calc.set_state('NumberState')
        else:
            calc.display = '0' + operator
            calc.expression = '0' + operator
            calc.set_state('OperatorState')
        return calc.display, calc.history_display

    def input_decimal(self, calc):
        calc.display = '0.'
        calc.expression = '0.'
        calc.set_state('DecimalState')
        return calc.display, calc.history_display
    
# 숫자입력상태일때 입력값들 예외처리
class NumberState(CalculatorState):

    def input_number(self, calc, number):
        current = calc.get_current_number()
        if (current in ('0','-0') and number=='0'):
            return calc.display, calc.history_display
        
        if calc.display == '-' and calc.expression == '-':
            calc.display += number
            calc.expression += number
            return calc.display, calc.history_display
        
        if current in ('0','-0') and number!='0':
            calc.display = calc.display[:-1] + number
            calc.expression = calc.expression[:-1] + number
        else:
            calc.display += number
            calc.expression += number
        return calc.display, calc.history_display

    def input_operator(self, calc, operator):
        if calc.display=='-' and calc.expression=='-':
            calc.display = '0'+operator
            calc.expression = '0'+operator
        else:
            calc.display += operator
            calc.expression += operator
        calc.set_state('OperatorState')
        return calc.display, calc.history_display

    def input_decimal(self, calc):
        calc.display += '.'
        calc.expression += '.'
        calc.set_state('DecimalState')
        return calc.display, calc.history_display

    def input_equals(self, calc):
        return calc.calculate_and_update()
    

# 소수점입력상태일때 입력값들 예외처리
class DecimalState(CalculatorState):
    def input_number(self, calc, number):
        calc.display += number
        calc.expression += number
        return calc.display, calc.history_display

    def input_operator(self, calc, operator):
        calc.display += operator
        calc.expression += operator
        calc.set_state('OperatorState')
        return calc.display, calc.history_display

    def input_decimal(self, calc):
        return calc.display, calc.history_display

    def input_equals(self, calc):
        return calc.calculate_and_update()
    

# 연산자입력상태일때 입력값들 예외처리
class OperatorState(CalculatorState):

    def input_number(self, calc, number):
        calc.display += number
        calc.expression += number
        calc.set_state('NumberState')
        return calc.display, calc.history_display

    def input_operator(self, calc, operator):
        # 마지막 문자 확인
        last = calc.display[-1]
        # 같은 연산자가 연속으로 입력되면 무시
        if last == operator:
            return calc.display, calc.history_display
        # 마지막에서 두 번째 문자 확인 (필요시)
        second_last = calc.display[-2] if len(calc.display) > 1 else ''
        # 모든 연산자 기호 가져오기
        all_operators = calc.operator_factory.get_all_operator_symbols()
        # 곱셈 나눗셈 연산자들
        high_precedence_operators = ''.join([op for op in all_operators 
                                             if calc.operator_factory.create_operator(op).precedence > 1])
    
        # '-' 연산자 특수 처리
        if operator == '-' and last in high_precedence_operators:
            # 이미 음수 처리된 경우는 처리하지 않음
            calc.display += operator
            calc.expression += operator
        # 마지막 문자가 '-'이면서 마지막에서 두 번째 문자가 곱셈/나눗셈/나머지연산인 경우
        elif last == '-' and second_last in high_precedence_operators:

            # 음수 취소: 이전 문자(-) 및 전전문자(×/%) 삭제 후 새 연산자 입력
            calc.display = calc.display[:-2] + operator
            calc.expression = calc.expression[:-2] + operator
        else:
            # 나머지 경우: 이전 연산자 대체
            calc.display = calc.display[:-1] + operator
            calc.expression = calc.expression[:-1] + operator
        return calc.display, calc.history_display
    
    # 연산자 다음 소수점 입력시 0.으로 입력
    def input_decimal(self, calc):
        calc.display += '0.'
        calc.expression += '0.'
        calc.set_state('DecimalState')
        return calc.display, calc.history_display

    # 연산 시 마지막에 연산자있으면 삭제
    def input_equals(self, calc):
        all_operators = calc.operator_factory.get_all_operator_symbols()
        if calc.expression and calc.expression[-1] in all_operators:
            calc.expression = calc.expression[:-1]
            calc.display = calc.display[:-1]
        return calc.calculate_and_update()
    

# 결과상태일때 입력값들 예외처리
class ResultState(CalculatorState):

    def input_number(self, calc, number):
        calc.display = number
        calc.expression = number
        calc.history_display = ''
        calc.set_state('NumberState')
        return calc.display, calc.history_display

    def input_operator(self, calc, operator):
        calc.display += operator
        calc.expression = calc.display
        calc.history_display = ''
        calc.set_state('OperatorState')
        return calc.display, calc.history_display

    def input_decimal(self, calc):
        calc.display = '0.'
        calc.expression = '0.'
        calc.history_display = ''
        calc.set_state('DecimalState')
        return calc.display, calc.history_display

    def input_backspace(self, calc):
        return self.backspace_common(calc, always_reset = True)

# 에러상태일때 입력값들 예외처리
class ErrorState(CalculatorState):
    
    #숫자나 소수점 누르면 초기상태처럼 입력될수있게 처리
    def _reset_and_delegate(self, calc, input_method, *args):
        calc.reset()
        calc.set_state('InitialState')
        method = getattr(calc.state, input_method)
        return method(calc, *args) if args else method(calc)
    
    def input_number(self, calc, number):
        return self._reset_and_delegate(calc, 'input_number', number)
        
    def input_decimal(self, calc):
        return self._reset_and_delegate(calc, 'input_decimal')
    
    # 인식안되게 
    def input_operator(self, calc, operator): 
        return calc.display, calc.history_display
    
    # 백스페이스 누르면 초기화
    def input_backspace(self, calc): 
        return self.backspace_common(calc, always_reset = True)