// Sources:
// https://reactjs.org/tutorial/tutorial.html
// https://reactjs.org/docs/forms.html
// https://reactjs.org/docs/lists-and-keys.html
// https://www.pluralsight.com/guides/display-multidimensional-array-data-in-react
// https://stackoverflow.com/questions/42238556/accessing-multidimensional-array-with-react-js
// https://dev.to/antdp425/populate-dropdown-options-in-react-1nk0  For the dropdown
// https://jsonlint.com/  Useful for validating and making JSON easier to look at
// https://colors.muz.li/color/e6e6e6 For colors
// https://icongr.am/ For icons

import React from 'react';
import { Grid } from 'gridjs-react';
import "gridjs/dist/theme/mermaid.css";
import { _ } from "gridjs-react";
import {post, get, verify} from './Script';
import "./enterClassesStyles.css";

class EnterClasses extends React.Component {
    constructor(props) {
      super(props);
      this.state = {
        year: 1, // Current year in which to add classes to (Initially 1)
        quarter: "Fall", // Current quarter in which to add classes to (Initially Fall)
        value: "",  // Current value of input form for classes
        toRemove: "Select",  // Value to be removed (Select when nothing selected)
        classes: Array(0).fill(""),  // Array of all entered classes. Purpose is to make dealing with some parts easier.

        // Keep dummy availableClasses for testing
        //availableClasses: ["CSE 101", "CSE 102", "CSE 103", "CSE 201", "STAT 131", "MATH 19A", "MATH 19B", "MATH 21"],
        availableClasses: [],  // List of available clases, after major has been selected
        arrOfArrOfClassData: [],  // The response from the major selection dropdown containing the class data
        verificationResults: [],
        currentMajor: "Select", 
        major:[
          'Agroecology B.A.',
          'Anthropology B.A.',
          'Applied Linguistics and Multilingualism B.A.',
          'Applied Mathematics B.S.',
          'Applied Physics B.S.',
          'Art and Design: Games and Playable Media B.A.',
          'Art B.A.',
          'Biochemistry and Molecular Biology B.S.',
          'Biology B.A.',
          'Biology B.S.',
          'Biomolecular Engineering and Bioinformatics B.S.',
          'Biotechnology B.A.',
          'Business Management Economics B.A.',
          'Chemistry B.A.',
          'Chemistry B.S.',
          'Classical Studies B.A.',
          'Cognitive Science B.S.',
          'Community Studies B.A.',
          'Computer Engineering B.S.',
          'Computer Science B.A.',
          'Computer Science B.S.',
          'Computer Science: Computer Game Design B.S.',
          'Critical Race and Ethnic Studies B.A.',
          'Earth Sciences B.S.',
          'Earth Sciences/Anthropology Combined Major B.A.',
          'Ecology and Evolution B.S.',
          'Economics B.A.',
          'Economics/Mathematics Combined B.A.',
          'Education, Democracy, and Justice B.A.',
          'Electrical Engineering B.S.',
          'Environmental Sciences B.S.',
          'Environmental Studies B.A.',
          'Environmental Studies/Biology Combined Major B.A.',
          'Environmental Studies/Earth Sciences Combined Major B.A.',
          'Environmental Studies/Economics Combined Major B.A.',
          'Feminist Studies B.A.',
          'Film and Digital Media B.A.',
          'Global Economics B.A.',
          'History B.A.',
          'History of Art and Visual Culture B.A.',
          'Human Biology B.S.',
          'Jewish Studies B.A.',
          'Language Studies B.A.',
          'Latin American and Latino Studies B.A.',
          'Latin American and Latino Studies/Politics Combined B.A.',
          'Latin American and Latino Studies/Sociology Combined B.A.',
          'Legal Studies B.A.',
          'Linguistics B.A.',
          'Literature B.A.',
          'Marine Biology B.S.',
          'Mathematics B.A.',
          'Mathematics B.S.',
          'Mathematics Education B.A.',
          'Molecular, Cell, and Developmental Biology B.S.',
          'Music B.A.',
          'Music B.M.',
          'Network and Digital Technology B.A.',
          'Neuroscience B.S.',
          'Philosophy B.A.',
          'Physics (Astrophysics) B.S.',
          'Physics B.S.',
          'Plant Sciences B.S.',
          'Politics B.A.',
          'Psychology B.A.',
          'Robotics Engineering B.S.',
          'Science Education B.S.',
          'Sociology B.A.',
          'Spanish Studies B.A.',
          'Technology and Information Management B.S.',
          'Theater Arts B.A.'
        ],

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
      };

      this.handleChangeClass = this.handleChangeClass.bind(this); // Handles typing in a class
      this.handleChangeQuarter = this.handleChangeQuarter.bind(this); // Handles changing the current quarter to put a class into
      this.handleChangeYear = this.handleChangeYear.bind(this); // Handles changing the year to put a class into
      this.handleChangeMajor = this.handleChangeMajor.bind(this); // Handles selecting the major
      this.handleAddClass = this.handleAddClass.bind(this); // Handles clicking "Add" when entering a class
      this.handleVerify = this.handleVerify.bind(this); // Handles clicking "Verify" when submitting all classes to be taken
      this.handleRemoveClass = this.handleRemoveClass.bind(this); // Handles clicking "Remove" when removing a class
    }

