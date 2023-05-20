function showPlaceholder(id) {
    const placeholders = document.getElementsByClassName('control-placeholder');

    for (let i = 0; i < placeholders.length; i++) {
        if (placeholders[i].id === id) {
            placeholders[i].style.display = 'block';
        } else {
            placeholders[i].style.display = 'none';
        }
    }
}

function sendUserInput() {
    const userInput = document.getElementById('user-prompt').value;

    fetch('/user-text-input', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `user_input=${encodeURIComponent(userInput)}`,
    })
        .then((response) => response.json())
        .then((data) => {
            // Display the response message
            console.log(data.message);
            const storyTextArea = document.getElementById('story-text');
            console.log("storyTextArea: " + storyTextArea.value);
            storyTextArea.value += `\n${data.message}\n`;
        })
        .catch((error) => {
            console.error('Error sending user input:', error);
        });
}

function sendChoice(buttonId) {
    // Send the button ID to the Flask backend
    fetch('/your-choice-endpoint', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ choice: buttonId }),
    })
    .then((response) => response.json())
    .then((data) => {
        // Process the received data from the Flask backend (e.g., update the story text)
        console.log('Data received from Flask:', data);
    })
    .catch((error) => {
        console.error('Error sending data to Flask:', error);
    });

    // Disable all buttons after a choice is made
    const choiceButtons = document.getElementsByClassName('choice-button');
    for (let i = 0; i < choiceButtons.length; i++) {
        choiceButtons[i].disabled = true;
    }
}

function enableChoiceButtons() {
    const choiceButtons = document.getElementsByClassName('choice-button');
    for (let i = 0; i < choiceButtons.length; i++) {
        choiceButtons[i].disabled = false;
    }
}

function rollDice(dice) {
    fetch(`/your-dice-endpoint/${dice}`, {
        method: 'GET',
    })
    .then((response) => response.json())
    .then((data) => {
        // Update the corresponding text field with the dice roll result
        document.getElementById(`result-${dice}`).value = data.result;

        // // Disable all dice buttons after a roll is made
        // const diceButtons = document.getElementsByClassName('dice-button');
        // for (let i = 0; i < diceButtons.length; i++) {
        //     diceButtons[i].disabled = true;
        // }
    })
    .catch((error) => {
        console.error('Error rolling dice:', error);
    });
}

function enableDiceButtons() {
    const diceButtons = document.getElementsByClassName('dice-button');
    for (let i = 0; i < diceButtons.length; i++) {
        diceButtons[i].disabled = false;
    }
}

document.addEventListener('DOMContentLoaded', function() {
    // Initially show the first placeholder (the user input container)
    // showPlaceholder('user-input-container');
    // showPlaceholder('dice-container');
    showPlaceholder('choices-container');

    // Add a click event listener to the send button
    document.getElementById('send-button').addEventListener('click', sendUserInput);

	// Add click event listeners to the choice buttons
	const choiceButtons = document.getElementsByClassName('choice-button');
	for (let i = 0; i < choiceButtons.length; i++) {
		choiceButtons[i].addEventListener('click', function() {
			sendChoice(this.id);
		});
	}

	// Add click event listeners to the dice buttons
	// const diceButtons = document.getElementsByClassName('dice-button');
	// for (let i = 0; i < diceButtons.length; i++) {
	// 	diceButtons[i].addEventListener('click', function() {
	// 		rollDice(this.id.split('-')[1]);
	// 	});
	// }
    document.getElementById("roll-d6").addEventListener("click", () => {
        rollDice("d6");
      });
      
      document.getElementById("roll-d12").addEventListener("click", () => {
        rollDice("d12");
      });
      
      document.getElementById("roll-d20").addEventListener("click", () => {
        rollDice("d20");
      });
	// enableDiceButtons();
});