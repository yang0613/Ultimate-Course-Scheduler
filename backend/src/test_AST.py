#!/usr/bin/python3.9
import AST

"""
This is not a up-to-standard UnitTest. The reason is because
testing for an AST can be costly as you would need to manually input
a tree. Instead I have compiled a list of a variety of prerequisite
expressions where you can check visually what they should look like to
see if our implementation matches expected behavior.
"""
test = AST.PrereqAlgebra()
expr = "Previous or concurrent enrollment in MATH 3, AM 3, or equivalent, or a mathematics placement score of 300 or higher; taking the online chemistry self-assessment exam is strongly recommended."
expr2 = "AM 3 or AM 6, or MATH 3 or higher; or mathematics placement examination (MPE) score of 300 or higher; or AP Calculus AB exam score of 3 or higher; ENVS 23 recommended as prerequisite to this course."
expr3 = "score of 300 or higher on the mathematics placement examination (MPE), or AM 3 or AM 6 or AM 11A or AM 15A or MATH 3 or MATH 11A or MATH 19A. Concurrent enrollment in STAT 7L is required."
expr4 = "MATH 2 or mathematics placement examination (MPE) score of 200 or higher or higher."
expr5 = "MATH 2 or mathematics placement (MP) score of 200 or higher. Students may not enroll in or receive credit for MATH 3 after receiving credit with a \"C\" or better in AM 11A, MATH 11A, MATH 19A, MATH 20A or equivalents."
expr6 = ''
expr7 = 'ENVS 23 or CHEM 1A; ENVS 24 or BIOE 20C; ENVS 25; and STAT 7 and STAT 7L, or ECON 113 or OCEA 90; and one from: ANTH 2, SOCY 1, SOCY 10, SOCY 15, PHIL 21, PHIL 22, PHIL 24, PHIL 28, or PHIL 80G. Concurrent enrollment in ENVS 100L Is required.'
expr8 = "Satisfaction of the Entry Level Writing and Composition requirements. Concurrent enrollment in ENVS 100 is required."
expr9 = "Concurrent enrollment in ENVS 130L and previous or concurrent enrollment in ENVS 100 and ENVS 100L, or by permission of instructor."
expr10 = "ENVS 100 and ENVS 100L; Entry Level Writing and Composition requirements. Enrollment is restricted to senior environmental studies majors and the combined majors with Earth sciences, biology, and economics."
expr11 = "Completion of ENVS 100 and ENVS 100L and ENVS 195A."
expr12 = "ENVS 183A. Students submit petition to course-sponsoring agency. Enrollment is restricted to environmental studies majors and the combined majors with Earth sciences, biology, and economics."
expr13 = "Completion of ENVS 100 and ENVS 100L, and Entry Level Writing and Composition requirements."
expr14 = "one from: \"req\" CSE 103, CSE 102, CSE 104, or MATH 19A start discounting two from: CSE 102 or CSE 104 discounting two from: CSE 103 or MATH 19A by quarter 5"
expr15 = 'CSE 15 and CSE 15L; or CSE 13S and CMPM 35; or CSE 13E and CMPM 35; or ECE 13 and CMPM 35; or CSE 101.'
expr16 = 'CSE 15 and CSE 15L; or CSE 13S and CMPM 35; or CSE 13E and CMPM 35; or ECE 13 and CMPM 35; or CSE 101. ECON 101.'
expr17 = 'MATH 11A or MATH 19A or MATH 20A or AM 11A or AM 15A'
expr18 = "satisfaction of the Entry Level Writing and Composition requirements and CSE 101 and CSE 130."
expr19 = "CSE 100"
expr20 = "(ECON 11A or AM 11A) and (ECON 11B or AM 11B); or MATH 11A and MATH 11B and MATH 22; or MATH 19A and MATH 19B and (MATH 22 or MATH 23A)"
expr21 = "score of 300 or higher on the mathematics placement examination (MPE), or AM 3 or AM 6 or AM 11A or AM 15A or MATH 3 or MATH 11A or MATH 19A. Concurrent enrollment in STAT 7L is required."
test_expr = expr21
print("=====================")
print("Raw Expression:")
print(test_expr)
parsed = test.parse(test_expr).simplify()
print("=====================")
print("AST representation:")
print(parsed.pretty())
print("=====================")

print("Boolean string representation")
print(AST.missing_requirements(parsed))
print("=====================")