import React from "react";
import Button from "@material-ui/core/Button";
import "./App.css";
import Home from "./Home";
import Tracks from "./Tracks";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";

function App() {
  return (
    <Router>
      <Switch>
        <Route path="/tracks">
          <Tracks />
        </Route>
        <Route path="/">
          <Home />
        </Route>
      </Switch>
    </Router>
  );
}

export default App;
