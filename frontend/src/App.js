import { useState } from "react";
import ShowWord from "./components/ShowWord";
// import text from "./data/single_words_easy.txt"
import text from "./data/may/400/inco_session0.txt"


function App(){
    const [appState, setStart] = useState(false);


    const handleClick = () => {
      
        //connect.connectToBackend();
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
                appState && <ShowWord file={text} delay={200}/> 
            }
                       
        </div>
    );
}

export default App;