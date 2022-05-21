#!/usr/bin/python3
from reqs import requirement
import json
import query
from pprint import pprint

# We changed 1, 2, 3, 4 to First, Second, Third, Fourth
# I just put 1, 2, 3, 4 here since that's what you currently have

# Valid
expr="""
{
	"1": {
		"Fall": ["CSE 20", "MATH 19A"],
		"Winter": ["CSE 12", "CSE 16", "CSE 30"],
		"Spring": ["CSE 13S", "MATH 21"],
		"Summer": []
	},
	"2": {
		"Fall": ["CSE 101", "MATH 19B"],
		"Winter": ["CSE 130", "CSE 103", "ECE 30"],
		"Spring": ["CSE 102", "CSE 120"],
		"Summer": []
	},
	"3": {
		"Fall": ["CSE 115A", "CSE 116"],
		"Winter": ["CSE 115B", "STAT 131"],
		"Spring": ["CSE 115C", "CSE 111"],
		"Summer": []
	},
	"4": {
		"Fall": ["CSE 144", "CSE 183"],
		"Winter": ["CSE 180"],
		"Spring": [],
		"Summer": []
	}
}
"""

# Valid. Just minor change in class order in year 2.
expr2="""
{
	"1": {
		"Fall": ["CSE 20", "MATH 19A"],
		"Winter": ["CSE 12", "CSE 16", "CSE 30"],
		"Spring": ["CSE 13S", "MATH 21"],
		"Summer": []
	},
	"2": {
		"Fall": ["CSE 101", "MATH 19B"],
		"Winter": ["CSE 102", "CSE 103", "ECE 30"],
		"Spring": ["CSE 130", "CSE 120"],
		"Summer": []
	},
	"3": {
		"Fall": ["CSE 115A", "CSE 116"],
		"Winter": ["CSE 115B", "STAT 131"],
		"Spring": ["CSE 115C", "CSE 111"],
		"Summer": []
	},
	"4": {
		"Fall": ["CSE 144", "CSE 183"],
		"Winter": ["CSE 180"],
		"Spring": [],
		"Summer": []
	}
}
"""

# 115A for DC req(doesn't count as elective if used as DC req)  183 Comprehensive Req.
# "A passed capstone course also counts toward satisfying the minimum number of upper-division electives requirement." -- 2021-22 Catalog
# Should be valid, since capstone counts as an elective
expr3="""
{
	"1": {
		"Fall": ["CSE 20", "MATH 19A"],
		"Winter": ["CSE 12", "CSE 16", "CSE 30"],
		"Spring": ["CSE 13S", "MATH 21"],
		"Summer": []
	},
	"2": {
		"Fall": ["CSE 101", "MATH 19B"],
		"Winter": ["CSE 130", "CSE 103", "ECE 30"],
		"Spring": ["CSE 102", "CSE 120"],
		"Summer": []
	},
	"3": {
		"Fall": ["CSE 115A", "CSE 116"],
		"Winter": ["CSE 115B", "STAT 131"],
		"Spring": ["CSE 115C", "CSE 111"],
		"Summer": []
	},
	"4": {
		"Fall": ["CSE 183"],
		"Winter": [],
		"Spring": [],
		"Summer": []
	}
}
"""

# Valid. Fall and Winter empty for 4
expr4="""
{
	"1": {
		"Fall": ["CSE 20", "MATH 19A"],
		"Winter": ["CSE 12", "CSE 16", "CSE 30"],
		"Spring": ["CSE 13S", "MATH 21"],
		"Summer": []
	},
	"2": {
		"Fall": ["CSE 101", "MATH 19B"],
		"Winter": ["CSE 130", "CSE 103", "ECE 30"],
		"Spring": ["CSE 102", "CSE 120"],
		"Summer": []
	},
	"3": {
		"Fall": ["CSE 115A", "CSE 116"],
		"Winter": ["CSE 115B", "STAT 131"],
		"Spring": ["CSE 115C", "CSE 111"],
		"Summer": []
	},
	"4": {
		"Fall": [],
		"Winter": [],
		"Spring": ["CSE 144","CSE 180", "CSE 183"],
		"Summer": []
	}
}
"""

