// Task 1 and 3

// Sources:
// https://reactjs.org/tutorial/tutorial.html
// https://reactjs.org/docs/forms.html
// https://reactjs.org/docs/lists-and-keys.html

import React from 'react';

class EnterClasses extends React.Component {
    constructor(props) {
      super(props);
      this.state = {
        value: "",  // Current value of form
        classes: Array(0).fill(""),  // Array of entered classes
        classList: "",  // List of entered classes as an HTML unordered list
        dummyReqsJSON: '["CSE 101", "CSE 102", "CSE 103", "CSE 120", "CSE 130", "CSE 116", "STAT 131"]',
        requiredList: "", // Keep only for testing? Or do I leave it?
        missingList: "",  // Missing requirements as an HTML unordered list
        fulfilledList: "", // Fulfilled requirements as an HTML unordered list
      };

      this.handleChange = this.handleChange.bind(this);
      this.handleSubmit1 = this.handleSubmit1.bind(this);
      this.handleSubmit2 = this.handleSubmit2.bind(this);
    }
 
    handleChange(event) {  // https://reactjs.org/docs/forms.html had this
      this.setState({value: event.target.value});
    }

    handleSubmit1(event) {  // Handles entering classes
      let value = this.state.value;
      if (value === "") {
        alert("Please enter a value before submitting.");
      }
      else {
        const classes = this.state.classes.slice();
        classes.push(value);

        const classList = classes.map((string) =>
          <li>{string}</li>
        );

        value = "";  // For next input

        this.setState({value: value, classes: classes, classList: classList});
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

      return (
        <div className="container1">
          <form onSubmit={this.handleSubmit1}>
            <label>
              Enter a class:
              <input type="text" value={this.state.value} onChange={this.handleChange} />
            </label>
            <input type="submit" value="Add" />
          </form>
        
          <ul>{this.state.classList}</ul>

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