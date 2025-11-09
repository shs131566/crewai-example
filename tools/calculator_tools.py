import ast
import operator
import re
from crewai.tools import tool


@tool("수학 표현식 계산")
def calculate(operation: str) -> str:
    """덧셈, 뺄셈, 곱셈, 나눗셈 등 모든 수학 계산을 수행하는 데 유용합니다.
    이 도구에 대한 입력은 수학적 표현식이어야 하며,
    예를 들어 `200*7` 또는 `5000/2*10`과 같습니다
    """
    try:
        # Define allowed operators for safe evaluation
        allowed_operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
            ast.Mod: operator.mod,
            ast.USub: operator.neg,
            ast.UAdd: operator.pos,
        }

        # Parse and validate the expression
        if not re.match(r'^[0-9+\-*/().% ]+$', operation):
            return "오류: 수학 표현식에 잘못된 문자가 있습니다"

        # Parse the expression
        tree = ast.parse(operation, mode='eval')

        def _eval_node(node):
            if isinstance(node, ast.Expression):
                return _eval_node(node.body)
            elif isinstance(node, ast.Constant):  # Python 3.8+
                return node.value
            elif isinstance(node, ast.Num):  # Python < 3.8
                return node.n
            elif isinstance(node, ast.BinOp):
                left = _eval_node(node.left)
                right = _eval_node(node.right)
                op = allowed_operators.get(type(node.op))
                if op is None:
                    raise ValueError(f"지원되지 않는 연산자: {type(node.op).__name__}")
                return op(left, right)
            elif isinstance(node, ast.UnaryOp):
                operand = _eval_node(node.operand)
                op = allowed_operators.get(type(node.op))
                if op is None:
                    raise ValueError(f"지원되지 않는 연산자: {type(node.op).__name__}")
                return op(operand)
            else:
                raise ValueError(f"지원되지 않는 노드 유형: {type(node).__name__}")

        result = _eval_node(tree)
        return str(result)

    except (SyntaxError, ValueError, ZeroDivisionError, TypeError) as e:
        return f"오류: {str(e)}"
    except Exception as e:
        return "오류: 잘못된 수학 표현식입니다"


class CalculatorTools():
    calculate = calculate