# Not valid, missing one elective
expr5="""
{
	"1": {
		"Fall": ["CSE 20", "MATH 19A"],
		"Winter": ["CSE 12", "CSE 16", "CSE 30"],
		"Spring": ["CSE 13S", "MATH 21"],
		"Summer": []
	},
	"2": {
		"Fall": ["CSE 101", "MATH 19B"],
		"Winter": ["CSE 130", "CSE 103", "ECE 30"],
		"Spring": ["CSE 102", "CSE 120"],
		"Summer": []
	},
	"3": {
		"Fall": ["CSE 115A", "CSE 116"],
		"Winter": ["CSE 115B", "STAT 131"],
		"Spring": ["CSE 115C", "CSE 111"],
		"Summer": []
	},
	"4": {
		"Fall": ["CSE 183"],
		"Winter": [],
		"Spring": [],
		"Summer": []
	}
}
"""

# Invalid: CSE 13S missing
expr6="""
{
	"1": {
		"Fall": ["CSE 20", "MATH 19A"],
		"Winter": ["CSE 12", "CSE 16", "CSE 30"],
		"Spring": ["MATH 21"],
		"Summer": []
	},
	"2": {
		"Fall": ["CSE 101", "MATH 19B"],
		"Winter": ["CSE 130", "CSE 103", "ECE 30"],
		"Spring": ["CSE 102", "CSE 120"],
		"Summer": []
	},
	"3": {
		"Fall": ["CSE 115A", "CSE 116"],
		"Winter": ["CSE 115B", "STAT 131"],
		"Spring": ["CSE 115C", "CSE 111"],
		"Summer": []
	},
	"4": {
		"Fall": ["CSE 144", "CSE 183"],
		"Winter": ["CSE 180"],
		"Spring": [],
		"Summer": []
	}
}
"""

# Invalid. Missing CSE 130 for 115A
# Note, CSE130 is in winter quarter of year 2 and is taken before CSE115A
expr7="""
{
	"1": {
		"Fall": ["CSE 20", "MATH 19A"],
		"Winter": ["CSE 12", "CSE 16", "CSE 30"],
		"Spring": ["CSE 13S", "MATH 21"],
		"Summer": []
	},
	"2": {
		"Fall": ["CSE 101", "MATH 19B"],
		"Winter": ["CSE 130", "CSE 103", "ECE 30"],
		"Spring": ["CSE 102", "CSE 120"],
		"Summer": []
	},
	"3": {
		"Fall": ["CSE 115A", "CSE 116"],
		"Winter": ["CSE 115B", "STAT 131"],
		"Spring": ["CSE 115C", "CSE 111"],
		"Summer": []
	},
	"4": {
		"Fall": ["CSE 144", "CSE 183"],
		"Winter": ["CSE 180"],
		"Spring": [],
		"Summer": []
	}
}
"""

# Invalid. CSE 102 needs 101 taken a previous quarter
expr8="""
{
	"1": {
		"Fall": ["CSE 20", "MATH 19A"],
		"Winter": ["CSE 12", "CSE 16", "CSE 30"],
		"Spring": ["CSE 13S", "MATH 21"],
		"Summer": []
	},
	"2": {
		"Fall": ["CSE 101", "CSE 102", "MATH 19"],
		"Winter": ["CSE 103", "ECE 30"],
		"Spring": ["CSE 130", "CSE 120"],
		"Summer": []
	},
	"3": {
		"Fall": ["CSE 115A", "CSE 116"],
		"Winter": ["CSE 115B", "STAT 131"],
		"Spring": ["CSE 115C", "CSE 111"],
		"Summer": []
	},
	"4": {
		"Fall": ["CSE 144", "CSE 183"],
		"Winter": ["CSE 180"],
		"Spring": [],
		"Summer": []
	}
}
"""

