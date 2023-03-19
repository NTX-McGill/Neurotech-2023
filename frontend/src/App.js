import { useState } from "react";
import ShowWord from "./components/ShowWord";
// import text from "./data/single_words_easy.txt"
import text from "./data/wordsbwords.txt"
import connect from "./components/connect";

function App(){
    const [appState, setStart] = useState(false);


    const handleClick = () => {
      
        connect.connectToBackend();
        setStart(!appState);
    };

    // fetch(text)
    // .then(r => r.text())
    // .then(text => {
    //     console.log('text decoded:', text);
    // });

    return(
        <div>
            <button onClick={handleClick}>Start</button>
            {
                // appState && <ShowWord word="Hello"/> 
                appState && <ShowWord file={text} delay={1000}/> 
            }
                       
        </div>
    );
}

export default App;