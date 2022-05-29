#Algorithm referenced
#https://etda.libraries.psu.edu/files/final_submissions/10828#:~:text=The%20Course%20Scheduling%20Algorithm%20returns,is%20kept%20to%20a%20minimum.
#https://www.codeproject.com/Articles/23111/Making-a-Class-Schedule-Using-a-Genetic-Algorithm
#Using DEAP
from copy import deepcopy
import AST
import parse
import cache
import random
import constraint
import constraint_types
import major_database

cache.update_full_database()
database = cache.database_cache
#Assumptions to simplify our generation
MAX_COURES_PER_QUARTER = 3
MAX_FITNESS = 1000
MAJOR = 'Computer Science B.S.'
TOTAL_INDIVIDUALS = 10
TOTAL_GENERATIONS = 10
MAXIMIUM_WAIT = 30
MUTATE_PROBABILITY = 0.5

"""
Todo
Implement a cache that stores all the related database Done
decide on whether or not for the fitness function to punish each
constraint equally Done - For Now
Implement a way to identify each punishment clearly Done - For Now
Integrate existing ideas WITH DEAP
Ignore: professor course load Done
Generation population
Don't mutate parts of existing schedules if its an inital input
Mutatuin: For each course do a swap, if it is better fitness
keep it
Local optimization: some sort of linear path that can gurantee 
increasing the fitness(optional)
Replacement on schedule
"""
con = constraint.Constraint([constraint_types.generate_prereq_func(), 
                            constraint_types.not_avaliable_during])
major_boolean_expr = major_database.MAJOR_MATCH_EXPRESSION[MAJOR]
ast = AST.algebra.parse(major_boolean_expr).simplify()
FITNESS_MEMOIZATION = []
GLOBAL_SCHEDULES = []
def Fitness(schedule):
    """Return the fitness value of a schedule
    """
    fitness = MAX_FITNESS - schedule_penalty(schedule) - major_penalty(schedule)
    return fitness
    

def major_penalty(schedule):
    """Given an schedule, return the penalty of an schedule in respect
    to the major

    Currently, it is hard coded to support only Computer Science B.S.
    """
    process_ast = AST.convert_schedule(schedule)
    major_req = ast.subs(process_ast).simplify()
    per_penalty = 20
    return len(AST.split_ast(major_req)) * per_penalty

def schedule_penalty(schedule):
    """Given an schedule, return the penalty of an schedule
    Args:
        schedule (JSON): JSON Object holding our Schedule
    """
    try:
        del con.constraints[0]
        con.constraints.insert(0, constraint_types.generate_prereq_func())
        schedule_errors = con.validate(schedule)
    except:
        return MAX_FITNESS
    per_penalty = 5
    penalty = 0
    for year in schedule_errors:
        for quarter in schedule_errors[year].keys():
            for errors in schedule_errors[year][quarter].values():
                penalty = penalty + (len(errors)*per_penalty)
    return penalty

def ScheduleTemplate():
    """Return a baseline schedule template with all the years
    and quarters, but no classes are inserted.
    """
    template = {}
    years = ["first", "second", "third", "fourth"]
    quarters = ["Fall", "Winter", "Spring", "Summer"]
    for year in years:
        template[year] = {}
        for quarter in quarters:
            template[year][quarter] = []
    return template

def randomClass():
    """Return a random class from the database of classes
    """
    return random.choice(list(database.keys()))

def randomListClasses(n):
    """Returns a list of random classes of length n

    Args:
        n (int): The length of the list
    """
    return random.choices(list(database.keys()), k=n)
def emptySchedule(schedule):
    """Returns True if the schedule is empty. Otherwise, return false

    Args:
        schedule (JSON): JSON Object holding our Schedule

    Returns:
        A stream of classes with their year and quarter 
    """
    return ScheduleTemplate() == schedule


def allClasses(schedule):
    """Wrapper function to get all the list of classes in a schedule

    Args:
        schedule (JSON): JSON Object holding our Schedule
    
    Returns:
        A list of classes
    """
    return list(parse.classIDS(schedule))

def Best(population, fitness_list):
    """Returns the schedule with the best fitness

    Args:
        population (list): A list of schedules
    """
    index_max = max(range(len(fitness_list)), key=fitness_list.__getitem__)
    return population[index_max]

def GeneratePopulation(schedule, generations):
    """Generate a population of schedules of length generations  
    """
    global FITNESS_MEMOIZATION
    global GLOBAL_SCHEDULES
    schedules = []
    for gen in range(generations):
        individual = deepcopy(schedule)
        for _, _, classes in parse.schedule_tokens(individual):
            add_classes = randomListClasses(MAX_COURES_PER_QUARTER
                                            - len(classes))
            classes.extend(add_classes)
        schedules.append(individual)
        fitness = Fitness(individual)
        FITNESS_MEMOIZATION.append(fitness)
    GLOBAL_SCHEDULES = schedules
    return schedules

def RandomSelection(population):
    return random.choice(population)

def Worst(population, fitness_list):
    index_min = min(range(len(fitness_list)), key=fitness_list.__getitem__)
    return population[index_min]
def ScheduleMutation(schedule, initialClasses):
    for _, _, classes in parse.schedule_tokens(schedule):
        for course in classes:
            m = random.uniform(0,1)
            if m <= MUTATE_PROBABILITY and course not in initialClasses:
                classes[classes.index(course)] = randomClass()

def ScheduleRepair(schedule):
    """Remove duplicates in a schedule
    """
    for _, _, classes in parse.schedule_tokens(schedule):
        duplicates = [x for x in classes if classes.count(x) >= 2]
        for course in duplicates:
            while (classes.count(course) != 1):
                classes[classes.index(course)] = randomClass()
def Replace(W, w_parent, w_child):
    global FITNESS_MEMOIZATION
    w_child_fit = Fitness(w_child)
    w_parent_fit = Fitness(w_parent)
    if w_child_fit > w_parent_fit:
        index = W.index(w_parent)
        W[index] = w_child
        FITNESS_MEMOIZATION[index] = w_child_fit
    else:
        w_worst = Worst(W, FITNESS_MEMOIZATION)
        w_worst_fit = Fitness(w_worst)
        if w_child_fit > w_worst_fit:
            index = W.index(w_worst)
            W[index] = w_child
            FITNESS_MEMOIZATION[index] = w_child_fit
        
        
def GenerateSchedule(schedule):
    g = 0
    W = GeneratePopulation(schedule, TOTAL_INDIVIDUALS)
    initialClasses = allClasses(schedule)
    while g <= TOTAL_GENERATIONS:
        w_parent = RandomSelection(W)
        w_child = deepcopy(w_parent)
        ScheduleMutation(w_child, initialClasses)
        ScheduleRepair(w_child)
        Replace(W, w_parent, w_child)
        g = g + 1
    best_schedule = Best(W, FITNESS_MEMOIZATION)
    return best_schedule
