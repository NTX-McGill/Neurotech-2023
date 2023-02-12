import React, { useState, useEffect, useRef } from 'react';

function ShowWord({file, delay}){
    // Initialize wordArray to store words that will flash on screen
    var wordArray = []

    // Read from the file and populate the wordArray
    fetch(file)
    .then(r => r.text())
    .then(text => {
        wordArray = text.split("\n");
    });


    // Set the state to allow for flashing words
    const [currWord, setCurrWord] = useState(wordArray[0]);
	const [isActive, setIsActive] = useState(true);

	const index = useRef(0);

    // Flashing word effect
	useEffect(() => {
		let interval = null;
		if (isActive) {
			interval = setInterval(() => {
				index.current++;
				setCurrWord(wordArray[index.current]);
				if (index.current === wordArray.length - 1) {
					setIsActive(false);
				}
			}, delay); // Sets the time interval in milliseconds
		}
		return () => clearInterval(interval);
	});

    // Returns the word in a styled fashion
	return (
		<div style={{textAlign: "center"}}>
			<h1>{currWord}</h1>
		</div>
	);
}

export default ShowWord;