# Invalid or Valid? What if CSE 30 included but not CSE 20?
expr9="""
{
	"1": {
		"Fall": ["MATH 19A"],
		"Winter": ["CSE 12", "CSE 16", "CSE 30"],
		"Spring": ["CSE 13S", "MATH 21"],
		"Summer": []
	},
	"2": {
		"Fall": ["CSE 101", "MATH 19B"],
		"Winter": ["CSE 130", "CSE 103", "ECE 30"],
		"Spring": ["CSE 102", "CSE 120"],
		"Summer": []
	},
	"3": {
		"Fall": ["CSE 115A", "CSE 116"],
		"Winter": ["CSE 115B", "STAT 131"],
		"Spring": ["CSE 115C", "CSE 111"],
		"Summer": []
	},
	"4": {
		"Fall": ["CSE 144", "CSE 183"],
		"Winter": ["CSE 180"],
		"Spring": [],
		"Summer": []
	}
}
"""

# Invalid? CSE 101 isn't available during the summer right? Or does it vary?
# 
expr10="""
{
	"1": {
		"Fall": ["CSE 20", "MATH 19A"],
		"Winter": ["CSE 12", "CSE 16", "CSE 30"],
		"Spring": ["CSE 13S", "MATH 21"],
		"Summer": ["CSE 101"]
	},
	"2": {
		"Fall": ["MATH 19B"],
		"Winter": ["CSE 130", "CSE 103", "ECE 30"],
		"Spring": ["CSE 102", "CSE 120"],
		"Summer": []
	},
	"3": {
		"Fall": ["CSE 115A", "CSE 116"],
		"Winter": ["CSE 115B", "STAT 131"],
		"Spring": ["CSE 115C", "CSE 111"],
		"Summer": []
	},
	"4": {
		"Fall": ["CSE 144", "CSE 183"],
		"Winter": ["CSE 180"],
		"Spring": [],
		"Summer": []
	}
}
"""

# Invalid. Comprehensive Req missing
expr11="""
{
	"1": {
		"Fall": ["CSE 20", "MATH 19A"],
		"Winter": ["CSE 12", "CSE 16", "CSE 30"],
		"Spring": ["CSE 13S", "MATH 21"],
		"Summer": []
	},
	"2": {
		"Fall": ["CSE 101", "MATH 19B"],
		"Winter": ["CSE 130", "CSE 103", "ECE 30"],
		"Spring": ["CSE 102", "CSE 120"],
		"Summer": []
	},
	"3": {
		"Fall": ["CSE 115A", "CSE 116"],
		"Winter": ["CSE 115B", "STAT 131"],
		"Spring": ["CSE 180", "CSE 111"],
		"Summer": []
	},
	"4": {
		"Fall": ["CSE 118", "CSE 117"],
		"Winter": [""],
		"Spring": [],
		"Summer": []
	}
}
"""
#No Upper Divsion Electives
expr12="""
{
	"1": {
		"Fall": ["CSE 20", "MATH 19A"],
		"Winter": ["CSE 12", "CSE 16", "CSE 30"],
		"Spring": ["CSE 13S", "MATH 21"],
		"Summer": []
	},
	"2": {
		"Fall": ["CSE 101", "MATH 19B"],
		"Winter": ["CSE 130", "CSE 103", "ECE 30"],
		"Spring": ["CSE 102", "CSE 120"],
		"Summer": []
	},
	"3": {
		"Fall": [],
		"Winter": ["STAT 131"],
		"Spring": [ ],
		"Summer": []
	},
	"4": {
		"Fall": [],
		"Winter": [""],
		"Spring": [],
		"Summer": []
	}
}
"""

#One upper division elective combination for CSE: PHYS 5A and PHYS 5B
expr13="""
{
	"1": {
		"Fall": ["CSE 20", "MATH 19A"],
		"Winter": ["CSE 12", "CSE 16", "CSE 30"],
		"Spring": ["CSE 13S", "MATH 21"],
		"Summer": []
	},
	"2": {
		"Fall": ["CSE 101", "MATH 19B"],
		"Winter": ["CSE 130", "CSE 103", "ECE 30"],
		"Spring": ["CSE 102", "CSE 120"],
		"Summer": []
	},
	"3": {
		"Fall": [],
		"Winter": ["STAT 131"],
		"Spring": [],
		"Summer": []
	},
	"4": {
		"Fall": ["PHYS 5A", "PHYS 5B"],
		"Winter": [""],
		"Spring": [],
		"Summer": []
	}
}
"""

