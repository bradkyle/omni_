import json
import numpy as np
import requests
import time
from omni.config import LINE_LENGTH,PADDING_CHAR,CHAR_EMBEDDING, BAD_REQUEST_PENALTY, SAVE_REQUEST, ACTION_LOW, ACTION_HIGH

f = open("./store.json", "a+")

def invoke(method, url, headers=None, body=None, params=None, payload=None, session=None, encode=True):

    if session is None:
        session = requests.Session()

    # todo caching requests
    # todo penalty for response size

    req = requests.Request(method, url, params=params, headers=headers, data=body)
    prepared = req.prepare()

    if SAVE_REQUEST:
        r = {}
        r["method"] = prepared.method
        r["url"] = prepared.url
        r["headers"] = {}
        for k, v in prepared.headers.items():
            r["headers"][str(k)] = str(v)
        r["body"] = prepared.body
        r["time"] = time.time()
        if payload:
            r["payload"] = payload
        json_request = json.dumps(r)
        f.write(json_request)

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

    if encode:
        observation = encode_response(response)
    else:
        observation = response

    return observation, penalty

# todo penalty for size of data
def encode_response(observation):
    """
    Encodes the observation response with a char embedding
    that is the same across all instances.
    """
    result = []
    for line in observation:
        line = list(str(line))
        if len(line) > LINE_LENGTH:
            line = line[-LINE_LENGTH:]
        num_padding = LINE_LENGTH - len(line)
        output_line = line + [PADDING_CHAR] * num_padding

        result.append(np.array([CHAR_EMBEDDING.find(char) for char in output_line], dtype=np.int8))

    return result

def convert(input, condition, output):
    """takes in a float int and turns it into a value based upon a second parameter"""




    return NotImplemented