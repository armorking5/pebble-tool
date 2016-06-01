# encoding: utf-8
from __future__ import absolute_import, print_function, division

import os
import subprocess

from pebble_tool.exceptions import ToolError
from pebble_tool.util.versions import version_to_key


def check_npm():
    try:
        npm_version = subprocess.check_output(["npm", "--version"]).strip()
        if version_to_key(npm_version)[0] < 3:
            raise ToolError("We require npm3; you are using version {}.".format(npm_version))
    except subprocess.CalledProcessError:
        raise ToolError(u"You must have npm ≥ 3.0.0 available on your path.")


def invoke_npm(args):
    check_npm()
    subprocess.check_call(["npm"] + args)


def sanity_check():
    if not os.path.exists('node_modules'):
        return
    for d in os.listdir('node_modules'):
        if 'node_modules' in os.listdir(os.path.join('node_modules', d)):
            raise ToolError("Conflicting npm dependency in {}: {}. Please resolve before continuing."
                            .format(d, os.listdir(os.path.join('node_modules', d, 'node_modules'))[0]))
