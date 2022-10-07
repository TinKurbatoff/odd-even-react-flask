import React, { Component } from "react";
import axios from "axios";
import "./style.css";

const todoItems = [];

class CharacterBox extends React.Component {
  render() {
    return (
      <div>Character Count:{this.props.charCount}</div>
    )
  }
}

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      flag: false,
      stringValue: 'Drop anought Agoe!',
      textHighlights: 'Drop <mark>anought</mark> Agoe!',
      serverHighLights: '',
    };
  }

  charCount = () => {
    const value = this.state.stringValue.length; 
    return (<label> {value} </label>);
    };

  onChange = (value) => {
    console.log(`CHAR COUNT ${this.state.stringValue.length}`);
    // const newValue = this.applyHighlights(value)
    axios
      .get(`https://1axm.com/odd-even/?input=${value}`)
      .then((res) => this.setState({ serverHighLights: res.data }))
      .catch((err) => console.log(err));
    this.setState({
         stringValue: value,
         // textHighlights: newValue,
      });
    console.log(this.state.serverHighLights);
  };

  resetInput = () => {
    console.log(this.state.stringValue);
    this.setState({
         stringValue: '',
         serverHighLights: '',
    });
    // this.state.stringValue = '';
  };

//   applyHighlights = (text) => {
//     text = text
//       .replace(/\n$/g, '')
//       .replace(/[A-Z].*?\b/g, '<mark>$&</mark>');
//     return text;
// 
//   }

  showHighlights = () => {
    // const text = this.applyHighlights(this.state.stringValue);
    const text = this.state.serverHighLights.markdown;
    console.log(text);
    return {__html: text}
  }

  showPerspective = () => {
  this.setState({flag: !this.state.flag});
  console.log(this.state.flag)
  };

  // Finally render
  render() {
    let containerState = this.state.flag ? 'container perspective' : 'container';
    return (
      <main className={containerState} >
        <h1 className="text-white text-uppercase text-center my-4">Odd Even</h1>
        <div className="row">
          <div className="col-md-6 col-sm-10 mx-auto p-0">
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
                  <div className="mt-4 p-2"><label className="mt-4">Character Count: {this.charCount()}</label></div>
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