    // Used to show initial table
    // https://stackoverflow.com/questions/65014512/how-to-initialize-data-before-rendering-in-react-js
    componentDidMount() {
      let acadPlanObj = localStorage.getItem('plan');
      acadPlanObj = acadPlanObj[0];
      
      if (!acadPlanObj) {
        const rows = Array(16).fill(0).map(row => new Array(5).fill(""));
        // rows[0][0], rows[4][0], ... are the "year rows"
        rows[0][0] = "Year 1";  // First row, first column  
        rows[4][0] = "Year 2";  // Fifth row, first column
        rows[8][0] = "Year 3";  // Ninth row, first column
        rows[12][0] = "Year 4";  // Thirteenth row, first column
        this.setState({rows: rows});
      } else {
        // plan == acadPlanObj
        let classes = [];
        let rowsFilled = this.state.rowsFilled;
        let rowsFilledForQtr = this.state.rowsFilledForQtr;
        let rowsForEachYear = this.state.rowsForEachYear;
        let rows = this.state.rows;
      
        // console.log("Start");
        // Iterate through the resulting acadPlanObj
        for (let yr of Object.keys(acadPlanObj)) {
          //console.log("Iterate Year (Should show up 4 times total");
          let yearObj = acadPlanObj[yr];
          let yrNum = 1; // The year as a number
          switch(yr) {
            case "First":
              yrNum = 1;
              break;
            case "Second":
              yrNum = 2;
              break;
            case "Third":
              yrNum = 3;
              break;
            case "Fourth":
              yrNum = 4;
              break;
            default:
              yrNum = 1;
              break;
          }
      
          for (let qtr of Object.keys(yearObj)) {
            //console.log("Iterate Quarter (Should show up 16 times total)");
            let quarterListOfClasses = yearObj[qtr];
            for (let i = 0; i < quarterListOfClasses.length; i++) {
              // Use handleAddClassForLogin to add everything
              let value = quarterListOfClasses[i];
              //this.handleAddClassForLogin(yrNum, qtr, value);
              console.log("value", value);
              //const classes = this.state.classes.slice();
              classes.push(value);  // Add this class to list of all classes
      
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
            }
          }
        }
      
        rows = this.buildRows(rowsForEachYear);
      
        this.setState({classes: classes, rowsFilled: rowsFilled, rowsFilledForQtr: rowsFilledForQtr, rowsForEachYear: rowsForEachYear, rows: rows});        
      }
    }

    // https://reactjs.org/docs/forms.html had this
    handleChangeClass(event) {  // Handles typing in a class name
      this.setState({value: event.target.value});
    }

    handleChangeQuarter(event) {  // Handles selecting the quarter in the dropdown
      this.setState({quarter: event.target.value});
    }

    handleChangeYear(event) {  // Handles selecting the year in the dropdown
      this.setState({year: event.target.value});
    }

    handleChangeMajor(event) {  // Handles selecting major
      let currentMajor = event.target.value;  // This is the data to be passed to the post/fetch call
      console.log(currentMajor);

      const current = {
        "majorstr": currentMajor
      };

      const response = post(current);
      response.then((res)=>{ //res = response.then -- promise, then
        return res.json();
      })
      .then((json) => {
        let returnedData = json;  // I added
        console.log("returnedData: ", returnedData);

        // returnedData is an array of array of arrays
        // Keep the array of arrays, which is an array of class data(class data is an array)
        let arrOfArrOfClassData = returnedData[0];  // Keep this for later (Sprint 4, can show units, full name, etc.)
        console.log("arrOfArrOfClassData: ", arrOfArrOfClassData);
        
        let availableClasses = [];  // This will be the list of available classes.
        let numberOfClasses = arrOfArrOfClassData.length;
        for (let i = 0; i < numberOfClasses; i++) 
        {  // For each class, get the 0th element (Contains class name  Ex. "CSE 101")
          availableClasses.push(arrOfArrOfClassData[i][0]);
          console.log("available classes: ", arrOfArrOfClassData[i][0]);
        }

        this.setState({currentMajor: currentMajor, arrOfArrOfClassData: arrOfArrOfClassData, availableClasses: availableClasses});
      })
      .catch((err)=>{
        console.log(err, "ERROR");
      })
    }

