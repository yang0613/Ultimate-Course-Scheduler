#!/usr/bin/python3
import boolean
import re

algebra = boolean.BooleanAlgebra(allowed_in_token=('.', ':', '_', '-', '/'))

reg = {}

# Mathicng classes as "CSE-101", "MATH-19A", "CSE-12/L"
reg["class"] = r"[a-zA-Z]+-(\d+\/?[a-zA-Z]+|\d+)"

# Matching categories as (Req: Major Qualification)
reg["category"] = r"(Req: *([^\)]*))"

# Matching a list as "CSE-101 MATH-19A CSE-12/L"
reg["list"] = r"({c}(?: +{c})*)".format(c=reg["class"])


# Matching a list or category as "(CSE-101 MATH-19A CSE-12/L)"
#                            or
#                               "(Req: Major Qualification)"
reg["list_or_category"] = r"(\( *{l} *\)|(\( *{c} *\)))" \
    .format(l=reg["list"],
            c=reg["category"])

# Matching a discount expr as "discounting 1 from (CSE-101 MATH-19A CSE-12/L)"
#                         or
#                            "discounting 2 from (Req: Major Qualification)"
reg["discount"] = r"discounting *(\d+) *from *{l_or_c}" \
    .format(l_or_c=reg["list_or_category"])
"""
2 of (CSE-101 MATH-19A CSE-12L) discounting 1 from (Req: Fun classes) by
quarter 5
"""
# Meaning that 2 out of the three courses, CSE-101, MATH-19A, CSE-12/L
# must be completed by the 5th quarter to fulfill a requirement.
# Additionally, classes that are  fun can at max only count towards 1
# of that requirement.

reg["full"] = r"(\d+) *of *{l_or_c} *({d} *)* *by *quarter *(\d+)" \
    .format(l_or_c=reg["list_or_category"],
            d=reg["discount"])
pat = re.compile(reg["full"])

regex = r"(\d+) *of *(\( *([a-zA-Z]+-(\d+\/?[a-zA-Z]+|\d+)(?: +[a-zA-Z]+-(\d+\/?[a-zA-Z]+|\d+))*) *\)|(\( *(Req: *([^\)]*)) *\))) *(discounting *(\d+) *from *(\( *([a-zA-Z]+-(\d+\/?[a-zA-Z]+|\d+)(?: +[a-zA-Z]+-(\d+\/?[a-zA-Z]+|\d+))*) *\)|(\( *(Req: *([^\)]*)) *\))) *)* *by *quarter *(\d+)"


def prefix_of(match, id, cmp):
    """Returns true if cmp is a prefix of the match's group id. If no 
    group exists, return false.

    Args:
        match (_sre.SRE_Match): A regex match
        id (int): The group id of match
        cmp (str): String for comparsion

    Returns:
        Bool: State of whether cmp is a prefix of match group id
    """
    str = match.group(id)
    if str is not None:
        return str.startswith(cmp)
    return False


class list_class:
    """A structure representing a list of classes via the following
    expressions:

    As any class belonging to a requirement tag "Category Name"
    "Req: Category Name"
    or
    Belonging to a direct space-delimited list of class names.
    "CSE-101 MATH-19A CSE-12/L"

    Operations can then be done to check which type of expression the 
    class is using, whether a class of interest is under this list, etc.
    """


    def __init__(self, expr):
        self.expr = expr
        if (expr.startswith("Req:")):
            self.type = "category"
            self.str = expr[4:].strip()
        else:
            self.type = "list"
            self.str = expr.strip()
            self.list = expr.split()

    def is_category(self):
        return self.type == "category"

    def verify_class(self, class_name, cat):
        """Verifies if the class belongs to this list or to the
        category cat

        Args:
            class_name (str): Class name
            category (list): A list of strings

        Returns:
            Bool: Whether or not the class is of this list
        """
        if ( self.is_category() ):
            return self.str in cat
        return class_name in self.list

    def __contains__(self, item):
        class_name = item[0] #To match format of our dummy json files
        category = item[1]
        return self.verify_class(class_name, category)

    def __str__(self):
        return self.str



