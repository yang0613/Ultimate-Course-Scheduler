// heading.js

import Login from './Login';
import Register from './Register';
import EnterClasses from './EnterClasses';
import React, { useState } from 'react';

class LandingPage extends React.Component 
{

  constructor(props) {
    super(props);
    this.state = {
      showComponent: false,
    };
    this._onLoginClick = this._onLoginClick.bind(this);
    this._onRegisterClick = this._onRegisterClick.bind(this);
    this._onGuestClick = this._onGuestClick.bind(this);
  }

  _onLoginClick() {
    this.setState({
      showComponentLogin: true,
    });
  }

  _onRegisterClick() {
    this.setState({
      showComponentRegister: true,
    });
  }

  _onGuestClick() {
    this.setState({
      showComponentGuest: true,
    });
  }

  render() 
  {
    return (
      <div class="container has-text-centered">
        <figure class="image is-inline-block ">
          <img src="slugLogo.png" alt="Placeholder image"></img>
        </figure>
        <br></br>

        <button text-align="center" class="button is-info is-rounded"
          onClick={this._onLoginClick} >
          Login to Account
        </button> 
        <br></br><br></br>
        {this.state.showComponentLogin ?
           <Login /> :
           null
        }

        <br></br>

        <button text-align="center" class="button is-info is-rounded"
          onClick={this._onRegisterClick} >
          Create Account
        </button> 
        <br></br><br></br>
        {this.state.showComponentRegister ?
           <Register /> :
           null
        }

        <br></br>

        <button text-align="center" class="button is-info is-rounded"
          onClick={this._onGuestClick} >
          Continue as Guest
        </button> 
        <br></br><br></br>
        {this.state.showComponentGuest ?
           <EnterClasses /> :
           null
        }

        <br></br><br></br>
      </div>
    );
  }
}

export default LandingPage;

