#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import logging

import requests

import click

from .base import Network

logger = logging.getLogger(__name__)

class Rest(Network):

    def send(self, data, *args, **kwargs):

        if not self.enabled:
            return { key : 'Network.Enabled=False' for key in data }

        network_errors = {}
        for key, value in data.iteritems():
            try:
                json_value = value

                response = requests.post(self.endpoint, json=json_value)

                if not response.status_code == 201:
                    network_errors[key] = response.status_code

            except Exception as err:
                network_errors[key] = err.message
                click.echo("[ {0} ] error : {1}".format(key, err.message))

        return network_errors

    def delete(self, id):
        try:
            url = "{0}{1}/".format(self.endpoint, id.strip())
            response = requests.delete(url)

            if not response.status_code == 204:
                raise Exception('STATUS CODE != 204')
        except Exception as err:
            # click.echo("[ {0} ] error deleting {1}".format(id, err.message))
            pass
