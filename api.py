from __future__ import unicode_literals
import json
import logging

from flask import Flask, request
app = Flask(__name__)


logging.basicConfig(level=logging.DEBUG)
sessionStorage = {}
@app.route("/", methods=['POST'])


def main():
    logging.info('Request: %r', request.json)

    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        "response": {
            "end_session": False
        }
    }

    handle_dialog(request.json, response)

    logging.info('Response: %r', response)

    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )

def handle_dialog(req, res):
    user_id = req['session']['user_id']
    if req['session']['new']:
        res['response']['text'] = 'Привет!'
        return

    if req['request']['original_utterance'].lower() == 'алиса, найди значение выражения':
        res['response']['text'] = 'Введите ваше выражение'
        a = True
        return
    b = req['request']['original_utterance'].split()
    res['response']['text'] = b
    t = 0
    for i in range(len(b)):
        if b[i] == '(':
            for i in range(len(b)):
                k = i
                for j in range(len(b)):
                    if b[j] == '(' and b[j + 2] == ')':
                        b.pop(j)
                        b.pop(j + 1)
                        t += 1
                        break
                if t == 1:
                    break
                if b[i] == '(':
                    while '*' in b or '/' in b or ':' in b:
                        if b[i] == ')':
                            break
                        if b[i] == '*':
                            b[i] = int(b[i - 1]) * int(b[i + 1])
                            b.pop(i - 1)
                            b.pop(i)
                            print(1)
                            i -= 2
                        if b[i] == '/' or b[i] == ':':
                            b[i] = int(b[i - 1]) / int(b[i + 1])
                            b.pop(i - 1)
                            b.pop(i)
                            i -= 2  
                        i += 1
                i = k
                while '+' in b or '-' in b:
                    if b[i] == ')':
                        break
                    if b[i] == '+':
                        b[i] = int(b[i - 1]) + int(b[i + 1])
                        b.pop(i - 1)
                        b.pop(i)
                        i -= 2
                    if b[i] == '-':
                        b[i] = int(b[i - 1]) - int(b[i + 1])
                        b.pop(i - 1)
                        b.pop(i)
                        i -= 2
                    i += 1  
                i = 0
        break
    while '*' in b or '/' in b or ':' in b:
        if b[i] == '*':
            b[i] = int(b[i - 1]) * int(b[i + 1])
            b.pop(i - 1)
            b.pop(i)
            i -= 2
        if b[i] == '/' or b[i] == ':':
            b[i] = int(b[i - 1]) / int(b[i + 1])
            b.pop(i - 1)
            b.pop(i)
            i -= 2
        i += 1
    i = 0
    while '+' in b or '-' in b:
        if b[i] == '+':
            b[i] = int(b[i - 1]) + int(b[i + 1])
            b.pop(i - 1)
            b.pop(i)
            i -= 2
            print(b[i], i)
        if b[i] == '-':
            b[i] = int(b[i - 1]) - int(b[i + 1])
            b.pop(i - 1)
            b.pop(i)
            i -= 2
        i += 1
    res['response']['text'] = b[0]
    return

if __name__ == '__main__':
    app.run()