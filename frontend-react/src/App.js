import React, { useState } from "react";
import axios from "axios";
import "./style.css";

const App = (props) => {  
  const apiBaseUrl = process.env.REACT_APP_BASE_URL? process.env.REACT_APP_BASE_URL : 'http://localhost:22045';
  const [flag, setFlag] = useState(false);
  const [stringValue, setStringValue] = useState('Drop anought Agoe!');
  const [textHighlights, setTextHighlights] = useState('Drop <mark>anought</mark> Agoe!');
  const [serverHighLights, setServerHighLights] = useState('');
  const [maxStreakLength, setMaxStreakLength] = useState(0);
  
  const onChange = (value) => {
    console.log(`CHAR COUNT ${stringValue.length}`);
    // const newValue = this.applyHighlights(value)
    // value=value.replace(/\n$/g, '&')
    axios
      .get(`${apiBaseUrl}/odd-even/?input=${value}`)
      .then((res) => {
        setServerHighLights(res.data)
        setMaxStreakLength(res.data.maxx)
        })
      .catch((err) => console.log(`🚨🚨  BACKEND ERROR: ${err.message}`))
    setStringValue(value)
    console.log(serverHighLights)
    }

  const resetInput = () => {
    /* Reset input field */
    console.log(stringValue);
    setStringValue('');
    setServerHighLights('');
  }

  const charCount = () => {
    const value = stringValue.length; 
    return (<>{value}</>);
    };


  const showHighlights = () => {
    /* Show highlight markdown  */
    const text = serverHighLights.markdown;
    console.log(text);
    return {__html: text}
  }

  const showPerspective = () => {
    /* Show highlights underneath  */
    setFlag(!flag)
    console.log(flag)
  }

  // Finally render
  return (() => {
      let containerState = flag ? 'container perspective' : 'container';
      return (
        <main className={containerState} >
          <h1 className="text-white text-uppercase text-center my-4">Odd Even</h1>
          <div className="row">
            <div className="col-ml-2 col-sm-10 mx-auto">
              {/* <div className="card p-3 "> */}
                <div className="mb-4">
                  <button
                    className="btn btn-primary"
                    onClick={resetInput}
                  >
                    Reset
                  </button>
                </div>
                  <div className="container">
                  <label className="p-2">
                  Streak counter
                  </label>  
                    <div className="backdrop">
                      <div className="highlights" dangerouslySetInnerHTML={showHighlights()}></div>  
                    </div>
                    <textarea
                      name="inputField"
                      type="text"
                      value={stringValue}
                      onChange={(e) => onChange(e.target.value)}
                    />
                    </div>
                    <div className="mt-4 mb-0 p-2 ">
                      <label className="mt-2">Character Count: {charCount()}</label>&nbsp;</div>
                    <div className="mt-0 mb-0 p-2 ">  
                      <label className="mt-0 ml-8">Max streak length: {maxStreakLength}</label>
                    </div>
                    <p className="p-2"><em>BASE URL: {apiBaseUrl}</em></p>
                    <button
                      className="btn btn-info btn-sm"
                      onClick={showPerspective}
                    >
                      Split highlight
                    </button>                  
              </div>
            </div>
          {/* </div> */}
        </main>
      );
    })();

}

export default App;