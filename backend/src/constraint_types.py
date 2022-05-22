from AST import PrereqAlgebra
from AST import missing_requirements
from req_types import ConcurrentEnrollment
import cache
algebra = PrereqAlgebra()

def generate_prereq_func():
    """To check for prerequisites, the function should remember
    what previous classes were in the schedule. This generation creates
    a function that stores their own schedule data as it is being 
    called.
    No two functions point to the same schedule.

    Returns:
        (function): A function that checks for prerequisites
    """
    schedule = {}
    def prerequsites(quarter, classes):
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
        for course in classes:
            prereq = cache.prerequisite(course)
            if prereq:
                #Adapt query.py format, first index is prereq string
                has_prereqs = algebra.parse(prereq).simplify()
                for req_type in has_prereqs.symbols:
                    if isinstance(req_type, ConcurrentEnrollment):
                        req_type.setQuarterClasses(classes)
                has_prereqs = has_prereqs.subs(schedule).simplify()
                if has_prereqs != algebra.TRUE:
                    missing_prereqs[course] = missing_requirements(has_prereqs)
        subs = {course: algebra.TRUE for course in classes}
        schedule.update(subs)            
        if missing_prereqs:
            return missing_prereqs
        return True
    return prerequsites

def not_avaliable_during(quarter, classes):
    """Given a quarter of classes, check to see if any of these
    classes are actually avaliable during the specific quarter.
    Returns:
        (dict or boolean): A dictionary of class keys K whose values
        are a list of conclicts for class K. If every class is
        avaliable for their specific quarter in the schedule, return True.
    """
    wrong_quarter ={}
    for course in classes:
        avaliable_quarters = cache.quarters(course)   
        if avaliable_quarters and quarter not in avaliable_quarters:
            wrong_quarter[course] = [f"{course} in {quarter} is not avaliable during {avaliable_quarters}"]
    if wrong_quarter:
        return wrong_quarter        
    return True


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

    
    

