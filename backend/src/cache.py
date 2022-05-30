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
    database = query.database_cache(parse.classIDS(schedule))
    database_cache.update(database)

def update_full_database():
    """
    Updates the cache in the database_cache to reflect the whole database

    Returns:
        None: Returns nothing and mutates database_cache
    """
    database_cache.update(query.database_cache(tuple(query.allClassIDs())))

    
def prerequisite(course):
    if course in database_cache:
        return database_cache[course]['prereq']
    None

def quarters(course):
    if course in database_cache:
        return database_cache[course]['quarters']
    return None