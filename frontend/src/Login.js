import React, { useState } from 'react';
import { BrowserRouter, Route, Switch, Link } from 'react-router-dom';
import {useNavigate} from 'react-router-dom';
import PropTypes from 'prop-types';
import './Login.css';
import {login} from './Script';



export default function Login({}) {
  const navigate = useNavigate()
  const [username, setUserName] = useState();
  const [password, setPassword] = useState();

  async function loginUser(credentials) {
    console.log(credentials, "  CREDENTIALS");
    const response = login(credentials);
    console.log(response, " POST CREDENTIALS");
  
    response.then((res)=>{
      return res.json();
      })
      .then((json) => {
        console.log("returnedData: ", json);
        localStorage.setItem('plan', JSON.stringify(json));
        navigate("/plan");
      })
      .catch((err)=>{
        console.log(err, "ERROR");
      })
  }
  
  const handleSubmit = async e => {
    e.preventDefault();
    const token = await loginUser({
      "username": username,
      "password": password
    });
    
    //setToken(token);
  }

  return(
    <div className="login-wrapper">
      <form onSubmit={handleSubmit}>

        
        <div class="field">
          <p class="control has-icons-left has-icons-right">
            <input class="input" type="email" placeholder="Email"
             onChange={e => setUserName(e.target.value)}></input>
            <span class="icon is-small is-left">
              <i class="fas fa-envelope"></i>
            </span>
            <span class="icon is-small is-right">
              <i class="fas fa-check"></i>
            </span>
          </p>
        </div>

        <div class="field">
          <p class="control has-icons-left">
            <input class="input" type="password" placeholder="Password"
            onChange={e => setPassword(e.target.value)}></input>
            <span class="icon is-small is-left">
              <i class="fas fa-lock"></i>
            </span>
          </p>
        </div>

        <div class="field">
          <p class="control">
            <div>
                <button type="submit" class="button is-info is-rounded">
                  Submit
                </button>
            </div>
          </p>
        </div>

        <br></br>

      </form>
    </div>
  )
}



/*import React from 'react';
//<a href="login.html">Login to Account</a>



            <label>
              <p>Username</p>
            </label>

class Login extends React.Component 
{
  render() {
    return (
      <body>
        <section class="hero is-link is-fullheight is-fullheight-with-navbar">
          <div class="hero-body">
            <div class="container has-text-centered">
              
              <h1 class="title">Welcome Back</h1>

              <div class="field">
                <p class="control has-icons-left has-icons-right">
                  <input class="input" type="email" placeholder="Email"></input>
                  <span class="icon is-small is-left">
                    <i class="fas fa-envelope"></i>
                  </span>
                  <span class="icon is-small is-right">
                    <i class="fas fa-check"></i>
                  </span>
                </p>
              </div>
              <div class="field">
                <p class="control has-icons-left">
                  <input class="input" type="password" placeholder="Password"></input>
                  <span class="icon is-small is-left">
                    <i class="fas fa-lock"></i>
                  </span>
                </p>
              </div>
              <div class="field">
                <p class="control">
                  <button class="button is-info is-success is-rounded ">
                    Login
                  </button> 
                </p>
              </div>
            </div>
          </div>
        </section>
      </body>
    );
  }
}

export default Login;
*/
