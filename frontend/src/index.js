import React from 'react';
import {BrowserRouter, Route, Routes} from 'react-router-dom';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App'; 
import reportWebVitals from './reportWebVitals';
//import ShowAcadPlanTbl from './ShowAcadPlanTbl';  // Most likely will remove later
import LandingPage from './LandingPage';
import Sidebar from './Sidebar';
import EnterClasses from './EnterClasses';


//removed for now - <ShowAcadPlanTbl/> -- add to LandingPage!

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <BrowserRouter>
    <Sidebar />
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/plan" element={<EnterClasses />} />
    </Routes>
  </BrowserRouter>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();