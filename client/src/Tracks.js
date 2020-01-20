import React from "react";
import List from "@material-ui/core/List";
import ListItem from "@material-ui/core/ListItem";
import ListItemText from "@material-ui/core/ListItemText";
import Grid from "@material-ui/core/Grid";
import "./App.css";
import { Container } from "@material-ui/core";

function Tracks() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Cloudmatch</h1>
        <Container maxWidth="md">
          <List
            style={{
              backgroundColor: "#00000050",
              width: "100%",
              borderRadius: 20
            }}
          >
            <ListItem style={{ marginBottom: 2 }}>
              <iframe
                width="100%"
                height="166"
                scrolling="no"
                frameborder="no"
                src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/34019569&amp;color=0066cc"
              ></iframe>
            </ListItem>
            <ListItem style={{ marginBottom: 2 }}>
              <iframe
                width="100%"
                height="166"
                scrolling="no"
                frameborder="no"
                src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/34019569&amp;color=0066cc"
              ></iframe>
            </ListItem>
          </List>
        </Container>
      </header>
    </div>
  );
}

export default Tracks;
