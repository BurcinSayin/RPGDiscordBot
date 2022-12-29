from flask import Flask, jsonify
from flask import request

import lambda_function

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    local_event = {
        'headers': {}
    }
    for hdr in request.headers:
        print(hdr)
        local_event['headers'][hdr[0].lower()] = hdr[1]
    local_event['body'] = request.get_data().decode('utf-8')
    return lambda_function.lambda_handler(local_event, "")


if __name__ == '__main__':
    app.run()
