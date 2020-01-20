import React from "react";
import Button from "@material-ui/core/Button";
import "./App.css";

function Home() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Cloudmatch</h1>
        <Button
          variant="contained"
          color="inherit"
          style={{ backgroundColor: "#1DB954" }}
        >
          Login with Spotify
        </Button>
      </header>
    </div>
  );
}

export default Home;
