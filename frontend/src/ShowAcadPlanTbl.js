import React from 'react';

//import { Grid } from "gridjs";
import { Grid } from 'gridjs-react';
import "gridjs/dist/theme/mermaid.css";

class ShowAcadPlanTbl extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      /*
        {
          "Fall 2022": {"CSE-130": 5, "CSE-103": 5, "CSE-180": 5}
          "Winter 2023":  same as above
          ...
        }
      */
      // NOTE: Quarters could be missing for a year, but "{Quarter} {Year}" values must be ordered
      acadPlanJSON1: '{"Fall 2022":{"CSE-130": 5, "CSE-103": 5, "CSE-111": 5, "CSE-118": 5}, "Winter 2023":{"CSE-115A": 5, "CSE-102": 5, "CSE-183": 5}, "Spring 2023":{"CSE-115B": 5, "CSE-114A": 5, "CSE-110A": 5}, "Summer 2023":{"CSE-144": 5}, "Fall 2023":{"CSE-115C": 5, "CSE-120": 5}, "Winter 2024":{"CSE-115A": 5, "CSE-138": 5}}',
      acadPlanJSON2: '{"Fall 2022":{"CSE-130": 5, "CSE-103": 5}, "Winter 2023":{"CSE-115A": 5, "CSE-102": 5}, "Spring 2023":{"CSE-115B": 5, "CSE-114A": 5}}',
      acadPlanJSON3: '{"Fall 2022":{"CSE-130": 5, "CSE-103": 5, "CSE-111": 5, "CSE-118": 5}, "Winter 2023":{"CSE-115A": 5, "CSE-102": 5, "CSE-183": 5}, "Spring 2023":{"CSE-115B": 5, "CSE-114A": 5, "CSE-110A": 5}, "Summer 2023":{"CSE-144": 5}, "Fall 2023":{"CSE-115C": 5, "CSE-120": 5}, "Winter 2024":{"CSE-115A": 5, "CSE-138": 5, "CSE-181": 5}, "Fall 2024":{"CSE-145": 5, "CSE-150": 5, "CSE-150L": 2}}',
      acadPlanJSON4: '{"Fall 2022":{"CSE-130": 5, "CSE-103": 5, "CSE-111": 5, "CSE-118": 5}, "Winter 2023":{"CSE-115A": 5, "CSE-102": 5, "CSE-183": 5}, "Spring 2023":{"CSE-115B": 5, "CSE-114A": 5, "CSE-110A": 5}, "Summer 2023":{"CSE-144": 5}, "Fall 2023":{"CSE-115C": 5, "CSE-120": 5}, "Winter 2024":{"CSE-115A": 5, "CSE-138": 5, "CSE-181": 5}, "Fall 2024":{"CSE-145": 5, "CSE-150": 5, "CSE-150L": 2}, "Winter 2026":{"CSE-160": 5, "CSE-160L": 2}}',
      // Rows for grid. Each row has 5 columns (Year, Fall, Winter, Spring, Summer)
      //   There are 4 rows for one year. 1 for containing current year. 3 for classes
      //   Can add more rows whenever needed
      //   UPDATE: Just start off with 1 row for the year row
      rows: Array(1).fill(0).map(row => new Array(5).fill("")),

      // DO LATER: See handleSubmit1
      //columns: Array(0).fill(),
      //gridHTML: ""
    };

    this.handleSubmit1 = this.handleSubmit1.bind(this);
  }

  handleSubmit1(event) {  // Handles generating an academic plan (Clicking generate)
    const acadPlanJSON = this.state.acadPlanJSON3; // Can change the number at the end to 1, 2, 3, or 4 for testing
    const acadPlanObj1 = JSON.parse(acadPlanJSON);

    // DO LATER: Only show a table after generate has been clicked.
    //const columns = ["Year", "Fall", "Winter", "Spring", "Summer"];
    //this.setState({columns: columns});
    //let gridHTML = <Grid data={this.state.rows} columns={this.state.columns} width='50%' />;
    //this.setState({gridHTML: gridHTML});

    // A.) Create an object with years as keys.
    // B.) Its values will be the list of classes for each quarter as objects, with each list being an object.
    //   For those objects:
    //     - the quarters(Fall, Winter, Spring, Summer) are the keys
    //     - the values are the list of classes(each one being an object, with the class name as the key and units as the value)
    // C.) To create the object mentioned in A:
    //   For each key, tokenize -> check which quarter -> check which year
    //     If quarter is Fall, put into that year's list
    //     If quarter is Winter, Spring, or Summer, put into list for (year - 1)
    const acadPlanObj2 = {};
    for (let quarter of Object.keys(acadPlanObj1)) {  // Basically, just need to know which year to put in a class list
      let str1 = quarter;
      let str2 = str1.split(" ");
      let qtr = str2[0];
      let year = "";
      if (qtr === "Fall") {  // For Winter, Spring, and Summer, just put into the same year as Fall
        year = str2[1];
      } else {
        year = String(Number(str2[1]) - 1);
      }
      if (acadPlanObj2[year]) {  // If there's already an existing property to represent this year
        acadPlanObj2[year][qtr] = acadPlanObj1[quarter];  // Notice how one side uses qtr, other uses quarter
      } else {
        acadPlanObj2[year] = {};  // An object
        acadPlanObj2[year][qtr] = acadPlanObj1[quarter];
      }

      // When this loop finishes, each acadPlanObj2[year] should be in the same format as acadPlanObj1
      //   With the only difference that instead of having "Fall 2022", it will have "Fall"
    }

    console.log(JSON.stringify(acadPlanObj2));  // FOR TESTING

    let rows = this.state.rows.slice();

    let k = 0;  // First row for current year
    for (let year of Object.keys(acadPlanObj2)) {
      if (k > 0) {  // If not the first year, add a row to enter first row data for this year
        rows.push(["","","","",""]);  // (NOTE: React suggests using concat instead of push, but concat doesn't work for some reason)
      }

      rows[k][0] = year + "-" + String(Number(year) + 1);
      let classesThisYear = acadPlanObj2[year];

      // Iterate through each key(quarter).
      // https://stackoverflow.com/questions/684672/how-do-i-loop-through-or-enumerate-a-javascript-object
      // https://www.w3schools.com/js/js_object_properties.asp
      //let j = 1; // Current column to fill. Start at 1 since first column is taken up by year.
      for (let qtr of Object.keys(classesThisYear)) {  // Iterate through each quarter
        let classesThisQtr = classesThisYear[qtr];  // Class list for this quarter

        // Column depends on qtr
        // Note that the quarters used as keys here are "Fall", "Winter", etc. instead of "Fall 2022", "Winter 2023", etc.
        let j = 0;
        switch(qtr) {
          case "Fall":
            j = 1;
            break;
          case "Winter":
            j = 2;
            break;
          case "Spring":
            j = 3;
            break;
          case "Summer":
            j = 4;
            break;
          default:
            j = 1;
            break;
        }

        // Iterate through each class (Classes are keys, units are values).
        // Adding classes for each quarter for current year could increase the number of rows
        //let i = 1;  // Current row to fill. Always start at 1 since first row is taken up by year.
        //let i = 0; // Just start at 0 and add 1 before every iteration below
        let i = k;
        for (let curClass of Object.keys(classesThisQtr)) {
          i++;  // Add classes row by row
          if (i >= rows.length) {  // Add a row with 5 columns since there's no more space
            rows.push(["","","","",""]);  // (NOTE: React suggests using concat instead of push, but concat doesn't work for some reason)
          }
          let units = classesThisQtr[curClass];
          rows[i][j] = curClass + " | " + units;  // Find a way to space this better. Cells ignore >1 spaces
        }

        //j++; // Place next set of classes to other column
      }

      k = rows.length;  // First row for current year is the last index + 1, since we started at row 0 (just the number of rows)
    }

    this.setState({rows: rows});  // Update state

    event.preventDefault();  // REMOVE after backend and frontend has been connected
  }

  // Table structure
  //     https://www.geeksforgeeks.org/how-to-create-nest-tables-within-tables-in-html/
  // OR using Grid.js:
  /*
        <Grid
          data={[
            ["2022-2023"],
            ["", "CSE-130", "CSE-115A", "CSE-115B", "CSE-144"],
          ]}
          columns={["Year", "Fall", "Winter", "Spring", "Summer"]}
        />
  */

  render() {
    return (
      <div className="container2">
        <form onSubmit={this.handleSubmit1}>
          <input type="submit" value="Generate Plan" />
        </form>

        <Grid
          data={this.state.rows}
          columns={["Year", "Fall", "Winter", "Spring", "Summer"]}
          width="50%"
        />

      </div>
    );
  }
}

export default ShowAcadPlanTbl;