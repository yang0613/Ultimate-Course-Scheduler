// Sources:
// https://reactjs.org/tutorial/tutorial.html
// https://reactjs.org/docs/forms.html
// https://reactjs.org/docs/lists-and-keys.html
// https://www.pluralsight.com/guides/display-multidimensional-array-data-in-react
// https://stackoverflow.com/questions/42238556/accessing-multidimensional-array-with-react-js
// https://dev.to/antdp425/populate-dropdown-options-in-react-1nk0  For the dropdown

// NOTE: Research proper way to update array values in React

import React from 'react';
import { Grid } from 'gridjs-react';
import "gridjs/dist/theme/mermaid.css";

class EnterClasses extends React.Component {
    constructor(props) {
      super(props);
      this.state = {
        year: 1, // Current year in which to add classes to (Initially 1)
        quarter: "Fall", // Current quarter in which to add classes to (Initially Fall)
        value: "",  // Current value of input form for classes
        toRemove: "Select",
        //classCount: 0, 

        classes: Array(0).fill(""),  // Array of all entered classes. Purpose is to make dealing with some parts easier.
        //classes: new Set(),

        // Object containing list of classes for each quarter for each year
        // IMPORTANT: Might be better to build this from rows(see below) since class removal would be complicated
        //acadPlanObj: {"Year 1": {"Fall": ["", "", "", ""], "Winter": ["", "", "", ""], "Spring": ["", "", "", ""], "Summer": ["", "", "", ""]}, "Year 2": {"Fall": ["", "", "", ""], "Winter": ["", "", "", ""], "Spring": ["", "", "", ""], "Summer": ["", "", "", ""]}, "Year 3": {"Fall": ["", "", "", ""], "Winter": ["", "", "", ""], "Spring": ["", "", "", ""], "Summer": ["", "", "", ""]}, "Year 4": {"Fall": ["", "", "", ""], "Winter": ["", "", "", ""], "Spring": ["", "", "", ""], "Summer": ["", "", "", ""]}},
        acadPlanObj: {"1": {"Fall": [""], "Winter": [""], "Spring": [""], "Summer": [""]}, "2": {"Fall": [""], "Winter": [""], "Spring": [""], "Summer": [""]}, "3": {"Fall": [""], "Winter": [""], "Spring": [""], "Summer": [""]}, "4": {"Fall": [""], "Winter": [""], "Spring": [""], "Summer": [""]}},

        // A 3D array containing the "rows" for each year
        //   Explanation: Each year has a set of rows contained within it
        //      First 4 is the number of years.  (Can add more years if needed...DO LATER)
        //      Second 4 is the number of rows for that year (Can add more rows. Ex. Adding more classes)
        //      The 5 is the number of columns for that year (Same for each year. Cannot be changed)
        rowsForEachYear: Array(4).fill(0).map(rowsForOneYear => Array(4).fill(0).map(row => new Array(5).fill(""))),
        rows: Array(1).fill(0).map(row => new Array(5).fill("")),  // Build this with each of the "rows" for each year above
        //rows: Array(16).fill(0).map(row => new Array(5).fill("")),

        // Number of rows filled for each year. Initially 1 for each (for the "year row")
        //   Just ppdate by +1 at the appropriate time before using (So on first use, 0 -> 1)
        rowsFilled: Array(4).fill(0),  // Needed to keep track of "highest" row occupied for each year

        // Number of rows filled for each quarter. (For each year)
        // Update by +1 before each use (So on first use, 0 -> 1)
        // https://stackoverflow.com/questions/50807131/how-do-i-use-array-fill-for-creating-an-array-of-objects
        //rowsFilledForQtr: Array(4).fill({"Fall": 0, "Winter": 0, "Spring": 0, "Summer": 0}),  // Needed to keep track of current row occupied for each quarter for each year
        rowsFilledForQtr: Array(4).fill(0).map(() => ({"Fall": 0, "Winter": 0, "Spring": 0, "Summer": 0})),

        dummyReqsJSON: '["CSE 101", "CSE 102", "CSE 103", "CSE 120", "CSE 130", "CSE 116", "STAT 131"]',
        requiredList: "", // Requirements list as a string
        missingList: "",  // Missing requirements as a string
        fulfilledList: "", // Fulfilled requirements as a string
      };

      this.handleChange1 = this.handleChange1.bind(this); // Handles typing in a class
      this.handleChange2 = this.handleChange2.bind(this); // Handles changing the current quarter to put a class into
      this.handleChange3 = this.handleChange3.bind(this); // Handles changing the year to put a class into
      this.handleChange4 = this.handleChange4.bind(this); // Handles selecting the class to be removed (before confirmation of removal)
      //this.handleLoad1 = this.handleLoad1.bind(this);  // DO LATER: Handles loading the initial table so it properly shows
      this.handleSubmit1 = this.handleSubmit1.bind(this);  // Handles clicking "Add" when entering a class
      this.handleSubmit2 = this.handleSubmit2.bind(this);  // Handles clicking "Submit" when submitting all classes to be taken
      this.handleSubmit3 = this.handleSubmit3.bind(this);  // Handles clicking "Remove" when removing a class
    }

