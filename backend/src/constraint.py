
from parse import schedule_tokens


def dict_list_append(src: dict[str, list], dict: dict[str, list]):
    """
    Add dictionary dict to src, merging matching keys as values where
    the list of src and list of dict and appended together. Assumes that
    each element of both lists are unqiue.
    Args:
        dict_src (dict): The dictionary with list values being added to
        append (dict): A constant dictionary with list values

    Returns:
        (dict): A dictionary with shared key values
    """
    for key,list in dict.items():
        if key in src.keys():
            src[key].append(list)
        else:
            src[key] = [list]

class Constraint:
    """
    A data structure that allows programmers to validate any schedule
    from a set of constraints like conflicting time slots, non-fulfilled 
    prequisites, etc. 

    Because each constraint is a self-contained function, programmers
    can more easily work on the fundamental nature of each constraint,
    rather than worrying about how to interface their constraint to fit
    with the underlying schedule data format.
    """

    def __init__(self, constraints=[]):
        """Creates a constraint class containing a list of constraints
        Args:
            constraints (list, optional): A list of 
            constraint functions. Defaults to [].
        """
        self.constraints = constraints

    def add(self, constraint):
        """Adds a constraint to our validation class.

        Args:
            constraint (function): Returns a dictionary of key classes
            whose values are a list of errors pertaining to that class
            given a schedule. Otherwise, return True, signaling that
            the constraint has been fulfilled. 

            For example, a constraint function that checks for 
            prereqs and conflicting timeslots for this quarter 
            will return:
            {
                "CSE-102": ["Missing a preqreusite CSE-101"],
                "MATH-19A": ["Has a timeconflict with CSE-102"]
            }

            Another constraint function that checks for only concurrent
            enrollment will return:
            {
                "PHYS-6A": ["Missing conccurent enrollment "PHYS-6L"]
            }
        
            A constriant function that complains if any classes start
            with the letter "Z", and since no classes in the schedule
            starts with "Z", the schedule is fulfilled for this
            constraint and will return:
            True
        """
        self.constraints.append(constraint)


    def validate(self, schedule):
        """Given a schedule, shows any scheduling errors due to 
        certain constraints in our class. 
        Args:
            schedule (dict): JSON Object holding our Schedule

        Returns:
            dict: A dictionary showing where the schedule error is by
            class and quarter(location) and details of the error.

            Example:
            {
                "1":
                {
                    "Fall":,
                        "CSE-102": ["Missing a preqreusite CSE-101"]
                        "MATH-19A": ["Has a timeconflict with PHYS-6A"]
                        "PHYS-6A": ["Has a timeconflict with MATH-19A", 
                                    "Missing concurrent enrollment with PHYS-6L"]
                }
                "2":
                {
                    "Winter":,
                        "CSE-115A": ["Not avaliable during this quarter"]
                }
            }
        """
        schedule_errors = {}
        for year, quarter, classes in schedule_tokens(schedule):
            error = {}
            if classes:
                for func in self.constraints:
                    #Applys the constraints to each quarter
                    fail_constraint = func(quarter, classes)

                    #And if the constraint is not satsified, add it to the list of errors
                    if fail_constraint != True:
                        dict_list_append(error, fail_constraint)
            if year not in schedule_errors.keys():
                schedule_errors[year] = {}
            schedule_errors[year][quarter] = error
        return schedule_errors

