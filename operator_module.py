import re
import decimal
from decimal import Decimal
from abc import ABC, abstractmethod

# 소수점 정밀도 설정
decimal.getcontext().prec = 30

# 들어오는 문자열이 숫자인지 확인 (유효성 검사. 확장성을 위해 사용)
def is_number(s):
    try:
        Decimal(s)
        return True
    except (decimal.InvalidOperation, ValueError):
        return False

# 인터페이스로 쓰이는 추상클래스(규칙 정의서) : 모든 연산(+,-,×,/)이 가져야할 공통규칙을 선언
class OperatorStrategy(ABC):
    @abstractmethod      # 반드시 자식클래스에서 이 메서드를 구현해야한다는 데코레이터
    # 두 숫자를 받아서 계산한다.
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        pass 
    
    @property            # 함수를 속성처럼 읽게 해주는 데코레이터(괄호 없이 접근 가능)
    @abstractmethod 
    # 연산자 기호
    def symbol(self) -> str:
        pass
    
    @property
    @abstractmethod
    # 연산자의 우선순위 (높을수록 먼저 계산됨)
    def precedence(self) -> int:
        pass 

# 추상클래스를 상속하여 연산자를 간단히 생성하는 매서드(이구조는 새로운 연산자 추가도 가능함 (^, %, √))
def create_operator_strategy(execute_func, symbol_val, precedence_val):
    class CustomOperatorStrategy(OperatorStrategy):   # 함수 안에 써서 캡슐화
        def execute(self, a: Decimal, b: Decimal) -> Decimal:
            return execute_func(a, b)
        
        @property
        def symbol(self) -> str:
            return symbol_val
        
        @property
        def precedence(self) -> int:
            return precedence_val
    
    return CustomOperatorStrategy()

# 팩토리 패턴 : 연산자 한번 생성하면 재사용
class OperatorFactory:
    # 나누기 (number / 0) 에러방지
    @staticmethod
    def _safe_div(a: Decimal, b: Decimal) -> Decimal:
        if b == 0:
            raise decimal.DivisionByZero
        return a / b
    
    # 중앙에서 관리하는 연산자 정의
    _strategies = {
        '+': create_operator_strategy(lambda a, b: a + b, '+', 1),
        '-': create_operator_strategy(lambda a, b: a - b, '-', 1),
        '×': create_operator_strategy(lambda a, b: a * b, '×', 2),
        '/': create_operator_strategy(_safe_div, '/', 2),
        '%': create_operator_strategy(lambda a, b: a % b, '%', 2),
    }
    
    # 우선순위 기준으로 연산자 그룹화
    _priority_groups = {
        1: ['+', '-'],        # 낮은 우선순위 연산자
        2: ['×', '/', '%']    # 높은 우선순위 연산자
    }
    
    @staticmethod
    def create_operator(symbol: str) -> OperatorStrategy:
        return OperatorFactory._strategies.get(symbol)
    
    @staticmethod
    def get_all_operator_symbols():
        # 모든 지원되는 연산자 기호를 문자열로 반환
        return ''.join(OperatorFactory._strategies.keys())
    
    @staticmethod
    def get_priority_group(priority: int):
        # 특정 우선순위에 해당하는 연산자 그룹 반환
        return ''.join(OperatorFactory._priority_groups.get(priority, []))
    
    @staticmethod
    def is_operator(symbol: str) -> bool:
        # 주어진 기호가 지원되는 연산자인지 확인
        return symbol in OperatorFactory._strategies

# 정규식으로 숫자와 연산자를 토큰화하는 클래스
class Tokenizer:
    def __init__(self, operator_factory):
        self.operator_factory = operator_factory
        # 연산자 기호들을 정규식에 안전하게 포함시키기 위해 이스케이프 처리
        escaped_operators = ''.join([re.escape(op) for op in operator_factory.get_all_operator_symbols()])
        self._pattern = re.compile(r'-?\d+\.?\d*|[' + escaped_operators + ']')

    def tokenize(self, expression: str) -> list[str]:
        tokens = []
        i = 0
        
        # 정규식으로 먼저 토큰을 추출
        raw_tokens = self._pattern.findall(expression)
        
        while i < len(raw_tokens):
            token = raw_tokens[i]
            
            # 음수와 빼기 연산자 구분
            if token == '-':
                # 첫 번째 토큰이거나 이전 토큰이 연산자인 경우
                if i == 0 or self.operator_factory.is_operator(raw_tokens[i-1]):
                    # 다음 토큰이 숫자인 경우, 음수로 처리
                    if i+1 < len(raw_tokens) and is_number(raw_tokens[i+1]):
                        # 음수 처리: 다음 토큰과 결합
                        tokens.append('-' + raw_tokens[i+1])
                        i += 2
                        continue
                # 그 외의 경우는 빼기 연산자로 처리
                tokens.append(token)
            # 숫자가 음수로 시작하는 경우
            elif token.startswith('-') and is_number(token) and not (i > 0 and is_number(raw_tokens[i-1])):
                # 첫 번째 토큰이거나 이전 토큰이 연산자인 경우 음수로 처리
                tokens.append(token)
            # 숫자가 '-'로 시작하지만 이전 토큰이 숫자인 경우 (빼기 연산)
            elif token.startswith('-') and is_number(token) and i > 0 and is_number(raw_tokens[i-1]):
                tokens.append('-')  # 빼기 연산자
                tokens.append(token[1:])  # 양수
            else:
                tokens.append(token)
            i += 1
            
        # 곱셈 및 나눗셈 등 높은 우선순위 연산자 뒤에 음수 처리
        # 수정: 높은 우선순위 연산자 그룹을 사용
        processed_tokens = []
        high_priority_ops = self.operator_factory.get_priority_group(2)  # '×/%'
        i = 0
        while i < len(tokens):
            tok = tokens[i]
            if i < len(tokens) - 1 and tok in high_priority_ops and tokens[i+1].startswith('-'):
                processed_tokens.append(tok)
                processed_tokens.append(tokens[i+1])
                i += 2
            else:
                processed_tokens.append(tok)
                i += 1
    
        return processed_tokens

# 파서 클래스
class Parser:
    def parse(self, tokens: list[str], precedence: dict[str, int]) -> list[str]:
        output, stack = [], []
        for tok in tokens:
            if is_number(tok):
                output.append(tok)
            elif tok in precedence:
                while stack and stack[-1] in precedence and precedence[stack[-1]] >= precedence[tok]:
                    output.append(stack.pop())
                stack.append(tok)
        while stack:
            output.append(stack.pop())
        return output