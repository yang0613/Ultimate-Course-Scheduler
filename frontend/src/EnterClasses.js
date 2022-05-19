// Sources:
// https://reactjs.org/tutorial/tutorial.html
// https://reactjs.org/docs/forms.html
// https://reactjs.org/docs/lists-and-keys.html
// https://www.pluralsight.com/guides/display-multidimensional-array-data-in-react
// https://stackoverflow.com/questions/42238556/accessing-multidimensional-array-with-react-js
// https://dev.to/antdp425/populate-dropdown-options-in-react-1nk0  For the dropdown
// https://jsonlint.com/  Useful for validating and making JSON easier to look at

import React from 'react';
import { Grid } from 'gridjs-react';
import "gridjs/dist/theme/mermaid.css";
import {post, get} from './Script';

class EnterClasses extends React.Component {
    constructor(props) {
      super(props);
      this.state = {
        year: 1, // Current year in which to add classes to (Initially 1)
        quarter: "Fall", // Current quarter in which to add classes to (Initially Fall)
        value: "",  // Current value of input form for classes
        toRemove: "Select",  // Value to be removed (Select when nothing selected)
        classes: Array(0).fill(""),  // Array of all entered classes. Purpose is to make dealing with some parts easier.

        // INTEGRATION: Currently dummy data. Need data returned by API.
        availableClasses: ["CSE 101", "CSE 102", "CSE 103", "CSE 201", "STAT 131", "MATH 19A", "MATH 19B", "MATH 21"],
        verificationResults: [],

        // Object containing list of classes for each quarter for each year (Keep the commented version in case it's needed)
        //acadPlanObj: {"Year 1": {"Fall": ["", "", "", ""], "Winter": ["", "", "", ""], "Spring": ["", "", "", ""], "Summer": ["", "", "", ""]}, "Year 2": {"Fall": ["", "", "", ""], "Winter": ["", "", "", ""], "Spring": ["", "", "", ""], "Summer": ["", "", "", ""]}, "Year 3": {"Fall": ["", "", "", ""], "Winter": ["", "", "", ""], "Spring": ["", "", "", ""], "Summer": ["", "", "", ""]}, "Year 4": {"Fall": ["", "", "", ""], "Winter": ["", "", "", ""], "Spring": ["", "", "", ""], "Summer": ["", "", "", ""]}},
        //acadPlanObj: {"1": {"Fall": [""], "Winter": [""], "Spring": [""], "Summer": [""]}, "2": {"Fall": [""], "Winter": [""], "Spring": [""], "Summer": [""]}, "3": {"Fall": [""], "Winter": [""], "Spring": [""], "Summer": [""]}, "4": {"Fall": [""], "Winter": [""], "Spring": [""], "Summer": [""]}},

        // A 3D array containing the "rows" for each year
        //   Explanation: Each year has a set of rows contained within it
        //      First 4 is the number of years.
        //      Second 4 is the number of rows for that year (Can add more rows. Ex. Adding more classes)
        //      The 5 is the number of columns for that year (Same for each year. Cannot be changed)
        rowsForEachYear: Array(4).fill(0).map(rowsForOneYear => Array(4).fill(0).map(row => new Array(5).fill(""))),

        // All the rows for the academic table (After the "labels")
        // Build this using the set of rows from rowsForEachYear
        // The idea is to edit rowsForEachYear to make updating the full table dynamically easier (hard to edit full table directly)
        // Then build the full table again
        rows: Array(1).fill(0).map(row => new Array(5).fill("")),

        // Number of rows occupied by each year. Initially 4 for each (for the "year row")
        //   Just update by +1 at the appropriate time before using (So on first use, 0 -> 1)
        // Needed to keep track of "highest" row occupied for each year
        rowsFilled: Array(4).fill(0),

        // Number of rows filled for each quarter. (For each year)
        // Update by +1 before each use (So on first use, 0 -> 1)
        // https://stackoverflow.com/questions/50807131/how-do-i-use-array-fill-for-creating-an-array-of-objects
        // Needed to keep track of current row occupied for each quarter for each year
        rowsFilledForQtr: Array(4).fill(0).map(() => ({"Fall": 0, "Winter": 0, "Spring": 0, "Summer": 0})),

        // INTEGERATION: Replace this with whatever backend returns
        dummyReqsJSON: '["CSE 101", "CSE 102", "CSE 103", "CSE 120", "CSE 130", "CSE 116", "STAT 131"]',
        requiredList: "", // Requirements list as a string
        missingList: "",  // Missing requirements as a string
        fulfilledList: "", // Fulfilled requirements as a string
      };

      // I would have preferred to have more obvious names, but React suggests to use handle{Event} naming convention
      // FOR DRAG AND DROP: If drag and drop is implemented, I put a *** for the ones that would no longer be needed
      this.handleChange1 = this.handleChange1.bind(this); // Handles typing in a class
      this.handleChange2 = this.handleChange2.bind(this); // *** Handles changing the current quarter to put a class into
      this.handleChange3 = this.handleChange3.bind(this); // *** Handles changing the year to put a class into
      this.handleChange4 = this.handleChange4.bind(this); // *** Handles selecting the class to be removed (before confirmation of removal)
      this.handleSubmit1 = this.handleSubmit1.bind(this); // Handles clicking "Add" when entering a class
      this.handleSubmit2 = this.handleSubmit2.bind(this); // Handles clicking "Submit" when submitting all classes to be taken
      this.handleSubmit3 = this.handleSubmit3.bind(this); // *** Handles clicking "Remove" when removing a class

      // INTEGRATION:
      //   Add handleChange functions for Mhia's dropdown(and other preference options) in the sidebar
      //   Then just add it on the HTML's on{Event} attribute (Ex. onChange)
    }

