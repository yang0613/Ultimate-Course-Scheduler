#!/usr/bin/python3
from AST import PrereqAlgebra
from constraint import Constraint
from constraint_types import generate_prereq_func, not_avaliable_during

algebra = PrereqAlgebra()

class requirement:
    """A class designed to verify if the courses in your schedule meet
    certain requirements. 

    All "requirements" such as getting ready to graduate or to declare
    your major can be expressed as a series of boolean expressions. That
    is, as long as you would need to check your schedule to receive a
    boolean answer (Am I ready to graduate? Yes or No?) this output can
    be expanded as an a boolean function where the inputs are the 
    classes themselves.

    Our implementation allows anyone with basic boolean and bracket 
    balancing skills to easily create any requirement for any classes
    as a boolean expression string, and the class will automatically
    solve and find the remaining classes needed to satisfy your
    requirement. Additionally, there are other phrases where it is 
    possible to even verify whether your schedule has enough classes
    for a certain "category" by X date. This is done by expanding on
    an existing boolean parser library with evaluation and string 
    support, and functionally resolving our special phrases before it 
    even reaches the parser, allowing us to functionally process our 
    input without having to develop a seperate parser for this 
    exclusive language from scratch.

    Examples:

    "MATH 19A or MATH 19B; CSE 101; and three from: "Fun Classes" 
    discounting one from: CSE 115A or ECON 104 discounting one from: 
    "Boring Classes" by quarter 5 and one from: CSE 13S, or CSE 30 by
    quarter 3".

    Meaning that the schedule must have 3 classes belonging to 
    "Fun Classes", but only one will count from either CSE-115A and
    ECON-104, and only one will also count towards that same total 
    belonging to "Boring Classes", all needing to be done by quarter 5. 
    Additionally, 1 class from CSE-13S or CSE-30 will be required by 
    quarter 3, CSE-101 will be required as well as MATH-19A or MATH-19B.
    """
    def __init__(self, expr=''):
        self.expr = expr
        self.ast = algebra.parse(expr).simplify()
        self.constraint = Constraint([generate_prereq_func(), not_avaliable_during])


    def validate(self, schedule):
        """Verfies the schedule to see if it satsifies the requirements
        set by expr. If all the requirements are sastified, return "1" 
        or True. Otherwise, return the missing requirements as a 
        boolean expression.

        Args:
            schedule (dict): JSON Object holding our Schedule

        Returns:
            A subset of our schedule where each class is key limited
            by a list of failed requirements
        """
        return self.constraint.validate(schedule)