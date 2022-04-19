
DELETE FROM Classes;
INSERT INTO Classes(classID, className, credit, diffculty, quarters, instructor) 
VALUES (
    'CSE 12', 'Computer Systems and Assembly Language and Lab', 7, 5, '["Fall","Winter","Spring","Summer"]', 
    '["The Staff", "Tracy Larrabee", "Darrell Long", "Jose Renau Ardevol", "Matthew Guthaus", "Max Dunne", "Sagnik Nath"]'
);
DELETE FROM Requirements;
INSERT INTO Requirements(classID, preReq, majorReq, gradReq, majorElective) 
VALUES (
    'CSE 12', '["CSE 5J", "CSE 20","CSE 30","BME 160"]', '["Computer Science B.S."]', '["Computer Science B.S."]', '[]'
);