    // Used to show initial table
    // https://stackoverflow.com/questions/65014512/how-to-initialize-data-before-rendering-in-react-js
    componentDidMount() {
      const rows = Array(16).fill(0).map(row => new Array(5).fill(""));
      // rows[0][0], rows[4][0], ... are the "year rows"
      rows[0][0] = "Year 1";  // First row, first column  
      rows[4][0] = "Year 2";  // Fifth row, first column
      rows[8][0] = "Year 3";  // Ninth row, first column
      rows[12][0] = "Year 4";  // Thirteenth row, first column
      this.setState({rows: rows});
    }

    // https://reactjs.org/docs/forms.html had this
    handleChange1(event) {  // Handles typing in a class name
        this.setState({value: event.target.value});
    }

    handleChange2(event) {  // Handles selecting the quarter in the dropdown
      this.setState({quarter: event.target.value});
    }

    handleChange3(event) {  // Handles selecting the year in the dropdown
      this.setState({year: event.target.value});
    }

    handleChange4(event) {  // Handles selecting the class to be removed 
      console.log("toRemove:" + event.target.value); // FOR TESTING
      this.setState({toRemove: event.target.value});
    }

    /*  Format for acadPlanObj
    {
      "1": {
        "Fall": 
          ["CSE-130", "CSE-103", "CSE-183"]
        ,
        "Winter":
          ["CSE-115A", "CSE-102", "CSE-110A"]
        ,
        "Spring":
          same format as above
        ,
        "Summer":
          same
      },
      "2": {
        "Fall": 
          same
        ,
        "Winter": 
          same
        ,
        ...Then the remaining quarters
      }
      ... Then the remaining years
    }
    */

