from flask import Flask, jsonify, request
from flask_cors import CORS
from random import choice

app = Flask(__name__)
CORS(app, origins="*") 

targetWord = ''

## gets a word to be guessed by the player
@app.route("/wordle/word", methods=['GET'])
def getWord():
    global targetWord
    with open("wordleBank.txt", 'r') as file: 
        words = file.read().splitlines()
        file.close()
    targetWord = choice(words)
    return jsonify({'word': targetWord.strip().upper()})

## checks player's guess against the word
@app.route("/wordle/check", methods=['POST'])
def checkWord():
    global targetWord
    data = request.get_json()
    guess = data.get('guess')
    feedback = getFeedback(guess, targetWord)
    return jsonify({"feedback": feedback})

def getFeedback(guess, targetWord):
    feedback = []
    for i in range(5):
        if guess[i] == targetWord[i]:
            feedback.append('success.light')
        elif guess[i] in targetWord:
            feedback.append('warning.light') 
        else:
            feedback.append('#aaa') 
    return feedback

## gets a guess word for the player
@app.route("/wordle/random", methods=['GET'])
def getRandom():
    with open("guessBank.txt", 'r') as file:
        words = file.read().splitlines()
        file.close()
    randGuess = choice(words)
    return jsonify({'random': randGuess.strip().upper()})


if __name__ == '__main__':
    app.run()
