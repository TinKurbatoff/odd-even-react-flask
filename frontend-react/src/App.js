import React, { Component } from "react";
import axios from "axios";
import "./style.css";

class App extends Component {
  constructor(props) {
    super(props);
    this.apiBaseUrl = process.env.REACT_APP_BASE_URL? process.env.REACT_APP_BASE_URL : 'http://localhost:22045';
    this.state = {
      flag: false,
      stringValue: 'Drop anought Agoe!',
      textHighlights: 'Drop <mark>anought</mark> Agoe!',
      serverHighLights: '',
      maxStreakLength: 0,
    };
  }

  charCount = () => {
    const value = this.state.stringValue.length; 
    return (<>{value}</>);
    };

  onChange = (value) => {
    console.log(`CHAR COUNT ${this.state.stringValue.length}`);
    // const newValue = this.applyHighlights(value)
    // value=value.replace(/\n$/g, '&')
    axios
      .get(`${this.apiBaseUrl}/odd-even/?input=${value}`)
      .then((res) => this.setState({ serverHighLights: res.data, maxStreakLength: res.data.maxx }))
      .catch((err) => console.log(err));
    this.setState({
         stringValue: value,
         // textHighlights: newValue,
      });
    console.log(this.state.serverHighLights);
  };

  resetInput = () => {
    /* Reset input field */
    console.log(this.state.stringValue);
    this.setState({
         stringValue: '',
         serverHighLights: '',
    });
  };


  showHighlights = () => {
    /* Show highlight markdown  */
    const text = this.state.serverHighLights.markdown;
    console.log(text);
    return {__html: text}
  }

  showPerspective = () => {
    /* Show highlights underneath  */
    this.setState({flag: !this.state.flag});
    console.log(this.state.flag)
  };

  // Finally render
  render() {
    let containerState = this.state.flag ? 'container perspective' : 'container';
    let maxStreakLength = this.state.maxStreakLength
    return (
      <main className={containerState} >
        <h1 className="text-white text-uppercase text-center my-4">Odd Even</h1>
        <div className="row">
          <div className="col-ml-2 col-sm-10 mx-auto">
            {/* <div className="card p-3 "> */}
              <div className="mb-4">
                <button
                  className="btn btn-primary"
                  onClick={this.resetInput}
                >
                  Reset
                </button>
              </div>
                <div className="container">
                <label className="p-2">
                Streak counter
                </label>  
                  <div className="backdrop">
                    <div className="highlights" dangerouslySetInnerHTML={this.showHighlights()}></div>  
                  </div>
                  <textarea
                    name="inputField"
                    type="text"
                    value={this.state.stringValue}
                    onChange={(e) => this.onChange(e.target.value)}
                  />
                  </div>
                  <div className="mt-4 mb-0 p-2 ">
                    <label className="mt-2">Character Count: {this.charCount()}</label>&nbsp;</div>
                  <div className="mt-0 mb-0 p-2 ">  
                    <label className="mt-0 ml-8">Max streak length: {maxStreakLength}</label>
                  </div>
                  <p className="p-2"><em>BASE URL: {this.apiBaseUrl}</em></p>
                  <button
                    className="btn btn-info btn-sm"
                    onClick={this.showPerspective}
                  >
                    Split highlight
                  </button>                  
            </div>
          </div>
        {/* </div> */}
      </main>
    );
  }
}

export default App;