import React from "react";
import List from "@material-ui/core/List";
import ListItem from "@material-ui/core/ListItem";
import "./App.css";
import { Container } from "@material-ui/core";
import { withRouter } from "react-router-dom";

const axios = require("axios");

class Tracks extends React.Component {
  state = {
    tracks: []
  };

  componentDidMount() {
    const search = this.props.location.search;
    const params = new URLSearchParams(search);
    const auth_token = params.get("code");
    const code_payload = {
      grant_type: "authorization_code",
      code: auth_token,
      client_id: "569291be8d344a19b817ae7d5971d3bb",
      client_secret: "87fb0c27093d4e65a111510e1f3806f5",
      redirect_uri: "http://localhost:3000/tracks/callback"
    };
    axios
      .post("https://accounts.spotify.com/api/token", null, {
        params: code_payload,
        headers: { "Content-Type": "application/x-www-form-urlencoded" }
      })
      .then(response => {
        axios
          .get("http://127.0.0.1:8080/callback/q", {
            headers: { "Access-Control-Allow-Origin": "*" },
            params: { access_token: response.data.access_token }
          })
          .then(response => {
            const uniq = [...new Set(response.data.data)];
            const noStream = uniq.map(track => {
              return track.substring(0, track.length - 7);
            });
            this.setState({
              tracks: noStream
            });
            console.log(this.state.tracks);
          });
      })
      .catch(err => {
        console.log(err);
      });
  }

  render() {
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
              {this.state.tracks.map(track => {
                return (
                  <ListItem key={track} style={{ marginBottom: 2 }}>
                    <iframe
                      width="100%"
                      height="166"
                      scrolling="no"
                      frameBorder="no"
                      src={`https://w.soundcloud.com/player/?url=${track}&amp;color=0066cc`}
                    ></iframe>
                  </ListItem>
                );
              })}
            </List>
          </Container>
        </header>
      </div>
    );
  }
}

export default withRouter(Tracks);
