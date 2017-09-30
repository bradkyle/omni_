import requests
import six.moves.urllib.parse as urlparse
import json
import os

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Client(object):
    """
    Gym client to interface with gym_http_server
    """

    def __init__(self, remote_base):
        self.remote_base = remote_base
        self.session = requests.Session()
        self.session.headers.update({'Content-type': 'application/json'})

    def _parse_server_error_or_raise_for_status(self, resp):
        j = {}
        try:
            j = resp.json()
        except:
            # Most likely json parse failed because of network error, not server error (server
            # sends its errors in json). Don't let parse exception go up, but rather raise default
            # error.
            resp.raise_for_status()
        if resp.status_code != 200 and "message" in j:  # descriptive message from server side
            raise ServerError(message=j["message"], status_code=resp.status_code)
        resp.raise_for_status()
        return j

    def _post_request(self, route, data):
        url = urlparse.urljoin(self.remote_base, route)
        logger.info("POST {}\n{}".format(url, json.dumps(data)))
        resp = self.session.post(urlparse.urljoin(self.remote_base, route),
                                 data=json.dumps(data))
        return self._parse_server_error_or_raise_for_status(resp)

    def _get_request(self, route):
        url = urlparse.urljoin(self.remote_base, route)
        logger.info("GET {}".format(url))
        resp = self.session.get(url)
        return self._parse_server_error_or_raise_for_status(resp)

    def instance_create(self, seed=None):
        route = '/v1/inst/'
        data = {'seed': seed}
        resp = self._post_request(route, data)
        instance_id = resp['instance_id']
        return instance_id

    def instance_reset(self, instance_id):
        route = '/v1/inst/{}/reset/'.format(instance_id)
        resp = self._post_request(route, None)
        observation = resp['observation']
        return observation

    def env_step(self, instance_id, action):
        route = '/v1/omni/{}/step/'.format(instance_id)
        data = {'action': action}
        resp = self._post_request(route, data)
        observation = resp['observation']
        reward = resp['reward']
        done = resp['done']
        info = resp['info']
        return [observation, reward, done, info]

    def env_action_space_info(self, instance_id):
        route = '/v1/omni/{}/action_space/'.format(instance_id)
        resp = self._get_request(route)
        info = resp['info']
        return info

    def env_action_space_sample(self, instance_id):
        route = '/v1/omni/{}/action_space/sample'.format(instance_id)
        resp = self._get_request(route)
        action = resp['action']
        return action

    def env_action_space_contains(self, instance_id, x):
        route = '/v1/omni/{}/action_space/contains/{}'.format(instance_id, x)
        resp = self._get_request(route)
        member = resp['member']
        return member

    def env_observation_space_info(self, instance_id):
        route = '/v1/omni/{}/observation_space/'.format(instance_id)
        resp = self._get_request(route)
        info = resp['info']
        return info

    def env_observation_space_contains(self, instance_id, params):
        route = '/v1/omni/{}/observation_space/contains'.format(instance_id)
        resp = self._post_request(route, params)
        member = resp['member']
        return member

    def instance_close(self, instance_id):
        route = '/v1/omni/{}/close/'.format(instance_id)
        self._post_request(route, None)

    def shutdown_server(self):
        route = '/v1/shutdown/'
        self._post_request(route, None)


class ServerError(Exception):
    def __init__(self, message, status_code=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code


if __name__ == '__main__':
    remote_base = 'http://omni:5000'
    client = Client(remote_base)

    # Create environment
    instance_id = client.instance_create()

    # Check properties
    action_info = client.env_action_space_info(instance_id)
    obs_info = client.env_observation_space_info(instance_id)

    # Run a single step
    init_obs = client.instance_reset(instance_id)
    [observation, reward, done, info] = client.env_step(instance_id, 1)