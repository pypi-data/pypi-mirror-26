from __future__ import print_function
from time import sleep
# import random
import requests
import sys
import json

import russell
from russell.constants import LOADING_MESSAGES


def get_task_url(id,gpu):
    """
    Return the url to proxy to a running task
    """
    if gpu:
        return "{}/{}".format(russell.russell_gpu_host, id)
    else:
        return "{}/{}".format(russell.russell_cpu_host, id)


def get_module_task_instance_id(task_instances):
    """
    Return the first task instance that is a module node.
    """
    for id in task_instances:
        if task_instances[id] == 'module_node':
            return id
    return None


def get_mode_parameter(mode):
    """
    Map the mode parameter to the server parameter
    """
    if mode == 'job':
        return 'cli'
    elif mode == 'serve':
        return 'serving'
    else:
        return mode


def wait_for_url(url, status_code=200, sleep_duration_seconds=1, iterations=120, message_frequency=15):
    """
    Wait for the url to become available
    """
    for iteration in range(iterations):
        # if(iteration % message_frequency == 0):
        #     print("\n{}".format(random.choice(LOADING_MESSAGES)), end='', flush=True)

        # print(".", end='', flush=True)
        # print (url)
        response = requests.get(url)

        if response.status_code == status_code:
            # print(".", flush=True)
            return True
        sleep(sleep_duration_seconds)
    # print(".", flush=True)
    return False

def getPythonVersion():
    if sys.version_info < (3, 0):
        return 2
    else:
        return 3

def py2code():
    if getPythonVersion() == 2:
        import sys
        reload(sys)
        sys.setdefaultencoding('utf-8')