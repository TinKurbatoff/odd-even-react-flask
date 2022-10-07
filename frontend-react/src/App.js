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
    };
  }

  charCount = () => {
    // return this.state.stringValue.length;
    const value = this.state.stringValue; //.replace(/[A-Z].*?\b/g, '<mark></mark>')
    // this.setState({
    //      stringValue: value, 
    // });
    // this.state.stringValue = '2121';
    return (<label> {this.state.stringValue.length} </label>);
    };

  onChange = (value) => {
    // this.state.stringValue = value
    console.log(`CHAR COUNT ${this.state.stringValue.length}`);
    const newValue = this.applyHighlights(value)
    
    this.setState({
         stringValue: value,
         // textHighlights: newValue,
    });

  };

  resetInput = () => {
    console.log(this.state.stringValue);
    this.setState({
         stringValue: 'ha-ha'
    });
    // this.state.stringValue = '';
  };

  applyHighlights = (text) => {
    text = text
      .replace(/\n$/g, '\n\n')
      .replace(/[A-Z].*?\b/g, '<mark>$&</mark>');
        
    return text;
  }


  render() {
    return (
      <main className="container">
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
                    <div className="highlights">Drop <mark>anought</mark> Agoe!</div>
                  </div>  
                  <textarea
                    name="inputField"
                    type="text"
                    value={this.state.stringValue}
                    onChange={(e) => this.onChange(e.target.value)}
                  />
                  </div>
                  <div className="mt-4 p-2"><label className="mt-4">Character Count: {this.charCount()}</label></div>
                  {/* <CharacterBox charCount={this.props.value}/> */}
                
            </div>
          </div>
        {/* </div> */}
      </main>
    );
  }
}

export default App;