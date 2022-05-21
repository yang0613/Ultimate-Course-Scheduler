import React from "react";

class UnitsDropdown extends React.Component {
  constructor(props) {
    super(props);
    this.state = {value: "5"};

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    
  }

  handleChange(event) {
    this.setState({ value: event.target.value});
  }

  handleSubmit(event) {
    event.preventDefault();
  }

  render() {
    return (
      <form onSubmit={this.handleSubmit}>
        <label>
          Total Units:
          <br/>
          <select value={this.state.value} onChange={this.handleChange}>
            <option value="5">5</option>
            <option value="7">7</option>
            <option value="10">10</option>
            <option value="12">12</option>
            <option value="15">15</option>
            <option value="17">17</option>
            <option value="19">19</option>
          </select>
        </label>
        <input type="submit" value="Submit" />
      </form>
    );
  }
}

export default UnitsDropdown