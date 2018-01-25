#!/usr/bin/env python3
from flask import Flask, request, jsonify
import uuid
import gym
import numpy as np
import six
import argparse
import sys
import json

from omni import Omni
import omni.core as core

import logging
logger = logging.getLogger('werkzeug')
logger.setLevel(logging.ERROR)

########## App setup ##########

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

########## Error handling ##########
class InvalidUsage(Exception):
    status_code = 400
    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

def get_required_param(json, param):
    if json is None:
        logger.info("Request is not a valid json")
        raise InvalidUsage("Request is not a valid json")
    value = json.get(param, None)
    if (value is None) or (value=='') or (value==[]):
        logger.info("A required request parameter '{}' had value {}".format(param, value))
        raise InvalidUsage("A required request parameter '{}' was not provided".format(param))
    return value

def get_optional_param(json, param, default):
    if json is None:
        logger.info("Request is not a valid json")
        raise InvalidUsage("Request is not a valid json")
    value = json.get(param, None)
    if (value is None) or (value=='') or (value==[]):
        logger.info("An optional request parameter '{}' had value {} and was replaced with default value {}".format(param, value, default))
        value = default
    return value

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

API_VERSION = "/v1/"

# Instantiate Omni
# =====================================================================================================================>

omni = Omni()

# Omni
# =====================================================================================================================>

@app.route(API_VERSION+'', methods=['POST'])
def instance_create():
    """
        Create an instance of interaction with omni

        Parameters:
            - config: the instances initial config
        Returns:
            - instance_id: a short identifier (such as '3c657dbc')
            for the created environment instance. The instance_id is
            used in future API calls to identify the instance to be
            manipulated
        """
    config = get_optional_param(request.get_json(), 'config', None)
    instance_id = omni.instantiate(config, direct=False)
    return jsonify(instance_id=instance_id)


@app.route(API_VERSION+'', methods=['GET'])
def omni_list_all():
    """
    List all instances running on the server

    Returns:
        - envs: dict mapping instance_id to env_id
        (e.g. {'3c657dbc': 'CartPole-v0'}) for every env
        on the server
    """
    all_instances = omni.list_instances()
    return jsonify(all_envs=all_instances)

@app.route(API_VERSION + 'omni/<instance_id>/reset/', methods=['POST'])
def instance_reset(instance_id):
    """
    Reset the state of the instance and return an initial
    observation.

    Parameters:
        - instance_id: a short identifier (such as '3c657dbc')
        for the instance
    Returns:
        - observation: the initial observation of the space
    """
    observation = omni.reset(instance_id)
    if np.isscalar(observation):
        observation = observation.item()
    return jsonify(observation = observation)

@app.route(API_VERSION + 'omni/<instance_id>/config/', methods=['POST'])
def instance_config(instance_id):
    return NotImplemented

@app.route(API_VERSION + 'omni/<instance_id>/interfaces/', methods=['POST'])
def instance_interfaces(instance_id):
    return NotImplemented

@app.route(API_VERSION + 'omni/<instance_id>/interfaces/', methods=['POST'])
def instance_options(instance_id):
    return NotImplemented

@app.route(API_VERSION + 'omni/<instance_id>/reset/', methods=['POST'])
def instance_spawn_candidates(instance_id):

    json = request.get_json()
    k = get_required_param(json, 'k')
    index = get_required_param(json, 'index')
    candidates = omni.spawn_candidates(instance_id, k, index)
    return jsonify(candidates=candidates)

@app.route(API_VERSION + 'omni/<instance_id>/step/', methods=['POST'])
def instance_step(instance_id):
    """
    Run one timestep of the environment's dynamics.

    Parameters:
        - instance_id: a short identifier (such as '3c657dbc')
        for the environment instance
        - action: an action to take in the environment
    Returns:
        - observation: agent's observation of the current
        environment
        - reward: amount of reward returned after previous action
        - done: whether the episode has ended
        - info: a dict containing auxiliary diagnostic information
    """
    json = request.get_json()
    index_action = get_required_param(json, 'index_action')
    param_action = get_required_param(json, 'param_action')
    [obs_jsonable, reward, done, info] = omni.step(instance_id, index_action, param_action)
    return jsonify(observation = obs_jsonable, reward = reward, done = done, info = info)

@app.route(API_VERSION + 'omni/<instance_id>/action_space/', methods=['GET'])
def instance_action_space_info(instance_id):
    """
    Get information (name and dimensions/bounds) of the env's
    action_space

    Parameters:
        - instance_id: a short identifier (such as '3c657dbc')
        for the environment instance
    Returns:
    - info: a dict containing 'name' (such as 'Discrete'), and
    additional dimensional info (such as 'n') which varies from
    space to space
    """
    info = omni.get_action_space_info(instance_id)
    return jsonify(info = info)


