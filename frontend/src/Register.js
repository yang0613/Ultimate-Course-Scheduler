
import React from 'react';

//<a href="login.html">Login to Account</a>

class Register extends React.Component 
{
  render() {
    return (
        <div class="container has-text-centered">
        
        <h1 class="title">Create Account</h1>

        <div class="field">
          <label class="label">Name</label>
          <div class="control">
            <input class="input" type="text" placeholder="Text input"></input>
          </div>
        </div>
        
        <div class="field">
          <label class="label">Username</label>
          <div class="control has-icons-left has-icons-right">
            <input class="input is-success" type="text" placeholder="Text input" value="name"></input>
            <span class="icon is-small is-left">
              <i class="fas fa-user"></i>
            </span>
            <span class="icon is-small is-right">
              <i class="fas fa-check"></i>
            </span>
          </div>
          <p class="help is-success">This username is available</p>
        </div>
        
        <div class="field">
          <label class="label">Email</label>
          <div class="control has-icons-left has-icons-right">
            <input class="input is-danger" type="email" placeholder="Email input" value="hello@"></input>
            <span class="icon is-small is-left">
              <i class="fas fa-envelope"></i>
            </span>
            <span class="icon is-small is-right">
              <i class="fas fa-exclamation-triangle"></i>
            </span>
          </div>
          <p class="help is-danger">This email is invalid</p>
        </div>
        
        <div class="field">
          <div class="control">
            <label class="checkbox">
              <input type="checkbox"></input>
              I agree to the <a href="#">terms and conditions</a>
            </label>
          </div>
        </div>
        
        <div class="field is-grouped">
          <div class="control">
            <button class="button is-link">Register</button>
          </div>
        </div>

        <br></br><br></br>

      </div>
    );
  }
}

export default Register;