    handleSubmit1(event) {  // Handles entering classes
      let yr = this.state.year;
      let yrNum = Number(yr);
      let qtr = this.state.quarter;
      let value = this.state.value;
      if (value === "") {
        alert("Please enter a class before submitting.");
      } else {
        const classes = this.state.classes.slice();
        // Only add a class if it hasn't been added yet
        if (!classes.includes(value)) {
          const availableClasses = this.state.availableClasses.slice();
          // Only add if included in the given list of available classes
          if (availableClasses.includes(value)) {
            classes.push(value);  // Add this class to list of all classes

            // ====================================================================================================
            // Update rowsForEachYear (Functionality explained in this.state within the constructor above
            // ====================================================================================================

            let yrIndex = yrNum - 1;  // yr - 1: Ex. Year 1, yrNum = 1, so correct index would be 0

            let column = 1;  // Which column of current row to add the class in
            switch(qtr) {
              case "Fall":
                column = 1;
                break;
              case "Winter":
                column = 2;
                break;
              case "Spring":
                column = 3;
                break;
              case "Summer":
                column = 4;
                break;
              default:
                column = 1;
                break;
            }

            //  Explanation: Each year has a set of rows it occupies
            //  The comments below are included to avoid having to look up all the way above for how each state works
            //    First 4 is the number of years. 
            //    Second 4 is the number of rows for that year (Can add more rows. Ex. Adding more classes)
            //    The 5 is the number of columns for that year (Same for each year. Cannot be changed)
            // rowsForEachYear: Array(4).fill(0).map(rowsForOneYear => Array(4).fill(0).map(row => new Array(5).fill("")))
            // rowsFilled: Array(4).fill(0)  // Update by +1 before each use (So on first use, 0 -> 1)
            // rowsFilledForQtr: Array(4).fill(0).map(() => ({"Fall": 0, "Winter": 0, "Spring": 0, "Summer": 0}))
            let rowsForEachYear = this.state.rowsForEachYear.slice();
            let rowsFilled = this.state.rowsFilled.slice();
            let rowsFilledForQtr = this.state.rowsFilledForQtr.slice();

            // Need to keep track of "highest" row occupied for each year (curRow)
            //   Also need to keep track of current row occupied for each quarter for each year
            rowsFilledForQtr[yrIndex][qtr] += 1; // As mentioned above, increment before each use
            let curRowForQtr = rowsFilledForQtr[yrIndex][qtr];  // The row in which to enter the class for the current year and quarter
            if (curRowForQtr > rowsFilled[yrIndex]) {  // If another row is needed (See below for the add)
              rowsFilled[yrIndex] += 1;  // As mentioned previously, increment at the appropriate time
            }
            let curRow = rowsFilled[yrIndex]; // Current row to be filled for current year
            if (curRow >= rowsForEachYear[yrIndex].length) { // If another row is needed
              rowsForEachYear[yrIndex].push(["","","","",""]); // Add a row with 5 columns
            }
            // [year][row][column]
            rowsForEachYear[yrIndex][curRowForQtr][column] = value;  // Add the class to the current row for the selected quarter for the selected year

            // ================================================================================================
            // Build the academic plan table to be shown
            // ================================================================================================

            let rows = this.buildRows(rowsForEachYear);

            value = "";  // For next input
            //this.setState({value: value, classes: classes, classCount: classCount, acadPlanObj:acadPlanObj, rowsFilled: rowsFilled, rowsFilledForQtr: rowsFilledForQtr, rowsForEachYear: rowsForEachYear, rows: rows});
            this.setState({value: value, classes: classes, rowsFilled: rowsFilled, rowsFilledForQtr: rowsFilledForQtr, rowsForEachYear: rowsForEachYear, rows: rows});
            
          } else {
            alert("Please select from the list of given classes.");
            value = "";  // For next input
            this.setState({value: value});
          }
        } else {
          alert("This class has already been added.");
          value = "";  // For next input
          this.setState({value: value});
        }
      }

      // INTEGRATION: Wenhao mentioned that there could be a POST request after entering a class
      event.preventDefault();


    }

    // Build the rows for the academic plan table
    buildRows(rowsForEachYear) {
      let rows = Array(0).fill(0);
      for(let i = 0; i < rowsForEachYear.length; i++) {  // Go through each year
        let year = i + 1;
        rowsForEachYear[i][0][0] = "Year " + year;  // Build the year row (Just build it every time, even if already there)
        for(let j = 0; j < rowsForEachYear[i].length; j++) {  // Go through each row for this year
          rows.push(rowsForEachYear[i][j]);  // Here, i is for year and j is for row. Push each row in the the complete array of rows
        }
      }

      return rows;  // rows state is changed in the function that calls buildRows
    }

