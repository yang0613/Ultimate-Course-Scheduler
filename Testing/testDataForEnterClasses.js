// THE FOLLOWING COMMENTED CODE BELOW CONTAIN TEST AND OTHER DUMMY DATA USED FOR EnterClasses.js

// ------------------- 1 --------------------------
// Used as dummy data to test if search bar works(if it lists available classes)
//availableClasses: ["CSE 101", "CSE 102", "CSE 103", "CSE 201", "STAT 131", "MATH 19A", "MATH 19B", "MATH 21", "dummy1", "dummy2", "dummy3", "dummy4"],

// ------------------- 2 -------------------------
// Dummy data used for testing if the handler for showing saved classes works properly
/*
let acadPlanObj = {
"First": {
    "Fall": ["CSE 20", "MATH 19A"],
    "Winter": ["CSE 12", "CSE 16", "CSE 30"],
    "Spring": ["CSE 13S", "MATH 21"],
    "Summer": []
},
"Second": {
    "Fall": ["CSE 101", "MATH 19B"],
    "Winter": ["CSE 130", "CSE 103", "ECE 30"],
    "Spring": ["CSE 102", "CSE 120"],
    "Summer": []
},
"Third": {
    "Fall": ["CSE 115A", "CSE 116"],
    "Winter": ["CSE 115B", "STAT 131"],
    "Spring": ["CSE 115C", "CSE 111"],
    "Summer": ["CSE 3"]
},
"Fourth": {
    "Fall": ["CSE 144", "CSE 183"],
    "Winter": ["CSE 180"],
    "Spring": [],
    "Summer": []
}
};
*/

/*  Format for acadPlanObj that will be passed to backend for verification
{
    "First": {
        "Fall": ["CSE 101"],
        "Winter": ["CSE 102", "CSE 103"],
        "Spring": [],
        "Summer": []
    },
    "Second": {
        "Fall": [],
        "Winter": ["CSE 130", "CSE 120"],
        "Spring": [],
        "Summer": []
    },
    "Third": {
        "Fall": ["CSE 115A"],
        "Winter": ["CSE 115B"],
        "Spring": ["CSE 115C"],
        "Summer": []
    },
    "Fourth": {
        "Fall": [],
        "Winter": [],
        "Spring": [],
        "Summer": []
    }
}
*/

/* Used as dummy data containing errors returned by backend
    // https://stackoverflow.com/questions/805107/creating-multiline-strings-in-javascript 
    let resultJSON = `
    {
        "1": {
            "Fall": {
                "CSE 102": ["Missing a prerequisite CSE 101"],
                "CSE 130": ["Error 1", "Error 2"]
            },
            "Winter": {
                "CSE 111": ["Error A", "Error B"]
            },
            "Summer": {
                "CSE 114A": ["Error C"],
                "CSE 110A": ["Error D"]
            }
        },
        "2": {
            "Fall": {
                "CSE 183": ["Error 1", "Error 2"],
                "CSE 130": ["Error A"]
            },
            "Winter": {
                "CSE 111": ["Error B"]
            },
            "Spring": {
                "CSE 114A": ["Error C"],
                "CSE 110A": ["Error D"]
            },
            "Summer": {
                "CSE 110B": ["Error E"]
            }
        },
        "4": {
            "Fall": {
                "CSE 138": ["Error 1", "Error 2"],
                "CSE 130": ["Error A"]
            },
            "Winter": {
                "CSE 111": ["Error B"]
            },
            "Spring": {
                "CSE 114A": ["Error C"],
                "CSE 110A": ["Error D"]
            },
            "Summer": {
                "CSE 110B": ["Error E"]
            }
        }
    }`;
*/


// This is the list containing the error message after they have been parsed through
//console.log(JSON.stringify(errorMessageList));  // TESTING
/*  CONSOLE SHOWS
    [
    "CSE 102: Missing a prerequisite CSE 101",
    "CSE 130:  Error 1  |  Error 2",
    "CSE 111:  Error A  |  Error B",
    "CSE 114A:  Error C",
    "CSE 110A:  Error D",
    "CSE 183:  Error 1  |  Error 2",
    "CSE 130:  Error A",
    "CSE 111:  Error B",
    "CSE 114A:  Error C",
    "CSE 110A:  Error D",
    "CSE 110B:  Error E",
    "CSE 138:  Error 1  |  Error 2",
    "CSE 130:  Error A",
    "CSE 111:  Error B",
    "CSE 114A:  Error C",
    "CSE 110A:  Error D",
    "CSE 110B:  Error E"
    ]
*/