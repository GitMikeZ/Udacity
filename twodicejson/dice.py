from flask import Flask, jsonify
app = Flask(__name__)

import json
import random


def rollDice():
    d = []
    for x in range(0, 10):
        d.append(random.randint(1, 6))
    return d

def dicetoJSON(num, values):
    return {
        'Dice number:' : num,
        'Dice values:' : values
    }

@app.route('/')
def diceJSON():
    dice1 = dicetoJSON(1, rollDice())
    dice2 = dicetoJSON(2, rollDice())
    dice = [dice1, dice2]
    return jsonify(Dice_Rolls = dice)


if __name__ == '__main__':
 app.debug = True
 app.run()
