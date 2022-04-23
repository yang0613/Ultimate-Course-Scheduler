import React from 'react';
//import EnterClasses from './EnterClasses';  // Or should EnterClasses import ShowScheduleTable instead?
//  Maybe they shouldn't import each other

// Whenever an array that is a state is to be mutated, use concat instead of push so we don't mutate the original
//   https://reactjs.org/tutorial/tutorial.html  in Lifting State Up, Again section

class ShowAcadPlanTbl extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      // The "5-unit GE" is just a way for us to tell the user to fill up the remaining units with a GE
      //   Since we don't want to recommend them 3 upper-div courses unless they specify that their okay with it
      dummyAcadPlanJSON: '[{"quarter": "Fall 2022", "classes":["CSE 130", "CSE 103", "5-unit GE"]}, {"quarter": "Winter 2023", "classes": ["CSE 102", "CSE 115A", "CSE 116"]}]',
      acadPlanTblHTML: "", // Academic plan table as an HTML (contains different lists)

      // '[{"quarter": "Fall 2022", "classes":["CSE 130", "CSE 103", "CSE 180"]}, {"quarter": "Winter 2023", "classes": ["CSE 102", "CSE 115A", "CSE 116"]}]'
    };

    //this.handleChange = this.handleChange.bind(this);
    //this.handleSubmit1 = this.handleSubmit1.bind(this);
  }

  render() {
    return (
      <div className="container2">
          Doesn't do anything yet:
          <form onSubmit={this.handleSubmit1}>
            <input type="submit" value="Generate Plan" />
          </form>
          Academic Plan:
          TO DO
      </div>
    );
  }
}

export default ShowAcadPlanTbl;