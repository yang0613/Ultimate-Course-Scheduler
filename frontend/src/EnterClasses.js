// Task 1 and 3

// Sources:
// https://reactjs.org/tutorial/tutorial.html
// https://reactjs.org/docs/forms.html
// https://reactjs.org/docs/lists-and-keys.html
// https://www.pluralsight.com/guides/display-multidimensional-array-data-in-react
// https://stackoverflow.com/questions/42238556/accessing-multidimensional-array-with-react-js

import React from 'react';

class EnterClasses extends React.Component {
    constructor(props) {
      super(props);
      this.state = {
        quarter: "", // Current quarter in which to add classes to
        value: "",  // Current value of input form for classes
        classes: Array(0).fill(""),  // Array of entered classes
        classesPerQtr: Array(6).fill(0).map(row => new Array(0).fill("")),
        //classList: "",  // List of entered classes as an HTML unordered list
        classList: Array(6).fill(""),
        dummyReqsJSON: '["CSE 101", "CSE 102", "CSE 103", "CSE 120", "CSE 130", "CSE 116", "STAT 131"]',
        requiredList: "", // Keep only for testing? Or do I leave it?
        missingList: "",  // Missing requirements as an HTML unordered list
        fulfilledList: "", // Fulfilled requirements as an HTML unordered list
      };

      this.handleChange1 = this.handleChange1.bind(this);
      this.handleChange2 = this.handleChange2.bind(this);
      this.handleSubmit1 = this.handleSubmit1.bind(this);
      this.handleSubmit2 = this.handleSubmit2.bind(this);
    }

    handleChange1(event) {  // https://reactjs.org/docs/forms.html had this
      this.setState({value: event.target.value});
    }

    handleChange2(event) {  // https://reactjs.org/docs/forms.html had this
      this.setState({quarter: event.target.value});
    }

    handleSubmit1(event) {  // Handles entering classes
      let quarter = this.state.quarter;
      let value = this.state.value;
      if (value === "") {
        alert("Please enter a value before submitting.");
      }
      else {
        let qtr = 0; // Number to indicate which quarter to enter class
        switch(quarter) {
          case "Fall 2021":
            qtr = 0;
            break;
          case "Winter 2022":
            qtr = 1;
            break;
          case "Spring 2022":
            qtr = 2;
            break;
          case "Fall 2022":
            qtr = 3;
            break;
          case "Winter 2023":
            qtr = 4;
            break;
          case "Spring 2023":
            qtr = 5;
            break;
          default:
            qtr = 0;
            break;
        }
        const classes = this.state.classes.slice();
        const classesPerQtr = this.state.classesPerQtr.slice();
        classes.push(value);
        classesPerQtr[qtr].push(value);

        /*
        const classList = classes.map((string) =>
          <li>{string}</li>
        );
        */

        const classList = classesPerQtr.map((classesForQtr) =>
          classesForQtr.map((a_class) =>
            <li>{a_class}</li>
          )  // NOTE: Notice the lack of a semicolon, which gives an error when put in
        );

        value = "";  // For next input

        this.setState({value: value, classesPerQtr: classesPerQtr, classes: classes, classList: classList});
      }

      event.preventDefault();
    }

    handleSubmit2(event) {  // Handles submitting the list of classes
      const dummyReqsJSON = this.state.dummyReqsJSON;
      const dummyReqsArr = JSON.parse(dummyReqsJSON);
      const classes = this.state.classes.slice();
      const missing = [];
      const fulfilled = [];
      let classVal = "";

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

      // Remove this one later?
      const requiredList = dummyReqsArr.map((string) =>
        <li>{string}</li>
      );

      const missingList = missing.map((string) =>
        <li>{string}</li>
      );

      const fulfilledList = fulfilled.map((string) =>
        <li>{string}</li>
      );

      this.setState({requiredList: requiredList, missingList: missingList, fulfilledList: fulfilledList});

      event.preventDefault();  // Just for now. Actually want to submit once able to connect to backend
    }

    render() {
      // Dummy json to check if missing requirements handler works
      //   CSE 12, CSE 16, CSE 20, CSE 30, CSE 13S, MATH 19A, MATH 19B, MATH 21, MATH 23A, ECE 30
      //   CSE 101, CSE 102, CSE 103, CSE 120, CSE 130, CSE 116, STAT 131, CSE 115A, CSE 183
      // This should probably be a state? So that it changes depending on major
      //let dummyReqsJSON = '["CSE 101", "CSE 102", "CSE 103", "CSE 120", "CSE 130", "CSE 116", "STAT 131"]';

      // <ul>{this.state.classList}</ul>   Old way to display classList

      // NOTE: Notice the part that displays classList. It doesn't give a semicolon after map.
      //   Adding it in gives an error

      return (
        <div className="container1">
          <form onSubmit={this.handleSubmit1}>
            <label>
              Select quarter:
            </label>
            <select className="quarter" onChange={this.handleChange2}>
              <option value="Fall 2021">Fall 2021</option>
              <option value="Winter 2022">Winter 2022</option>
              <option value="Spring 2022">Spring 2022</option>
              <option value="Fall 2022">Fall 2022</option>
              <option value="Winter 2023">Winter 2023</option>
              <option value="Spring 2023">Spring 2023</option>
            </select>
            <label>
              Enter a class:
            </label>
            <input type="text" value={this.state.value} onChange={this.handleChange1} />
            <input type="submit" value="Add" />
          </form>

          <ul>
            {this.state.classList.map((classListForQtr) =>
              <div>
                <h4>Quarter(fix this)</h4>
                <ul>{classListForQtr}</ul>
              </div>
            ) }
          </ul>

          <form onSubmit={this.handleSubmit2}>
            <input type="submit" value="Submit" />
          </form>

          <h2>Results:</h2>

          <h4>Required:</h4>
          <ul>{this.state.requiredList}</ul>
          <h4>Missing:</h4>
          <ul>{this.state.missingList}</ul>
          <h4>Fulfilled:</h4>
          <ul>{this.state.fulfilledList}</ul>
        </div>
      );
    }
}

export default EnterClasses;