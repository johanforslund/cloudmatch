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
          href="https://accounts.spotify.com/authorize?client_id=569291be8d344a19b817ae7d5971d3bb&redirect_uri=http:%2F%2Flocalhost:3000%2Ftracks%2Fcallback&scope=user-top-read&response_type=code"
        >
          Login with Spotify
        </Button>
      </header>
    </div>
  );
}

export default Home;