    handleSubmit2(event) {  // Handles submitting the list of classes (Clicking Verify)

      // INTEGRATION: Create the object that will be passed to the backend
      let rowsForEachYear = this.state.rowsForEachYear.slice();
      //let acadPlanObj = {"1": {"Fall": [""], "Winter": [""], "Spring": [""], "Summer": [""]}, "2": {"Fall": [""], "Winter": [""], "Spring": [""], "Summer": [""]}, "3": {"Fall": [""], "Winter": [""], "Spring": [""], "Summer": [""]}, "4": {"Fall": [""], "Winter": [""], "Spring": [""], "Summer": [""]}};
      //let acadPlanObj = {"1": {"Fall": [], "Winter": [], "Spring": [], "Summer": []}, "2": {"Fall": [], "Winter": [], "Spring": [], "Summer": []}, "3": {"Fall": [], "Winter": [], "Spring": [], "Summer": []}, "4": {"Fall": [], "Winter": [], "Spring": [], "Summer": []}};
      let acadPlanObj = {"first": {"Fall": [], "Winter": [], "Spring": [], "Summer": []}, "second": {"Fall": [], "Winter": [], "Spring": [], "Summer": []}, "third": {"Fall": [], "Winter": [], "Spring": [], "Summer": []}, "fourth": {"Fall": [], "Winter": [], "Spring": [], "Summer": []}};
      for (let k = 0; k < rowsForEachYear.length; k++) {  // Iterate through each year
        //let yr = String(k + 1);  // Will be 1 to 4
        let yr = "";
        switch(k) {
          case 0:
            yr = "first";
            break;
          case 1:
            yr = "second";
            break;
          case 2:
            yr = "third";
            break;
          case 3:
            yr = "fourth";
            break;
          default:
            yr = "first";
        }

        for (let i = 0; i < rowsForEachYear[k].length; i++) {  // Iterate through each row for each year
          for (let j = 1; j < rowsForEachYear[k][i].length; j++) {  // Iterate through each column(qtr) for current row
            let toInsert = rowsForEachYear[k][i][j];
            if (toInsert === "Year 1" || toInsert === "Year 2" || toInsert === "Year 3" || toInsert === "Year 4" || toInsert === "") {
              continue;
            }

            let qtr = "";
            switch(j) {
              case 1:
                qtr = "Fall";
                break;
              case 2:
                qtr = "Winter";
                break;
              case 3:
                qtr = "Spring";
                break;
              case 4:
                qtr = "Summer";
                break;
              default:
                qtr = "Fall";
            }
            acadPlanObj[yr][qtr].push(toInsert);
          }
        }
      }

      //console.log(acadPlanObj);
      let acadPlanObjJSON = JSON.stringify(acadPlanObj);
      console.log(acadPlanObjJSON);
  
      // UPDATE FOR SPRINT 4: need to create another object that contains preferences
      // Then combine acadPlanObj with this new one

      // INTEGRATION: (IMPORTANT):
      //   How is data submitted?     See file that Shing showed
      //   Put this data in resultJSON

      /*

      {
      	"1": {
      		"Fall": {
      			"CSE 102": ["Missing a prerequisite CSE 101"],
      			"CSE 130": ["Error 1", "Error 2"]
      		},
      		"Winter": {
      			"CSE 111": ["Error A", "Error B"]
      		},
      		"Spring": {
      			"CSE 114A": ["Error C"],
      			"CSE 110A": ["Error D"]
      		},
      		"Summer": {}
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
      	"3": {
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
      	},
      	"4": {
      		"Fall": {},
      		"Winter": {},
      		"Spring": {},
      		"Summer": {}
      	}
      }

      */

      // Get JSON Data returned by backend. See format above
      // let result = APICall ...
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

      let errorMessageList = [];

      // Iterate through the resulting object to get the error messages
      let resultObj = JSON.parse(resultJSON);
      for (let year of Object.keys(resultObj)) {
        //if (year) {  // If there's an error message for that year  NOT NEEDED, wouldn't be traversed in the first place
        let yearObj = resultObj[year];
        for (let quarter of Object.keys(yearObj)) {
          let quarterObj = yearObj[quarter];
          for (let thisClass of Object.keys(quarterObj)) {
            let classObj = quarterObj[thisClass];
            let errorMessage = thisClass + ":\xa0\xa0";
            for (let i = 0; i < classObj.length; i++) {
              // https://stackoverflow.com/questions/5237989/how-is-a-non-breaking-space-represented-in-a-javascript-string
              errorMessage += classObj[i] + "\xa0\xa0|\xa0\xa0";  // TEMPORARY
            }
            if (classObj.length >= 1) {  // If this class actually has error messages
              errorMessage = errorMessage.slice(0, -5);
              errorMessageList.push(errorMessage);
            }
          }
        }
      }

      console.log(JSON.stringify(errorMessageList));  // TESTING
      /*  CONSOLE SHOWS
        ["CSE 102: Missing a prerequisite CSE 101",
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
        "CSE 110B:  Error E"]
      */

      const verificationResults = errorMessageList.map((string) =>
        <li>{string}</li>
      );
        
      // INTEGRATION (FOR SPRINT4 GENERATING):
      // For generating, create a seperate handleSubmit
      // Then just update rowsForEachYear by parsing the data returned by backend

    
      // ================================================================================================
          // INTEGRATION 
      // ================================================================================================
      //ADDED -- frontend fetch call - success/error message 
      //check for error from Backend - 404 //alert within fetch! 
      const response = get(verificationResults); //changed from get to post, check with group/TA
      response.then((res)=>{
        console.log(res, "Hi this was a success!");
        console.log(JSON.stringify(res), "sdfdsfdf");
        console.log(res.json());
      }).catch((err)=>{
        console.log(err, "ERROR Verfication Failed");
      })
      // ================================================================================================


      // OLD, keep for reference
      // INTEGRATION: Probably just need a state for the result
      //this.setState({requiredList: requiredList, missingList: missingList, fulfilledList: fulfilledList});
      this.setState({verificationResults: verificationResults});

      alert("Use API calls later, then return result. For now, look at console."); // Temporary. REMOVE LATER
      event.preventDefault(); // Without this, the page re-renders and all states are lost
      // INTEGRATION: Maybe keep the event.preventDefault() above and just use the API calls to get the needed data
    }

