// INTEGRATION:  This is the format of the JSON that will be passed to the post/fetch request
/*  Format for acadPlanObj   Instead of First, Second, etc.  it used to be 1, 2, etc.
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

/* KEEP FOR ERROR REFERENCE
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