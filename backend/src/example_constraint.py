
import boolean

algebra = boolean.BooleanAlgebra()
"""NOTE: THIS FILE IS WORK IN PROGRESS
"""

def prereqsuites(schedule, classObj):
    """Given an valid schedule, check to see if the prerequsites of
    this class is fulfilled. 

    Returns:
        (str or boolean): The missing prerequisites if they are not 
        fulfilled, otherwise return True.
    """
    classes =  dict.fromkeys([algebra.Symbol(c)
                    for c in schedule.keys()], algebra.TRUE)

    prereqs = algebra.parse(classObj['prereqs']).subs(classes).simplify()

    if prereqs == algebra.TRUE:
        return True
    return str(prereqs)

def time_conflict(schedule, classObj):
    """Given an valid schedule, check to see if there any time conflicts
    with this class.

    Returns:
        (str or boolean): The class that is in conflict if there is a
        time conflict, otherwise return True.
    """

    def is_conflict(c_1, c_2):
        return c_1['start'] < c_2['end'] and c_1['end'] > c_2['start']
    for class_ in schedule:
        if is_conflict(class_['timeslot'], classObj['timeslot']):
            return "{c1} is in conflict with {c2}".format(c1 = class_, c2=classObj)
    return True
    
    

