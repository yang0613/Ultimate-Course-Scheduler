from AST import PrereqAlgebra
from req_types import ConcurrentEnrollment
from query import singleClassRequirement
algebra = PrereqAlgebra()
from parse import missing_requirements

def generate_prereq_func():
    """To check for prerequisites, the function should remember
    what previous classes were in the schedule. This generation creates
    a function that stores their own schedule data as it is being 
    called.
    No two functions point to the same schedule.

    Returns:
        (function): A function that checks for prerequisites
    """
    classes = {}
    def prerequsites(quarter):
        """Given an existing schedule, check to see if the 
        prerequisies of all the classes in the quarter has been 
        fulfilled.

        Returns:
            (dict or boolean): a dictionary of class keys K whose values
            are a list of missing prerequisites for class K. If no such 
            missing prerequisites exist for any classes in this quarter,
            return True.
        """
        missing_prereqs = {}
        subs = {}
        for course in quarter:
            prereq = singleClassRequirement(course)[0]
            print(prereq)
            has_prereqs = algebra.parse(prereq).simplify()
            for req_type in has_prereqs.symbols:
                if isinstance(req_type, ConcurrentEnrollment):
                    req_type.setQuarterClasses(quarter)
            has_prereqs = has_prereqs.subs(classes).simplify()
            if has_prereqs != algebra.TRUE:
                bool_expr = str(has_prereqs)
                missing_prereqs[course] = missing_requirements(bool_expr)
            subs[course] = algebra.TRUE

        classes.update(subs)            
        if missing_prereqs:
            return missing_prereqs
        return True
    return prerequsites


def time_conflict(quarter):
    """Given a quarter of classes, check to see if any of these
    classe have a time conflict with one another. 

    Returns:
        (dict or boolean): A dictionary of class keys K whose values
        are a list of conclicts for class K. If no conflicts arise
        between classes of this quarter, return True.
    """

    def is_conflict(c_1, c_2):
        if c_1['start'] < c_2['end'] and c_1['end'] > c_2['start']:
            return "{c1} is in conflict with {c2}".format(c1 = c_1, c2=c_2)
        return False

    conflicts = {}
    #Optimized Naive implementation for time conflicts: n^2 complexity
    classes_left = quarter.copy()
    while classes_left:
        class_ = classes_left.pop()
        for other in classes_left:
            conflict = is_conflict(class_, other)
            if conflict:
                if class_ in conflicts:
                    conflicts[class_].append(conflict)
                else:
                    conflicts[class_] = [conflict]
    if conflicts:
        return conflicts
    return True

    
    

