import re
import decimal
from decimal import Decimal
from state_module import (InitialState, NumberState, DecimalState, OperatorState, ResultState, ErrorState)
from operator_module import OperatorFactory, Tokenizer, Parser, is_number

# 계산기 클래스
class Calculator:
    def __init__(self):
        self.display = '0'
        self.history_display = ''
        self.expression = ''

        # 전 입력문자에 따른 상태 
        self.state_instances = {
            'InitialState'  : InitialState(),
            'NumberState'   : NumberState(),
            'DecimalState'  : DecimalState(),
            'OperatorState' : OperatorState(),
            'ResultState'   : ResultState(),
            'ErrorState'    : ErrorState()
        }
        # 처음 인스턴스 생성시 초기상태로 설정
        self.state = self.state_instances['InitialState']

        # 각 클래스들의 인스턴스변수 생성.
        self.operator_factory = OperatorFactory()
        self.tokenizer = Tokenizer(self.operator_factory)
        self.parser = Parser()

    # 초기상태로 되돌리기
    def reset(self):
        self.display = '0'
        self.history_display = ''
        self.expression = ''
        self.set_state('InitialState')

    #상태가 존재하지 않으면 에러상태로 변경
    def set_state(self, name):
        self.state = self.state_instances.get(name, self.state_instances['ErrorState'])

    # 벡스페이스로 제거시 남아있는 마지막문자 상태를 가져옴.
    def update_state_after_backspace(self):
        if not self.display:
            self.reset()
            return
        last = self.display[-1]
        if last == '.': 
            self.set_state('DecimalState')
        elif last in self.operator_factory.get_all_operator_symbols(): 
            self.set_state('OperatorState')
        elif last.isdigit(): 
            self.set_state('NumberState')
        else: 
            self.reset()

    def get_current_number(self):
        # 연산자로 분리해서 마지막 숫자 부분 가져오기
        operators = self.operator_factory.get_all_operator_symbols()
        parts = re.split(r'[' + re.escape(operators) + ']', self.display)
        return parts[-1]
    
    # UI클래스에서 입력 받은 값들을 현재상태에 따라 상태클래스로 보냄
    def input_number(self, num): 
        return self.state.input_number(self, num)
    def input_operator(self, op): 
        return self.state.input_operator(self, op)
    def input_decimal(self): 
        return self.state.input_decimal(self)
    def input_backspace(self): 
        return self.state.input_backspace(self)
    def input_equals(self): 
        return self.state.input_equals(self)
    def input_clear(self): 
        return self.state.input_clear(self)
    
    def calculate_and_update(self):
        # 문자열 끝의 연산자 제거
        expr = self.expression
        operators = self.operator_factory.get_all_operator_symbols()
        
        # 표현식 끝에 연산자가 있다면 제거
        while expr and expr[-1] in operators:
            expr = expr[:-1]
            
        self.history_display = expr
        try:
            result = self.calculate(expr)
            self.display = self.format_decimal_result(result)
            self.expression = self.display
            self.set_state('ResultState')
        except decimal.DivisionByZero:
            self.display = 'ERROR: Division by zero'
            self.set_state('ErrorState')
        except Exception as e:
            print(f"계산 오류: {e}")  # 디버깅용 출력
            self.display = 'ERROR: Invalid expression'
            self.set_state('ErrorState')
        return self.display, self.history_display

    # 연산 함수
    def calculate(self, expr):
        # 연산자 우선순위를 OperatorFactory에서 가져오기
        precedence = {op: self.operator_factory.create_operator(op).precedence 
                     for op in self.operator_factory.get_all_operator_symbols()}
        
        tokens = self.tokenizer.tokenize(expr)
        print(f"토큰: {tokens}")  # 디버깅용 출력
        postfix = self.parser.parse(tokens, precedence)
        print(f"후위표기: {postfix}")  # 디버깅용 출력
        
        stack = []
        for tok in postfix:
            if is_number(tok): 
                stack.append(Decimal(tok))
            else:
                if len(stack) < 2:
                    raise ValueError(f"계산 스택에 충분한 값이 없습니다. 현재 스택: {stack}, 토큰: {tok}")
                b, a = stack.pop(), stack.pop()
                op = self.operator_factory.create_operator(tok)
                if op is None:
                    raise ValueError(f"인식할 수 없는 연산자: {tok}")
                stack.append(op.execute(a, b))
        
        if not stack:
            return Decimal('0')
        return stack[0]
    
    # 소수점 뒤에 0만있으면 소수점을 지워주는 함수
    def format_decimal_result(self, result):
        r = result.normalize()
        return str(int(r)) if r == int(r) else str(r)