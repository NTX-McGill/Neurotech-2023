import { useState } from "react";
import ShowWord from "./components/ShowWord";

function App(){
    const [appState, setStart] = useState(false);

    const handleClick = () => {
        setStart(true);
    };
    return(
        <div>
            <button onClick={handleClick}>Start</button>
            {
                appState && <ShowWord word="Hello"/> 
            }
                       
        </div>
    );
}

export default App;