    // https://stackoverflow.com/questions/65014512/how-to-initialize-data-before-rendering-in-react-js
    componentDidMount() {
      const rows = Array(16).fill(0).map(row => new Array(5).fill(""));
      // Build the "year rows"
      rows[0][0] = "Year 1";  // First row, first column  
      rows[4][0] = "Year 2";  // Fifth row, first column
      rows[8][0] = "Year 3";  // Ninth row, first column
      rows[12][0] = "Year 4";  // Thirteenth row, first column
      this.setState({rows: rows});
    }

    handleChange1(event) {  // https://reactjs.org/docs/forms.html had this
      this.setState({value: event.target.value});
    }

    handleChange2(event) {
      this.setState({quarter: event.target.value});
    }

    handleChange3(event) {
      this.setState({year: event.target.value});
    }

    handleChange4(event) {
      console.log("toRemove:" + event.target.value); // TESTING
      this.setState({toRemove: event.target.value});
    }

    /*
    handleLoad1(event) {  // During initial loading (Just to inialize year rows)
      let rows = this.state.rows;
      rows[0][0] = "1";
      rows[4][0] = "2";
      rows[8][0] = "3";
      rows[12][0] = "4";

      this.setState({rows: rows});
    }
    */

    /*  Format for acadPlanObj  (Change Year 1 to the person's first year Ex. 2022)
    {
      "1": {
        "Fall": {
          ["CSE-130", "CSE-103", "CSE-183"]
        },
        "Winter": {
          ["CSE-115A", "CSE-102", "CSE-110A"]
        },
        "Spring": {
          same format as above
        },
        "Summer": {
          same
        }
      },
      "2": {
        "Fall": {
          same
        },
        "Winter": {
          same
        }
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
       
          classes.push(value);  // Add this class to list of all classes

          //let classCount = this.state.classCount;
          //console.log("classCount(before add):" + String(classCount)); // TESTING
          //classCount++;  // Increase class entered count (Used as a safety check when removing classes)
          //console.log("classCount(after add):" + String(classCount));  // TESTING

          // ============================================ PART 1 ====================================================
          // This first part handles adding the class name to the object (This part is only needed for when passing to backend)

          // IMPORTANT: Might be better to build this from rows(see below) since class removal would be complicated
          const acadPlanObj = this.state.acadPlanObj;
          acadPlanObj[yr][qtr].push(value);
          //this.setState({acadPlanObj: acadPlanObj});

          // ============================================ PART 2 ====================================================
          // This second part handles updating the row in which the class is to be added
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

          //  Explanation: Each year has a set of rows contained within it
          //    First 4 is the number of years.  (Can add more years if needed...DO LATER)
          //    Second 4 is the number of rows for that year (Can add more rows. Ex. Adding more classes)
          //    The 5 is the number of columns for that year (Same for each year. Cannot be changed)
          // rowsForEachYear: Array(4).fill(0).map(rowsForOneYear => Array(4).fill(0).map(row => new Array(5).fill("")))
          // rowsFilled: Array(4).fill(0),  // Update by +1 before each use (So on first use, 0 -> 1)
          // rowsFilledForQtr: Array(4).fill({"Fall": 0, "Winter": 0, "Spring": 0, "Summer": 0})
          let rowsForEachYear = this.state.rowsForEachYear.slice();
          let rowsFilled = this.state.rowsFilled.slice();
          let rowsFilledForQtr = this.state.rowsFilledForQtr.slice();

          // Need to keep track of "highest" row occupied for each year (curRow)
          // Also need to keep track of current row occupied for each quarter for each year

          rowsFilledForQtr[yrIndex][qtr] += 1; // As mentioned above, increment before each use
          let curRowForQtr = rowsFilledForQtr[yrIndex][qtr];
          if (curRowForQtr > rowsFilled[yrIndex]) {
            rowsFilled[yrIndex] += 1;  // As mentioned previously, increment at the appropriate time
          }
          let curRow = rowsFilled[yrIndex];
          if (curRow >= rowsForEachYear[yrIndex].length) {
            rowsForEachYear[yrIndex].push(["","","","",""]); // Add a row with 5 columns
          }
          // [year][row][column]
          rowsForEachYear[yrIndex][curRowForQtr][column] = value;  // Add the class to the current row for the quarter

          //this.setState({rowsFilled: rowsFilled, rowsForEachYear: rowsForEachYear});

          // ============================================ PART 3 ====================================================
          // This third part handles rebuilding the entire table

          /*
          let rows = Array(0).fill(0);
          for(let i = 0; i < rowsForEachYear.length; i++) {  // Go through each year
            let year = i + 1;
            rowsForEachYear[i][0][0] = "Year " + year;  // Build the year row (Just build it every time, even if already there)
            for(let j = 0; j < rowsForEachYear[i].length; j++) {  // Go through each row for this year
              rows.push(rowsForEachYear[i][j]);  // Here, i is for year and j is for row. Push each row in the the complete array of rows
            }
          }
          */
          let rows = this.buildRows(rowsForEachYear);

