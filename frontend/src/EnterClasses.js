// Task 1

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
        classList: "",  // List of entered classes as an HTML
      };

      this.handleChange = this.handleChange.bind(this);
      this.handleSubmit = this.handleSubmit.bind(this);
    }
 
    handleChange(event) {
      this.setState({value: event.target.value});
    }

    handleSubmit(event) {
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
  
    render() {
      return (
        <div className="container1">
          <form onSubmit={this.handleSubmit}>
            <label>
              Enter a class:
              <input type="text" value={this.state.value} onChange={this.handleChange} />
            </label>
            <input type="submit" value="Submit" />
          </form>
        
          <ul>{this.state.classList}</ul>
        </div>
      );
    }
}

export default EnterClasses;