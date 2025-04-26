from PyQt6 import uic
from PyQt6.QtWidgets import QApplication,  QDialog
from functools import partial
from state_module import CalculatorState
from calculator_module import Calculator
import os

script_dir = os.path.dirname(os.path.abspath(__file__))  # 현재 스크립트 위치
from_class = uic.loadUiType(os.path.join(script_dir, "Calculator.ui"))[0]

# 사용자 인터페이스 모듈
# PyQt6 관련 코드와 이벤트 관리
# 계산기 입력 UI 클래스
class CalculatorApp(QDialog, from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('계산기')
        self.calc = Calculator()
        self.connect_buttons()
        self.lineEdit.setText('0')
        self.lineEdit_2.setText('')

    # 어떤 버튼이 눌렀는지 
    def connect_buttons(self):
        for i in range(10): 
            getattr(self, f'button_{i}').clicked.connect(lambda _, x=str(i): self.process_calculator_input('number', x))

        ops = {'plus':'+','minus':'-','multiply':'×','divide':'/', 'modulo': '%'}
        for name, sym in ops.items():
            getattr(self, f'button_{name}').clicked.connect(lambda _, s=sym: self.process_calculator_input('operator', s))


        self.button_decimal.clicked.connect(partial(self.process_calculator_input, 'decimal'))
        self.button_result.clicked.connect(partial(self.process_calculator_input, 'equals'))
        self.button_allclear.clicked.connect(partial(self.process_calculator_input, 'clear'))
        self.button_back.clicked.connect(partial(self.process_calculator_input, 'backspace'))

    # 중간 연결함수 : 계산기 클래스랑 연결하는 함수, 결합도 최소화
    def process_calculator_input(self, action, value=None):
        handler = {
            'number'    : lambda v: self.calc.input_number(v),
            'operator'  : lambda v: self.calc.input_operator(v),
            'decimal'   : lambda _: self.calc.input_decimal(),
            'equals'    : lambda _: self.calc.input_equals(),
            'clear'     : lambda _: self.calc.input_clear(),
            'backspace' : lambda _: self.calc.input_backspace(),
        }.get(action)

        if handler:
            self.update_display(*handler(value)) # handler값을 여러개 받는이유 : 연산 결과값 받을때 수식값도 같이 시현
    
    #결과 값 시현 
    def update_display(self, display, history):
        self.lineEdit.setText(display)
        self.lineEdit_2.setText(history or '')