from happytransformer import HappyTextToText, TTSettings

happy_tt = HappyTextToText("T5", "vennify/t5-base-grammar-correction")

from flask import Flask, request, abort
import json

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return 'LAST UPDATED: 8:00PM - 10/24/2022'


@app.route('/check-grammar', methods=['GET'])
def check_grammar():
    try:
        args = request.args
        if args['payload'] == 'undefined':
            raise ValueError('Payload is not found!')
        payload = json.loads(args['payload'])
        if payload['text'] == 'undefined':
            raise ValueError('Text is not found!')
        text = payload['text']
        if len(text) > 500:
            raise ValueError('Text is too long!')
        result = happy_tt.generate_text("grammar: " + text, args=TTSettings(num_beams=5, min_length=1, max_length=1024))
        return json.dumps({ "text": result.text });
    except Exception:
        abort(400)