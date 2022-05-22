import query
import parse
database_cache = {}
def update_cache(schedule):
    """Updates the cache in database_cache to reflect the contents
    of the schedule.

    Args:
        schedule (JSON): JSON Object holding our Schedule

    Returns:
        None: Returns nothing and mutates database_cache
    """
    global database_cache
    database_cache = query.database_cache(parse.classIDS(schedule))
    
def prerequisite(course):
    if course in database_cache:
        return database_cache[course]['prereq']
    None

def quarters(course):
    if course in database_cache:
        return database_cache[course]['quarters']
    return None