          value = "";  // For next input

          //this.setState({value: value, classes: classes, classCount: classCount, acadPlanObj:acadPlanObj, rowsFilled: rowsFilled, rowsFilledForQtr: rowsFilledForQtr, rowsForEachYear: rowsForEachYear, rows: rows});
          this.setState({value: value, classes: classes, acadPlanObj:acadPlanObj, rowsFilled: rowsFilled, rowsFilledForQtr: rowsFilledForQtr, rowsForEachYear: rowsForEachYear, rows: rows});
        } else {
          alert("This class has already been added.");
          value = "";  // For next input
          this.setState({value: value});
        }
      }

      event.preventDefault();  // Important
    }

    buildRows(rowsForEachYear) {  // Build the rows for the academic plan table
      let rows = Array(0).fill(0);
      for(let i = 0; i < rowsForEachYear.length; i++) {  // Go through each year
        let year = i + 1;
        rowsForEachYear[i][0][0] = "Year " + year;  // Build the year row (Just build it every time, even if already there)
        for(let j = 0; j < rowsForEachYear[i].length; j++) {  // Go through each row for this year
          rows.push(rowsForEachYear[i][j]);  // Here, i is for year and j is for row. Push each row in the the complete array of rows
        }
      }

      return rows;
    }

    handleSubmit2(event) {  // Handles submitting the list of classes
      const dummyReqsJSON = this.state.dummyReqsJSON;
      const dummyReqsArr = JSON.parse(dummyReqsJSON);
      const classes = this.state.classes.slice();
      const missing = [];
      const fulfilled = [];
      let classVal = "";

      // ================================================================================================
      // NOTE: This enclosed part is only here temporarily.
      // Later, the backend should return which classes are missing and which ones have been fulfilled.

      for(let i = 0; i < classes.length; i++) {  // Check which requirements have been fulfilled
        classVal = classes[i];
        if (dummyReqsArr.includes(classVal)) {
          fulfilled.push(classVal);
        }
      }

      // Check which requirements are missing
      // Iterate through list of requirements, comparing to the list of requirements fulfilled
      for(let i = 0; i < dummyReqsArr.length; i++) {
        classVal = dummyReqsArr[i];
        if (!fulfilled.includes(classVal)) {
          missing.push(classVal);
        }
      }
      // ================================================================================================

      let requiredList = "";
      for (let i = 0; i < dummyReqsArr.length; i ++) {
        requiredList += dummyReqsArr[i] + ", ";
      }
      requiredList = requiredList.slice(0, -2);

      let missingList = "";
      for (let i = 0; i < missing.length; i ++) {
        missingList += missing[i] + ", ";
      }
      missingList = missingList.slice(0, -2);

      let fulfilledList = "";
      for (let i = 0; i < fulfilled.length; i ++) {
        fulfilledList += fulfilled[i] + ", ";
      }
      fulfilledList = fulfilledList.slice(0, -2);

      this.setState({requiredList: requiredList, missingList: missingList, fulfilledList: fulfilledList});

      event.preventDefault();  // Just for now. Actually want to submit once able to connect to backend
    }

    handleSubmit3(event) {  // For class removal.  NOTE: This removes all instances of a class
      //let classCount = this.state.classCount;
      let toRemove = this.state.toRemove;

      //if (classCount >= 1) {  // If there's a class to be removed in the first place
      if (!(toRemove === "Select")) {  // If a class to be removed was selected
        //console.log("classCount(before decrement): " + String(classCount));  // TESTING
        //classCount--;
        //console.log("classCount(after decrement): " + String(classCount));  // TESTING

        //let toRemove = this.state.toRemove;
        console.log("toRemove: " + toRemove);  // TESTING
        let classes = this.state.classes.slice();

        // Remove from "classes"
        // Since duplicates are no longer allowed when entering, it's now unnecessary to look through whole list
        console.log("classes(before remove): " + classes.toString());  // TESTING
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
        /*
          rowsForEachYear
          rowsFilled (for each year)
          rowsFilledForQtr (for each quarter for each year)
        */
        let rowsForEachYear = this.state.rowsForEachYear.slice();
        let rowsFilled = this.state.rowsFilled.slice();
        let rowsFilledForQtr = this.state.rowsFilledForQtr.slice();

        /*
          Will need to know:
          qtr = column
          year = yrIndex
          theClassName = value
        */

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

                // Could also edit rowsFilled, but not necessary

                break;  // Nothing else to remove
              }
            }
          }
        }

        /* //  NOT NEEDED, Keep for reference
        // i for rows, j for columns
        // Go through each column of each row to remove instance of the class to be removed
        for (let i = 0; i < rows.length; i++) {
          for (let j = 0; j < rows[i].length; j++) {
            if (rows[i][j] === toRemove) {
              console.log("i: " + String(i) + "    j: " + String(j) + "    rows[i][j]: " + rows[i][j]);  // TESTING
              rows[i][j] = ""; // Remove by making it an empty string
            }
          }
        }
        */

        // Build the rows for the academic plan table
        let rows = this.buildRows(rowsForEachYear);

        toRemove = "Select";  // Reset toRemove for next possible removal

        // Update this to include rowsForEachYear and the various rowsFilled variables
        //this.setState({classes: classes, classCount: classCount, toRemove: toRemove, rows: rows});
        //this.setState({classes: classes, toRemove: toRemove, rows: rows});
        this.setState({classes: classes, toRemove: toRemove, rowsForEachYear: rowsForEachYear, rowsFilled: rowsFilled, rowsFilledForQtr: rowsFilledForQtr, rows: rows});
      } else {
        alert("Please select a class to remove.");
      }

      // Don't do anything if there are no classes in the first place

      event.preventDefault(); // Important
    }

    render() {
      // Dummy json to check if missing requirements handler works
      //   CSE 12, CSE 16, CSE 20, CSE 30, CSE 13S, MATH 19A, MATH 19B, MATH 21, MATH 23A, ECE 30
      //   CSE 101, CSE 102, CSE 103, CSE 120, CSE 130, CSE 116, STAT 131, CSE 115A, CSE 183

      return (
        <div className="container1">
          <form onSubmit={this.handleSubmit1}>
            <label>Enter a class:&nbsp;</label>
            <input type="text" value={this.state.value} onChange={this.handleChange1} />
            &nbsp;
            <input type="submit" value="Add" />
            &emsp;
            <label>Year:&nbsp;</label>
            <select className="quarter" onChange={this.handleChange3}>
                <option value="1">Year 1</option>
                <option value="2">Year 2</option>
                <option value="3">Year 3</option>
                <option value="4">Year 4</option>
            </select>
            &emsp;
            <label>Quarter:&nbsp;</label>
            <select className="quarter" onChange={this.handleChange2}>
              <option value="Fall">Fall</option>
              <option value="Winter">Winter</option>
              <option value="Spring">Spring</option>
              <option value="Summer">Summer</option>
            </select>
          </form>

          {
            // For removing a class. "classes" is primarily used for this
            // https://stackoverflow.com/questions/21733847/react-jsx-selecting-selected-on-selected-select-option
          }
          <form onSubmit={this.handleSubmit3}>
            <label>Remove a class:&nbsp;</label>
            <select className="toRemove" value={this.state.toRemove} onChange={this.handleChange4}>
              <option value="Select">Select</option>
              {this.state.classes.map((theClass) => <option value={theClass.value}>{theClass}</option>)}
            </select>
            &nbsp;
            <input type="submit" value="Remove" />
          </form>

          {
            // The academic plan table
          }
          <Grid
            data={this.state.rows}
            columns={["Year", "Fall", "Winter", "Spring", "Summer"]}
            width="50%"
          />

          {
            // Submit the academic plan table (As a JSON, with each class associated with a quarter and a year)
          }
          <form onSubmit={this.handleSubmit2}>
            <input type="submit" value="Submit" />
          </form>


          {
            // Edit this part later so it takes in data returned by the backend
          }      
          <h2>Results:</h2>
          <p><b>Requirements: </b>{this.state.requiredList}</p>
          <p><b>Missing: </b>{this.state.missingList}</p>
          <p><b>Fulfilled:</b>{this.state.fulfilledList}</p>

        </div>
      );
    }
}

export default EnterClasses;



