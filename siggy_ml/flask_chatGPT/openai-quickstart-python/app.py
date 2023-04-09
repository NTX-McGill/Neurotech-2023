import os

import openai
from flask import Flask, redirect, render_template, request, url_for, jsonify, make_response

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        words = request.json["words"]
        context = request.json["context"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(words, context),
            temperature=1,
            max_tokens=2048
        )
        text_response = response.choices[0].text
        return make_response(text_response)
    
    return "", 204

def generate_prompt(words, context):
    prompt = f'''Say I'm learning a new language and I've categorized all the words in a given text that I don't understand. 
    I want you to take the list of words I did not understand and provide definitions and example sentences for each of the following words given the context. 
    Context: {context} Words:\n
    Format of the output should be a list of words 
    '''
    for word in words:
        prompt += f"* {word}\n"
    return prompt