#One upper division elective combination for CSE: PHYS 5A only won't count
expr14="""
{
	"1": {
		"Fall": ["CSE 20", "MATH 19A"],
		"Winter": ["CSE 12", "CSE 16", "CSE 30"],
		"Spring": ["CSE 13S", "MATH 21"],
		"Summer": []
	},
	"2": {
		"Fall": ["CSE 101", "MATH 19B"],
		"Winter": ["CSE 130", "CSE 103", "ECE 30"],
		"Spring": ["CSE 102", "CSE 120"],
		"Summer": []
	},
	"3": {
		"Fall": [],
		"Winter": ["STAT 131"],
		"Spring": [],
		"Summer": []
	},
	"4": {
		"Fall": ["PHYS 5A", ""],
		"Winter": [""],
		"Spring": [],
		"Summer": []
	}
}
"""

#An mathematic/computional media elective won't count more than two
expr15="""
{
	"1": {
		"Fall": ["CSE 20", "MATH 19A"],
		"Winter": ["CSE 12", "CSE 16", "CSE 30"],
		"Spring": ["CSE 13S", "MATH 21"],
		"Summer": []
	},
	"2": {
		"Fall": ["CSE 101", "MATH 19B"],
		"Winter": ["CSE 130", "CSE 103", "ECE 30"],
		"Spring": ["CSE 102", "CSE 120"],
		"Summer": []
	},
	"3": {
		"Fall": [],
		"Winter": ["STAT 131"],
		"Spring": [],
		"Summer": []
	},
	"4": {
		"Fall": ["PHYS 5A", "PHYS 5B"],
		"Winter": ["AM 114", "AM 147"],
		"Spring": [],
		"Summer": []
	}
}
"""

#ENVS 130A requires concurrent enrollment, so DOES PHYS 5A
expr16="""
{
	"1": {
		"Fall": ["ENVS 130A", "ENVS 130L", "ENVS 100", "ENVS 100L", "CSE 20", "MATH 19A"],
		"Winter": ["CSE 12", "CSE 16", "CSE 30"],
		"Spring": ["CSE 13S", "MATH 21"],
		"Summer": []
	},
	"2": {
		"Fall": ["CSE 101", "MATH 19B"],
		"Winter": ["CSE 130", "CSE 103", "ECE 30"],
		"Spring": ["CSE 102", "CSE 120"],
		"Summer": []
	},
	"3": {
		"Fall": [],
		"Winter": ["STAT 131"],
		"Spring": [],
		"Summer": []
	},
	"4": {
		"Fall": ["PHYS 5A", "PHYS 5B"],
		"Winter": ["AM 114", "AM 147"],
		"Spring": [],
		"Summer": []
	}
}
"""

#Attempt to Fulfill the requirements for ENVS 100 and ENVS 100L
expr16="""
{
	"1": {
		"Fall": [ "CSE 20", "MATH 19A"],
		"Winter": ["CSE 12", "CSE 16", "CSE 30"],
		"Spring": ["CSE 13S", "MATH 21"],
		"Summer": []
	},
	"2": {
		"Fall": ["CSE 101", "MATH 19B"],
		"Winter": ["CSE 130", "CSE 103", "ECE 30"],
		"Spring": ["CSE 102", "CSE 120"],
		"Summer": ["BIOE 20C"]
	},
	"3": {
		"Fall": ["ENVS 25", "STAT 7L", "STAT 7"],
		"Winter": ["STAT 131", "ANTH 2", "CHEM 1A"],
		"Spring": ["ENVS 130A", "ENVS 130L", "ENVS 100", "ENVS 100L"],
		"Summer": []
	},
	"4": {
		"Fall": ["PHYS 5A", "PHYS 5B"],
		"Winter": ["AM 114", "AM 147"],
		"Spring": [],
		"Summer": []
	}
}
"""
req = requirement(major='Computer Science B.S.')
test = expr16
missing = req.validate(json.loads(test))
major = req.verify_major(json.loads(test))
pprint(missing)
print(major)