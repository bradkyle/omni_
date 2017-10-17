import json
from flask import jsonify
import numpy as np
import requests
import time
from omni.config import LINE_LENGTH,PADDING_CHAR,CHAR_EMBEDDING, BAD_REQUEST_PENALTY, SAVE_REQUEST

f = open("./store.json", "a+")

def invoke(method, url, headers=None, body=None, params=None, cached=False, cache_length=None, request=None):
    session = requests.Session()

    # todo if url host is unique create new, if url

    req = requests.Request(method, url, params=params, headers=headers, data=body)
    prepared = req.prepare()

    if SAVE_REQUEST:
        request = {}
        request["instance"] = []
        request["file"] = '{}\n{}\n{}\n\n{}'.format(
            '-----------START-----------',
            prepared.method + ' ' + prepared.url,
            '\n'.join('{}: {}'.format(k, v) for k, v in prepared.headers.items()),
            prepared.body,
        )
        request["time"] = time.time()
        f.write(jsonify(request))

    #response_object = session.get(url, params=params, timeout=DEFAULT_TIMEOUT)
    response_object = session.send(prepared)

    try:
        if response_object.status_code != 200:
            penalty = BAD_REQUEST_PENALTY
        else:
            penalty = 0
        response = json.loads(response_object.text)
        print(json.dumps(response))
    except requests.exceptions.RequestException as e:
        return e

    observation = encode(response)

    return observation, penalty

# todo implement in cython
def encode(observation):
    """
    Encodes the observation response with a char embedding
    that is the same across all instances.
    """
    result = []
    for line in observation:
        line = list(line)
        if len(line) > LINE_LENGTH:
            line = line[-LINE_LENGTH:]
        num_padding = LINE_LENGTH - len(line)
        output_line = line + [PADDING_CHAR] * num_padding

        result.append(np.array([CHAR_EMBEDDING.find(char) for char in output_line], dtype=np.int8))

    return result

def convert(input, condition, output):
    """takes in a float int and turns it into a value based upon a second parameter"""
    return NotImplemented