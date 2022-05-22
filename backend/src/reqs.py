#!/usr/bin/python3.9
import AST
import constraint
import constraint_types
import major_database

algebra = AST.algebra

class requirement:
    """A class designed to verify if the courses in your schedule meet
    certain requirements. 

    All "requirements" such as getting ready to graduate or to declare
    your major can be expressed as a series of boolean expressions. That
    is, as long as you would need to check your schedule to receive a
    boolean answer (Am I ready to graduate? Yes or No?) this output can
    be expanded as an a boolean function where the inputs are the 
    classes themselves.

    Our implementation allows anyone with basic boolean skills
    to easily create any requirement for any classes
    as a boolean expression string, and the class will automatically
    solve and find the remaining classes needed to satisfy your
    requirement. Additionally, there are other phrases where it is 
    possible to even verify whether your schedule has enough classes
    for a certain "category" by X date. This is done by equipping
    an existing boolean parser library with the capabilties to read
    and process a special language exclusively used to represent
    any sort of requirement. With the language now processed and 
    converted into an Abstract Syntax Tree (AST), the parser can now
    "trim the branches", so to speak, where each class in our schedule
    is a branch. The more classes we have in our schedule, the more 
    branches we can cut, and the more likely it is our requirements will
    be completely sastified. Therefore what is left of the tree must 
    represent whatever is remaining/missing to sastify our requirement, 
    or to "fully cut down the tree". 

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
    def __init__(self, major=''):
        self.major = major
        major_boolean_expr = major_database.MAJOR_MATCH_EXPRESSION[major]
        self.ast = algebra.parse(major_boolean_expr).simplify()
        self.constraint = constraint.Constraint([constraint_types.generate_prereq_func(), 
                                                constraint_types.not_avaliable_during])


    def validate(self, schedule):
        """Validates the schedule to see if there are any errors
        for each class. If all the requirements are sastified, return
        an empty requirements.

        Args:
            schedule (dict): JSON Object holding our Schedule

        Returns:
            A subset of our schedule where each class is key limited
            by a list of failed requirements
        """
        return self.constraint.validate(schedule)

    def verify_major(self, schedule):
        """Verfies the schedule to see if the schedule meets the major
        requirement. If all the requirements are sastified, return
        an empty list.
        Args:
            schedule (dict): JSON Object holding our Schedule

        Returns:
            A list of requirements that is required to fulfill
            the major requirements
        """
        process_ast = AST.convert_schedule(schedule)
        major_req = self.ast.subs(process_ast).simplify()
        return AST.split_ast(major_req)