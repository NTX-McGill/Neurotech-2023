const express = require('express');
const openai = require('openai');
const app = express();

// Replace YOUR_API_KEY with your OpenAI API key
const openaiAPIKey = 'YOUR_API_KEY';
const gpt3Config = {
  apiKey: openaiAPIKey,
  model: 'text-davinci-002',
  temperature: 0.5,
  maxTokens: 1024,
  n: 1,
  stop: '\n'
};

// Set up a route to handle the API request
app.get('/api/chatgpt', async (req, res) => {
  const prompt = `Say I'm learning a new language and I've categorized all the words in a given text that I don't understand. I want you to take the list of words I did not understand and output feedback. This feedback should categorize my weakness (for example, but not limited to: is there a common theme  in the kinds of words I did not understand? Perhaps I struggle with semantics, maybe I struggle with slang/informal language). Additionally, for each word given in the list, I want you to give a definition and use it in a sentence.
    Words:
    - deliberate
    - merely
    - chunks
    - mastering`;

  try {
    // Generate a response using the OpenAI API
    const result = await openai.complete({ ...gpt3Config, prompt });
    const response = result.data.choices[0].text;

    // Send the response back to the client
    res.send(response);
  } catch (error) {
    console.log(error);
    res.status(500).send('Error generating response');
  }
});

// Start the Express server
const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});