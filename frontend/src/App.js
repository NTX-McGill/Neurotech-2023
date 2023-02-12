import { useState } from "react";

function App(){
    const [count, setCount] = useState(0);

    const handleClick = () => {
    };
    return(
        <div>
            <button onClick={handleClick}>Start</button>
        </div>
    );
}

export default App;