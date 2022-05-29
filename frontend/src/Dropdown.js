import React from "react";

class Dropdown extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      currentUnits: 5,
      currentDivs: 1,
      currentMajor: "Select",
      units : [5, 7, 10, 12, 15, 17, 19],
      divs: [1, 2, 3],
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
      ]
    
    };

    this.handleChange = this.handleChange1.bind(this);
    this.handleChange = this.handleChange2.bind(this);
    this.handleChange = this.handleChange3.bind(this);

    this.handleSubmit = this.handleSubmit.bind(this);
    
  }

  handleChange1(event) {
    this.setState({ value: event.target.value});
  }

  handleChange2(event) {
    this.setState({ value: event.target.value});
  }

  handleChange3(event) {
    this.setState({ value: event.target.value});
  }

  handleSubmit(event) {
    event.preventDefault();
  }

  render() {
    return (
      <form onSubmit={this.handleSubmit}>
        <label>Major:&nbsp;</label>
          <br />
          <select className="majorList" value={this.state.currentMajor} onChange={this.handleChange1}>
            <option value="Select">Select</option>
            {this.state.major.map((theMajor) => <option value={theMajor.value}>{theMajor}</option>)}
          </select>
        <label>Total Units:&nbsp;</label>
          <br />
          <select className="unitList" value={this.state.currentUnits} onChange={this.handleChange2}>
            <option value="Select">Select</option>
            {this.state.units.map((theUnits) => <option value={theUnits.value}>{theUnits}</option>)}
          </select>
        <br />
        <label>Upper Divs per Quarter:&nbsp;</label>
        <br />
        <select className="divList" value={this.state.currentDivs} onChange={this.handleChange3}>
          <option value="Select">Select</option>
          {this.state.divs.map((theDivs) => <option value={theDivs.value}>{theDivs}</option>)}
        </select>
        <br />
        <input className="button" type="submit" value="Submit" />
      </form>
    );
  }
}

export default Dropdown