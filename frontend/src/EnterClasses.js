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
        toRemove: "",
        classCount: 0,

        classes: Array(0).fill(""),  // Array of all entered classes. Purpose is to make dealing with some parts easier.

        // Object containing list of classes for each quarter for each year
        // IMPORTANT: Might be better to build this from rows(see below) since class removal would be complicated
        //acadPlanObj: {"Year 1": {"Fall": ["", "", "", ""], "Winter": ["", "", "", ""], "Spring": ["", "", "", ""], "Summer": ["", "", "", ""]}, "Year 2": {"Fall": ["", "", "", ""], "Winter": ["", "", "", ""], "Spring": ["", "", "", ""], "Summer": ["", "", "", ""]}, "Year 3": {"Fall": ["", "", "", ""], "Winter": ["", "", "", ""], "Spring": ["", "", "", ""], "Summer": ["", "", "", ""]}, "Year 4": {"Fall": ["", "", "", ""], "Winter": ["", "", "", ""], "Spring": ["", "", "", ""], "Summer": ["", "", "", ""]}},
        acadPlanObj: {"1": {"Fall": [""], "Winter": [""], "Spring": [""], "Summer": [""]}, "2": {"Fall": [""], "Winter": [""], "Spring": [""], "Summer": [""]}, "3": {"Fall": [""], "Winter": [""], "Spring": [""], "Summer": [""]}, "4": {"Fall": [""], "Winter": [""], "Spring": [""], "Summer": [""]}},

        //rowsY1: Array(4).fill(0).map(row => new Array(5).fill("")),  // 4 rows for each (3 for the classes, 1 for the "year row"), 5 columns each(4 for the quarters, 1 for "year column")
        //rowsY2: Array(4).fill(0).map(row => new Array(5).fill("")),
        // ...
        // NOTE: Use the 3D array below

        // A 3D array containing the "rows" for each year
        //   Explanation: Each year has a set of rows contained within it
        //      First 4 is the number of years.  (Can add more years if needed...DO LATER)
        //      Second 4 is the number of rows for that year (Can add more rows. Ex. Adding more classes)
        //      The 5 is the number of columns for that year (Same for each year. Cannot be changed)
        rowsForEachYear: Array(4).fill(0).map(rowsForOneYear => Array(4).fill(0).map(row => new Array(5).fill(""))),
        rows: Array(1).fill(0).map(row => new Array(5).fill("")),  // Build this with each of the "rows" for each year above

        // Number of rows filled for each year. Initially 1 for each (for the "year row")
        rowsFilled: Array(4).fill(0),  // Needed to keep track of "highest" row occupied for each year

        // Update by +1 before each use (So on first use, 0 -> 1)
        // https://stackoverflow.com/questions/50807131/how-do-i-use-array-fill-for-creating-an-array-of-objects
        //rowsFilledForQtr: Array(4).fill({"Fall": 0, "Winter": 0, "Spring": 0, "Summer": 0}),  // Needed to keep track of current row occupied for each quarter for each year
        rowsFilledForQtr: Array(4).fill(0).map(() => ({"Fall": 0, "Winter": 0, "Spring": 0, "Summer": 0})),

        dummyReqsJSON: '["CSE 101", "CSE 102", "CSE 103", "CSE 120", "CSE 130", "CSE 116", "STAT 131"]',
        requiredList: "", // Requirements list as a string
        missingList: "",  // Missing requirements as a string
        fulfilledList: "", // Fulfilled requirements as a string
      };

      this.handleChange1 = this.handleChange1.bind(this);
      this.handleChange2 = this.handleChange2.bind(this);
      this.handleChange3 = this.handleChange3.bind(this);
      this.handleChange4 = this.handleChange4.bind(this);
      //this.handleLoad1 = this.handleLoad1.bind(this);
      this.handleSubmit1 = this.handleSubmit1.bind(this);
      this.handleSubmit2 = this.handleSubmit2.bind(this);
      this.handleSubmit3 = this.handleSubmit3.bind(this);
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
      console.log("toRemove:" + event.target.value);
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

    /*  Format for acadPlanObj
    {
      "Year 1": {
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
      "Year 2": {
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
        classes.push(value);  // Add this class to list of all classes

        let classCount = this.state.classCount;
        console.log("classCount(before add):" + String(classCount));
        classCount++;  // Increase class entered count (Used as a safety check when removing classes)
        console.log("classCount(after add):" + String(classCount));

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
        //rowsForEachYear: Array(4).fill(0).map(rowsForOneYear => Array(4).fill(0).map(row => new Array(5).fill("")))
        //rowsFilled: Array(4).fill(0),  // Update by +1 before each use (So on first use, 0 -> 1)
        //rowsFilledForQtr: Array(4).fill({"Fall": 0, "Winter": 0, "Spring": 0, "Summer": 0})
        let rowsForEachYear = this.state.rowsForEachYear.slice();
        let rowsFilled = this.state.rowsFilled.slice();
        let rowsFilledForQtr = this.state.rowsFilledForQtr.slice();

        // Need to keep track of "highest" row occupied for each year (curRow)
        // Also need to keep track of current row occupied for each quarter for each year

        rowsFilledForQtr[yrIndex][qtr] += 1; // As mentioned above, increment before each use
        let curRowForQtr = rowsFilledForQtr[yrIndex][qtr];
        if (curRowForQtr > rowsFilled[yrIndex]) {
          rowsFilled[yrIndex] += 1;
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

        //let rows = Array(1).fill(0).map(row => new Array(5).fill(""));
        let rows = Array(0).fill(0);
        for(let i = 0; i < rowsForEachYear.length; i++) {  // Go through each year
          let year = i + 1;
          rowsForEachYear[i][0][0] = "Year " + year;  // Build the year row (Just build it every time, even if already there)
          for(let j = 0; j < rowsForEachYear[i].length; j++) {  // Go through each row for this year
            rows.push(rowsForEachYear[i][j]);  // Here, i is for year and j is for row. Push each row in the the complete array of rows
          }
        }

        value = "";  // For next input

        //this.setState({value: value, classes: classes, rows: rows});
        this.setState({value: value, classes: classes, classCount: classCount, acadPlanObj:acadPlanObj, rowsFilled: rowsFilled, rowsFilledForQtr: rowsFilledForQtr ,rowsForEachYear: rowsForEachYear, rows: rows});
      }

      event.preventDefault();  // Important
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
      let classCount = this.state.classCount;
      if (classCount >= 1) {  // If there's a class to be removed in the first place
        console.log("classCount(before decrement): " + String(classCount));
        classCount--;
        console.log("classCount(after decrement): " + String(classCount));

        let toRemove = this.state.toRemove;
        console.log("toRemove: " + toRemove);
        let classes = this.state.classes.slice();
        let rows = this.state.rows.slice();

        // i for rows, j for columns
        // Go through each column of each row to remove instance of the class to be removed
        for (let i = 0; i < rows.length; i++) {
          for (let j = 0; j < rows[i].length; j++) {
            if (rows[i][j] === toRemove) {
              console.log("i: " + String(i) + "    j: " + String(j) + "    rows[i][j]: " + rows[i][j]);
              rows[i][j] = ""; // Remove by making it an empty string
            }
          }
        }

        // Also need to remove it in  rowsForEachYear
        //   Complicated. Will need to update current table index

        console.log("classes(before remove): " + classes.toString());
        /*
        for (let i = 0; i < classes.length; i++) {
          if (classes[i] === toRemove) {
            classes.splice(i, 1);
          }
        }    
        */
        let x = 0;
        while (x < classes.length) {
          if (classes[x] === toRemove) {
            classes.splice(x, 1);
          } else {
            x++;
          }
        }
        console.log("classes(after remove): " + classes.toString());

        toRemove = "";

        this.setState({classes: classes, classCount: classCount, toRemove: toRemove, rows: rows});
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

          <form onSubmit={this.handleSubmit3}>
            <label>Remove a class:&nbsp;</label>
            <select className="toRemove" onChange={this.handleChange4}>
              <option value="">Select</option>
              {this.state.classes.map((theClass) => <option value={theClass.value}>{theClass}</option>)}
            </select>
            &nbsp;
            <input type="submit" value="Remove" />
          </form>

          <Grid
            data={this.state.rows}
            columns={["Year", "Fall", "Winter", "Spring", "Summer"]}
            width="50%"
          />

          <form onSubmit={this.handleSubmit2}>
            <input type="submit" value="Submit" />
          </form>

          <h2>Results:</h2>

          <p><b>Requirements: </b>{this.state.requiredList}</p>
          <p><b>Missing: </b>{this.state.missingList}</p>
          <p><b>Fulfilled:</b>{this.state.fulfilledList}</p>
        </div>
      );
    }
}

export default EnterClasses;

