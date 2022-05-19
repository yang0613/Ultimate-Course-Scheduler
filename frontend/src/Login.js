
import React from 'react';

//<a href="login.html">Login to Account</a>

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