    handleAddClass(event) {  // Handles entering classes
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
            // Update rowsForEachYear (Functionality explained in this.state within the constructor at the very beginning of this JavaScript class
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
            //
            //    rowsForEachYear: Array(4).fill(0).map(rowsForOneYear => Array(4).fill(0).map(row => new Array(5).fill("")))
            //    rowsFilled: Array(4).fill(0)  // Update by +1 before each use (So on first use, 0 -> 1)
            //    rowsFilledForQtr: Array(4).fill(0).map(() => ({"Fall": 0, "Winter": 0, "Spring": 0, "Summer": 0}))
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
          value = "";  // For next input
          this.setState({value: value});
        }
      }

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

    handleVerify(event) {  // Handles submitting the list of classes for verification (Clicking Verify)
      // INTEGRATION: Create the object that will be passed to the backend
      let rowsForEachYear = this.state.rowsForEachYear.slice();
      //let acadPlanObj = {"1": {"Fall": [], "Winter": [], "Spring": [], "Summer": []}, "2": {"Fall": [], "Winter": [], "Spring": [], "Summer": []}, "3": {"Fall": [], "Winter": [], "Spring": [], "Summer": []}, "4": {"Fall": [], "Winter": [], "Spring": [], "Summer": []}};
      let acadPlanObj = {"First": {"Fall": [], "Winter": [], "Spring": [], "Summer": []}, "Second": {"Fall": [], "Winter": [], "Spring": [], "Summer": []}, "Third": {"Fall": [], "Winter": [], "Spring": [], "Summer": []}, "Fourth": {"Fall": [], "Winter": [], "Spring": [], "Summer": []}};
      for (let k = 0; k < rowsForEachYear.length; k++) {  // Iterate through each year
        //let yr = String(k + 1);  // Will be 1 to 4
        let yr = "";
        switch(k) {
          case 0:
            yr = "First";
            break;
          case 1:
            yr = "Second";
            break;
          case 2:
            yr = "Third";
            break;
          case 3:
            yr = "Fourth";
            break;
          default:
            yr = "First";
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
      console.log("acadPlanObj", acadPlanObj);

      // IGNORE FOR NOW
      //   FOR SPRINT 4: When schedule generation is done, need to create another object that contains preferences
      //   Ask algorithm how they want the data to be passed (in acadPlanObj, or a seperate post request?)

      // See testDataforEnterClasses.js for format of acadPlanObj

      const current = acadPlanObj;
      
      // const store = storePlan(current);

      // store.then((res)=>{ //res = response.then -- promise, then
      //   return res.json();
      // })
      // .then((json) => {
      //   console.log(json);
      // })
      // .catch((err)=>{
      //   console.log(err, "ERROR");
      // })

      const response = verify(current);
      response.then((res)=>{ //res = response.then -- promise, then
        return res.json();
      })
      .then((json) => {
        let resultJSON = JSON.stringify(json);  // I added
        //let resultJSON = json;
        console.log("resultJSON: " + JSON.stringify(resultJSON));  // works
        //console.log("resultJSON", resultJSON);  // doesn't work if returnedData not stringified
        
        let errorMessageList = [];

        // Iterate through the resulting object to get the error messages
        let resultObj = JSON.parse(resultJSON);
        for (let year of Object.keys(resultObj)) {
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
        
        //console.log(JSON.stringify(errorMessageList));  // TESTING
    
        // Works, but need to change formatting so it looks better
        const verificationResults = errorMessageList.map((string) =>
          <li>{string}</li>
        );

        this.setState({verificationResults: verificationResults});  

      })
      .catch((err)=>{
        console.log(err, "ERROR");
      })

      // IGNORE FOR NOW
      // INTEGRATION (FOR SPRINT4 GENERATING):
      // For generating a schedule, create a seperate handleSubmit
      // Then just update rowsForEachYear by parsing the data returned by backend

      event.preventDefault(); // Without this, the page re-renders and all states are lost
    }

    handleRemoveClass(event) {  // For class removal from the list of entered classes

      /*  OLD  For now, keep for reference in case its needed
      let toRemoveInnerHTML = event.target.innerHTML;
      toRemoveInnerHTML = toRemoveInnerHTML.trim();
      console.log("toRemove", toRemoveInnerHTML);

      // Check with Wenhao to clarify if all classes have class name format:  CSE 101    where its   classname(space)number
      let toRemoveSplit = toRemoveInnerHTML.split(" ");
      let toRemove = toRemoveSplit[0] + " " + toRemoveSplit[1];
      */

      //let toRemove = event.target.value;
      let toRemove = event.target.parentElement.value;

      //https://stackoverflow.com/questions/18971210/get-inner-text-and-split-it-javascript-problems-using-innerhtml-and-split
      //console.log("toRemove", toRemove);

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

                  // IF THIS GIVES ERRORS:
                  // If removing classes before submitting to backend gives unexpected behavior regarding results
                  //   Problem could be because there's an extra element in the array with "" as its value
                  //   Solution: Pop the last element if length > 3
                  // ALTERNATIVE: Just fix it in handleVerify
                  //   Don't add values that are ""
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
                // Note: When adding another class (in handleAddClass):
                //   rowsFilledForQtr is used as an index for the current row to fill when pushing into rowsForEachYear 
                //   rowsFilled is used to determine if an extra row needs to be added

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
          <form onSubmit={this.handleAddClass}>
            {
              // ADDED for integeration may 18
            }
            <label>Major:&nbsp;</label>
            <select className="majorList" value={this.state.currentMajor} onChange={this.handleChangeMajor}>
              <option value="Select">Select</option>
              {this.state.major.map((theMajor) => <option value={theMajor.value}>{theMajor}</option>)}
            </select>
            &emsp;
      
            <label>Enter Course:&nbsp;</label>
            <input list="availableClasses" name="classstr" value={this.state.value} onChange={this.handleChangeClass} />
            <datalist id="availableClasses">
              <option value=""></option>
              {this.state.availableClasses.map((theClass) => <option value={theClass.value}>{theClass}</option>)}
            </datalist>
            &nbsp;
            <button class="button is-info is-rounded is-small add-class-button"><img src="https://icongr.am/entypo/arrow-right.svg?size=20&color=ffffff" alt="X button" onClick={this.handleAddClass}></img></button>
            {
              //<input type="submit" value="Add" />  OLD Submit button  Use this if the button above causes errors
            }

            &emsp;
            <label>Quarter:&nbsp;</label>
            <select className="quarter" onChange={this.handleChangeQuarter}>
              <option value="Fall">Fall</option>
              <option value="Winter">Winter</option>
              <option value="Spring">Spring</option>
              <option value="Summer">Summer</option>
            </select>
            &emsp;
            <label>Year:&nbsp;</label>
            <select className="quarter" onChange={this.handleChangeYear}>
                <option value="1">Year 1</option>
                <option value="2">Year 2</option>
                <option value="3">Year 3</option>
                <option value="4">Year 4</option>
            </select>
          </form>
          <br></br>

          {
            // The academic plan table
            // https://gridjs.io/docs/examples/react-cells
            // https://stackoverflow.com/questions/37627712/how-to-use-if-else-condition-in-arrow-function-in-javascript
          }
          <Grid
            data={this.state.rows}
            columns={
              [
                "Year",
                { 
                  name: "Fall",
                  formatter: (cell) => (cell === "") ? "" : _(<button class="button is-info is-rounded" value={cell}> {cell} &nbsp;<img src="https://icongr.am/clarity/close.svg?size=20&color=E6E6E6" alt="X button" onClick={this.handleRemoveClass}></img></button>)
                },
                { 
                  name: "Winter",
                  formatter: (cell) => (cell === "") ? "" : _(<button class="button is-info is-rounded" value={cell}> {cell} &nbsp;<img src="https://icongr.am/clarity/close.svg?size=20&color=E6E6E6" alt="X button" onClick={this.handleRemoveClass}></img></button>)
                },
                { 
                  name: "Spring",
                  formatter: (cell) => (cell === "") ? "" : _(<button class="button is-info is-rounded" value={cell}> {cell} &nbsp;<img src="https://icongr.am/clarity/close.svg?size=20&color=E6E6E6" alt="X button" onClick={this.handleRemoveClass}></img></button>)
                },
                { 
                  name: "Summer",
                  formatter: (cell) => (cell === "") ? "" : _(<button class="button is-info is-rounded" value={cell}> {cell} &nbsp;<img src="https://icongr.am/clarity/close.svg?size=20&color=E6E6E6" alt="X button" onClick={this.handleRemoveClass}></img></button>)
                }
              ]
            }
            width="100%"
          />

          <div class="flex-container">
            {
              // Submit the academic plan table (As a JSON, with each class associated with a quarter and a year)
            }
            <form onSubmit={this.handleVerify}>
                <input class="button is-info is-rounded" type="submit" value="Verify" />
            </form>
            &emsp;

            {
              // Not functional
            }
            <button class="button is-info is-rounded">Generate</button>

          </div>

          <br></br>

          {
            // This is where the errors will be shown
          }      
          <br></br>
          <h2>Verification Results:</h2>
          <ul>{this.state.verificationResults}</ul>

        </div>
      );
    }
}

export default EnterClasses;