class discount:
    """A structure designed to account for common curriculum policies 
    where certain classes are not fairly counted, hence the term 
    discount. For example, when a set of classes A is discounted 2 from
    another set of classes B, it means that no combination of classes 
    from B will count more than twice to the requirements for classes A. 
    """
    def __init__(self, expr, total):
        self.count = 0
        self.total = total
        self.list_class = list_class(expr)

    def is_full(self):
        return self.count > self.total

    def up(self):
        """Returns the incremental change from upping the counter by 1.
        The count must not exceed the total. In that case, 
        no incremental change occurs. Otherwise, the 
        counter was upped succesfully and returns a 1.

        Returns:
            _type_: _description_
        """
        if self.count >= self.total:
            return 0
        self.count = self.count + 1
        return 1

    def __contains__(self, item):
        class_name = item[0]
        catergories = item[1] #A list of requirement catergories
        for cat in catergories:
            if (class_name, cat) in self.list_class:
                return True
        return False


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

    "(MATH-19A or MATH-19B) and CSE-101 and 3 of (Req: Fun Classes) 
    discounting 1 from (CSE-115A ECON-104) discounting 1 from 
    (Req: Boring Classes) by quarter 5 and 1 of (CSE-13S CSE-30) by
    quarter 3".

    Meaning that the schedule must have 3 classes belonging to 
    "Fun Classes", but only one will count from either CSE-115A and
    ECON-104, and only one will also count towards that same total 
    belonging to "Boring Classes", all needing to be done by quarter 5. 
    Additionally, 1 class from CSE-13S or CSE-30 will be required by 
    quarter 3, CSE-101 will be required as well as MATH-19A or MATH-19B.
    """

    def gen_req_func(self, total, list_class, discounts, quarter):
        """Generates a requirement function that returns the status of
        requirements left to be satisfied by a specific quarter time date.

        Args:
            total (int): How many classes needed to fulfill the req
            list_class (list_class): What classes can fulfill the req
            discounts (list): A list discount class containing a list class
            and an counter for the purpose of restricting some counts of
            other classes
            quarter (int): When the classes must be taken by
        """
        def test_class(class_name, class_data):
            if class_data['Quarter'] > quarter: 
                return 0
            for discount in discounts:
                if (class_name, class_data['req']) in discount:
                    return discount.up()
            if (class_name, class_data['req']) in list_class:
                return 1
            return 0

        def req_func(schedule):
            count = 0
            for (class_name, class_data) in schedule.items():
                count += test_class(class_name, class_data)
            if total > count:
                return "{d}_of_{expr}_left_by_quarter_{q}" \
                            .format(d=total-count, expr=list_class, 
                            q=quarter).strip().replace(" ", "_")
            return "1" #Returns true - requirement is fulfilled
        return req_func

    def find_discounts(self, match):
        """Given a match, returns a list of class discounts

        Args:
            match (match): A regular expression match

        Returns:
            (list): list of class discounts
        """
        discounts = []
        for sub in re.finditer(reg["discount"], match):
            total = int(sub.group(1))
            list_expr = sub.group(7)
            d = discount(list_expr, total)
            discounts.append(d)
        return discounts

    def __init__(self, expr):
        self.expr = expr
        self.funcs = [] #A list of functions 
        self.matches = [] #A list of matches
        for match in re.finditer(pat, expr):
            #Parse for the special phrase
            self.matches.append(match.group(0))
            total = int(match.group(1))
            lst = list_class(match.group(2)[1:-1].strip())
            discounts = self.find_discounts(expr[match.start():match.end()])
            quarter = int(match.group(18))
            self.funcs.append(self.gen_req_func(total, lst,
                              discounts, quarter))

    def preresolve(self, schedule):
        """Preresolves the expression given a schedule by evaluating 
        all the relevant courses in the schedule, and reformats them
        in non-space delimited symbols for boolean algebra processing

        Args:
            schedule (dict): A json object holding our schedule

        Returns:
            str: Boolean ready string
        """
        bool = self.expr
        for i in range(len(self.funcs)):
            str = self.matches[i]
            func = self.funcs[i]
            bool = bool.replace(str, func(schedule))
        return bool

    def validate(self, schedule, pretty=True):
        """Verfies the schedule to see if it satsifies the requirements
        set by expr. If all the requirements are sastified, return "1" 
        or True. Otherwise, return the missing requirements as a 
        boolean expression.

        Args:
            schedule (dict): JSON Object holding our Schedule

        Returns:
            str: A parsable string showing our missing requirements
        """

        bool_expr = self.preresolve(schedule)

        done_classes = dict.fromkeys([algebra.Symbol(c)
                                    for c in schedule.keys()], algebra.TRUE)
        #Substitute all classes that are completed as "True" "and evaluate
        bool_expr = algebra.parse(bool_expr).subs(done_classes).simplify()
        bool_expr = str(bool_expr).replace("_", " ")
        if pretty:
            bool_expr = bool_expr.replace("&", " and ")
            bool_expr = bool_expr.replace("|", " or ")
        return str(bool_expr)