@app.route(API_VERSION + 'omni/<instance_id>/action_space/sample', methods=['GET'])
def instance_action_space_sample(instance_id):
    """
    Get a sample from the env's action_space

    Parameters:
        - instance_id: a short identifier (such as '3c657dbc')
        for the environment instance
    Returns:

    	- action: a randomly sampled element belonging to the action_space
    """
    action = omni.get_action_space_sample(instance_id)
    return jsonify(action=action)


@app.route(API_VERSION + 'omni/<instance_id>/action_space/contains/<x>', methods=['GET'])
def instance_action_space_contains(instance_id, x):
    """
    Assess that value is a member of the env's action_space

    Parameters:
        - instance_id: a short identifier (such as '3c657dbc')
        for the environment instance
	    - x: the value to be checked as member
    Returns:
        - member: whether the value passed as parameter belongs to the action_space
    """

    member = omni.get_action_space_contains(instance_id, x)
    return jsonify(member=member)

@app.route(API_VERSION + 'omni/<instance_id>/observation_space/contains', methods=['POST'])
def instance_observation_space_contains(instance_id):
    """
    Assess that the parameters are members of the env's observation_space

    Parameters:
        - instance_id: a short identifier (such as '3c657dbc')
        for the environment instance
    Returns:
        - member: whether all the values passed belong to the observation_space
    """
    j = request.get_json()
    member = omni.get_observation_space_contains(instance_id, j)
    return jsonify(member = member)

@app.route(API_VERSION + 'omni/<instance_id>/observation_space/', methods=['GET'])
def instance_observation_space_info(instance_id):
    """
    Get information (name and dimensions/bounds) of the env's
    observation_space

    Parameters:
        - instance_id: a short identifier (such as '3c657dbc')
        for the environment instance
    Returns:
        - info: a dict containing 'name' (such as 'Discrete'),
        and additional dimensional info (such as 'n') which
        varies from space to space
    """
    info = omni.get_observation_space_info(instance_id)
    return jsonify(info = info)

@app.route(API_VERSION + 'omni/<instance_id>/close/', methods=['POST'])
def instance_close(instance_id):
    """
    Manually close an instance

    Parameters:
        - instance_id: a short identifier (such as '3c657dbc')
          for the environment instance
    """
    omni.instance_close(instance_id)
    return ('', 204)

# Core
# =====================================================================================================================>

@app.route('/v1/core/count', methods=['POST'])
def count():
    """
    Assess that value is a member of the env's action_space

    Parameters:
        - instance_id: a short identifier (such as '3c657dbc')
        for the environment instance
	    - x: the value to be checked as member
    Returns:
        - member: whether the value passed as parameter belongs to the action_space
    """

    count = core.count()
    return jsonify(count=count)

@app.route('/v1/core/count', methods=['POST'])
def list_all_interfaces():
    """
    Assess that value is a member of the env's action_space

    Parameters:
        - instance_id: a short identifier (such as '3c657dbc')
        for the environment instance
	    - x: the value to be checked as member
    Returns:
        - member: whether the value passed as parameter belongs to the action_space
    """

    interfaces = core.list_all_interface_info()
    return jsonify(interfaces=interfaces)


# System
# =====================================================================================================================>

# todo: update config, confi help, reinitialization,


@app.route('/v1/config/', methods=['POST'])
def shutdown():
    """ Request a server shutdown - currently used by the integration tests to repeatedly create and destroy fresh copies of the server running in a separate thread"""
    f = request.environ.get('werkzeug.server.shutdown')
    f()
    return 'Server shutting down'

@app.route('/v1/config/help', methods=['POST'])
def shutdown():
    """ Request a server shutdown - currently used by the integration tests to repeatedly create and destroy fresh copies of the server running in a separate thread"""
    f = request.environ.get('werkzeug.server.shutdown')
    f()
    return 'Server shutting down'

@app.route('/v1/config/update', methods=['POST'])
def shutdown():
    """ Request a server shutdown - currently used by the integration tests to repeatedly create and destroy fresh copies of the server running in a separate thread"""
    f = request.environ.get('werkzeug.server.shutdown')
    f()
    return 'Server shutting down'


@app.route('/v1/shutdown/', methods=['POST'])
def shutdown():
    """ Request a server shutdown - currently used by the integration tests to repeatedly create and destroy fresh copies of the server running in a separate thread"""
    f = request.environ.get('werkzeug.server.shutdown')
    f()
    return 'Server shutting down'

@app.route('/v1/log', methods=['POST'])
def shutdown():
    """ Request a server shutdown - currently used by the integration tests to repeatedly create and destroy fresh copies of the server running in a separate thread"""
    f = request.environ.get('werkzeug.server.shutdown')
    f()
    return 'Server shutting down'



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Start a Gym HTTP API server')
    parser.add_argument('-l', '--listen', help='interface to listen to', default='127.0.0.1')
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to bind to')

    args = parser.parse_args()
    print('Server starting at: ' + 'http://{}:{}'.format(args.listen, args.port))
    app.run(host=args.listen, port=args.port)
























