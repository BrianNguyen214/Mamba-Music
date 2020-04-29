import React from 'react';
import App from './App';
import NavigationBar from './nav';
import { Jumbotron, Container } from 'reactstrap';

import "./Home.css";
import Player from './Player';

class Home extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      userDetails: {},
      isUserLoggedIn: false,
      musicInfo: null,
      currentMusicIndex: 0,
      changeRadioIndex: null,
    };

    this.handleUserLoggedInInfo = this.handleUserLoggedInInfo.bind(this);
    this.handleUserDetails = this.handleUserDetails.bind(this);
    this.handleMusicInfo = this.handleMusicInfo.bind(this);
    this.handleCurrentMusicIndex = this.handleCurrentMusicIndex.bind(this);
    this.handleChangeRadioIndex = this.handleChangeRadioIndex.bind(this);
  }

  UNSAFE_componentWillReceiveProps() {
    this.forceUpdate()
  }

  handleUserLoggedInInfo(resp) {
    this.setState({ isUserLoggedIn: resp })
  }

  handleUserDetails(resp) {
    this.setState({ userDetails: resp })
  }

  handleMusicInfo(resp) {
    this.setState({ musicInfo: resp })
  }

  handleCurrentMusicIndex(resp) {
    this.setState({ currentMusicIndex: resp })
  }

  handleChangeRadioIndex(resp) {
    this.setState({ changeRadioIndex: resp })
  }

  render() {
    const {userDetails, isUserLoggedIn, musicInfo, currentMusicIndex, changeRadioIndex} = this.state
    return (
        <div>
            <NavigationBar userInfoOne={this.handleUserLoggedInInfo} userInfoTwo={this.handleUserDetails} />
            {isUserLoggedIn && (
              <div>
                <App deets={userDetails} musicDeets={musicInfo} currentMusic={currentMusicIndex} chooseRadio={this.handleChangeRadioIndex}/>
              </div>
            )}

            {!isUserLoggedIn && (
              <Container>
                <Jumbotron className="goodStyle">
                  <h1 className="display-3">Welcome to Mamba Music!</h1>
                  <p className="lead">Click the play button below to play music generated by a machine.</p>
                  <hr className="my-2" />
                  <p>For personalized music, please login using Google.</p>
                  <p className="lead">
                  </p>
                </Jumbotron>   
              </Container>
            )}

          <div className="footerPadding"/>
          <Player isUserLoggedIn={isUserLoggedIn} userInfo={userDetails} musicInfo={this.handleMusicInfo} currentMusic={this.handleCurrentMusicIndex} changeRadio={changeRadioIndex}/>
      </div>
    )
  }
}

export default Home;