    handleSubmit3(event) {  // For class removal from the list of entered classes
      let toRemove = this.state.toRemove;

      if (!(toRemove === "Select")) {  // If a class to be removed was selected
        console.log("toRemove: " + toRemove);  // TESTING
        let classes = this.state.classes.slice();

        // Remove all instances from "classes"
        // UPDATE: Since duplicates are no longer allowed when entering, it's now unnecessary to look through whole list
        let x = 0;
        while (x < classes.length) {
          if (classes[x] === toRemove) {
            classes.splice(x, 1);
          } else {
            x++;
          }
        }
        console.log("classes(after remove): " + classes.toString());  // TESTING

        // Remove it in rowsForEachYear
        //   Need to update the various rowsFilled variables.
        let rowsForEachYear = this.state.rowsForEachYear.slice();
        let rowsFilled = this.state.rowsFilled.slice();  // For each year
        let rowsFilledForQtr = this.state.rowsFilledForQtr.slice();  // For each quarter for each year

        // First, find the class to be removed.
        // Let k = year, i = row, j = column
        for (let k = 0; k < rowsForEachYear.length; k++) {  // Iterate through each year
          // Iterate through each row for each year
          for (let i = 0; i < rowsForEachYear[k].length; i++) {
            // Iterate through each column(qtr) for current row
            for (let j = 0; j < rowsForEachYear[k][i].length; j++) {
              if (rowsForEachYear[k][i][j] === toRemove) {
                rowsForEachYear[k][i][j] = "";  // Delete by turning into an empty string

                // Shift elements back if needed to (in other words, upward if looking at the table)
                for (let a = i + 1; a < rowsForEachYear[k].length; a++) {  // Start at the one after the deleted one
                  rowsForEachYear[k][a - 1][j] = rowsForEachYear[k][a][j];
                  rowsForEachYear[k][a][j] = "";
                }

                let qtr = "";
                switch(j) {
                  case 0:
                    qtr = "";
                    break;
                  case 1:
                    qtr = "Fall";
                    break;
                  case 2:
                    qtr = "Winter";
                    break;
                  case 3:
                    qtr = "Spring";
                    break;
                  case 4:
                    qtr = "Summer";
                    break;
                  default:
                    qtr = "";
                    break;
                }

                rowsFilledForQtr[k][qtr] -= 1; // Decrement rows occupied for current quarter
                // Note: When adding another class (in handleSubmit1):
                //   rowsFilledForQtr is used as an index for the current row to fill when pushing into rowsForEachYear 
                //   rowsFilled is used to determine if an extra row needs to be added
                // So, everything should work properly as long as the shifting above is done properly

                // Could edit rowsFilled if I want to shrink the table when appropriate, but not necessary

                break;  // Nothing else to remove
              }
            }
          }
        }

        // Build the rows for the academic plan table
        let rows = this.buildRows(rowsForEachYear);

        toRemove = "Select";  // Reset toRemove for next possible removal

        this.setState({classes: classes, toRemove: toRemove, rowsForEachYear: rowsForEachYear, rowsFilled: rowsFilled, rowsFilledForQtr: rowsFilledForQtr, rows: rows});
      } else {
        alert("Please select a class to remove.");
      }

      event.preventDefault(); // Important
    }

