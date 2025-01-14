from pyiron_workflow import as_function_node, as_macro_node, as_dataclass_node
from typing import Optional

@as_function_node("sum")
def Addition(variable1:Optional[int|float], variable2:Optional[int|float]) -> int|float:
    sum_ = variable1 + variable2
    return sum_

@as_function_node("difference")
def Subtraction(variable1, variable2:Optional[int|float]) -> int|float:
    diff = variable1 - variable2
    return diff

@as_function_node("product")
def Multiplication(variable1, variable2:Optional[int|float]) -> int|float:
    prod = variable1 * variable2
    return prod

@as_function_node("quotient")
def Division(variable1, variable2:Optional[int|float]) -> int|float:
    qnt = variable1 / variable2
    return qnt