    render() {

      return (
        <div className="container1">
          <form onSubmit={this.handleSubmit1}>
            <label>Enter Course:&nbsp;</label>
            <input list="availableClasses" name="classstr" value={this.state.value} onChange={this.handleChange1} />
            <datalist id="availableClasses">
              <option value=""></option>
              {this.state.availableClasses.map((theClass) => <option value={theClass.value}>{theClass}</option>)}
            </datalist>
            &nbsp;
            <input type="submit" value="Add" />

            &emsp;
            <label>Quarter:&nbsp;</label>
            <select className="quarter" onChange={this.handleChange2}>
              <option value="Fall">Fall</option>
              <option value="Winter">Winter</option>
              <option value="Spring">Spring</option>
              <option value="Summer">Summer</option>
            </select>
            &emsp;
            <label>Year:&nbsp;</label>
            <select className="quarter" onChange={this.handleChange3}>
                <option value="1">Year 1</option>
                <option value="2">Year 2</option>
                <option value="3">Year 3</option>
                <option value="4">Year 4</option>
            </select>
          </form>

          {
            // For removing a class. "classes" is primarily used for this
            // https://stackoverflow.com/questions/21733847/react-jsx-selecting-selected-on-selected-select-option
          }
          <form class = "m-0" onSubmit={this.handleSubmit3}>
            <label>Remove Course:&nbsp;</label>
            <select className="toRemove" value={this.state.toRemove} onChange={this.handleChange4}>
              <option value="Select">Select</option>
              {this.state.classes.map((theClass) => <option value={theClass.value}>{theClass}</option>)}
            </select>
            &nbsp;
            <input type="submit" value="Remove" />
          </form>
          <br></br>

          {
            // The academic plan table
          }
          <Grid
            data={this.state.rows}
            columns={["Year", "Fall", "Winter", "Spring", "Summer"]}
            width="100%"
          />

          {
            // Submit the academic plan table (As a JSON, with each class associated with a quarter and a year)
          }
          <form onSubmit={this.handleSubmit2}>
              <input class="button is-info is-rounded" type="submit" value="Verify" />
          </form>
          {
            // INTEGRATION: Edit this part later so it takes in data returned by the backend
                // check in how to implement this! 
                // post/get call? not sure! - same implementation as above but for data! 
          }      
          <br></br>
          <h2>Verification Results:</h2>
          <ul>{this.state.verificationResults}</ul>

        </div>
      );
    }
}

export default EnterClasses;
