#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2018  Jun Makii <junmakii@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""

umuus-websockets-notification
=============================

Installation
------------

    $ pip install git+https://github.com/junmakii/umuus-websockets-notification.git

Example
-------

    $ umuus_websockets_notification

    >>> import umuus_websockets_notification

Usage
-----

twitter-oauth.json::

    {
        "client_key": "XXXXXXXXXXXXXXXXXXXXXXXXX",
        "client_secret": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        "access_token": "XXXXXXXXXX-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        "access_token_secret": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    }

docker-compose.yml::

    services:
      umuus_twitter_websockets_notification:
        image: "umuus-twitter-websockets-notification:0.1"
        command: ["run", "--host", '"0.0.0.0"', "--port", "8888", "--twitter_config", "/app/config/twitter-oauth.json"]
        volumes:
          - "twitter-oauth.json:/app/config/twitter-oauth.json"
        ports:
          - "8888:8888"

Client
------

    <script>
      function UmuusWebsocketsNotification() {
	  this.address = 'ws://' + 'localhost' + ':' + '8888';
	  console.log('UmuusWebsocketsNotification is called: ' + this.address);
	  this.socket = new ReconnectingWebSocket(this.address, ['protocol1', 'protocol2'], {debug: true, reconnectInterval: 1000});

	  this.socket.addEventListener(
	      'message', 
	      function(event){
		  const data = JSON.parse(event.data).data;
		  new Notification(data.title, data.options);
	      });
	  
	  this.socket.addEventListener(
	      'close',
	      function(event){
		  console.log('Connection has closed.');
	      });
      }
      
      window.addEventListener('load', function() { new UmuusWebsocketsNotification(); });
    </script>

Authors
-------

- Jun Makii <junmakii@gmail.com>

License
-------

GPLv3 <https://www.gnu.org/licenses/>

"""
# -- Import --
import os
import sys
import json
import typing
import functools
import attr
import logging
logger = logging.getLogger(__name__)
import fire
import os
import datetime
import asyncio
import websockets
import json
import jmespath
import tweepy
import re
import peewee
# -- End BaseImport --
# -- Metadata --
__version__ = '0.1'
__url__ = 'https://github.com/junmakii/umuus-twitter-websockets-notification'
__author__ = 'Jun Makii'
__author_email__ = 'junmakii@gmail.com'
__keywords__ = []
__license__ = 'GPLv3'
__scripts__ = []
__install_requires__ = [
    'fire',
    'attrs',
    'addict',
    'requests',
    'jmespath',
    'tweepy==3.7.0',
    # 'pymongo',
    'peewee',
    'websockets',
]
__dependency_links__ = [
    # 'git+https://github.com/junmakii/umuus-utils.git#egg=umuus_utils-1.0',
]
__classifiers__ = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Natural Language :: English',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
]
__entry_points__ = {
    'console_scripts': [
        'umuus_twitter_websockets_notification = umuus_twitter_websockets_notification:main'
    ],
    'gui_scripts': [],
}
__project_urls__ = {
    'Bug Tracker':
    'https://github.com/junmakii/umuus-twitter-websockets-notification/issues',
    'Documentation':
    'https://github.com/junmakii/umuus-twitter-websockets-notification/',
    'Source Code':
    'https://github.com/junmakii/umuus-twitter-websockets-notification/',
}
__setup_requires__ = ['pytest-runner']
__test_suite__ = 'umuus_twitter_websockets_notification'
__tests_require__ = ['pytest']
__extras_require__ = {}
__package_data__ = {'': []}
__python_requires__ = '>=3.0.0'
__include_package_data__ = True
__zip_safe__ = True
__static_files__ = {}
__extra_options__ = {
    'docker_requires': [
        'ca-certificates',
        'python3',
        'python3-dev',
    ],
    'docker_cmd': [],
}
# -- End Metadata --
# -- Extra --
umuus_twitter_websockets_notification = __import__(__name__)
# -- End Extra --

base_database = peewee.SqliteDatabase(None)


class BaseModel(peewee.Model):
    class Meta:
        database = base_database


class Data(BaseModel):
    id = peewee.AutoField()
    data_id = peewee.CharField(unique=True)
    body = peewee.TextField()
    created_at = peewee.DateTimeField(default=datetime.datetime.now)


@attr.s()
class UmuusTwitterWebsocketsNotification(object):
    host = attr.ib('0.0.0.0')
    port = attr.ib(8024)
    twitter_config = attr.ib(None, converter=lambda _: json.load(open(_)))
    twitter_auth = attr.ib(None)
    twitter_api = attr.ib(None)
    connections = attr.ib(factory=lambda: set())
    timelines = attr.ib([
        'junmakii/news-en', 'ftraversin/python-universe',
        'joncutrer/python-developers'
    ],
                        converter=lambda _: [i.split('/', 1) for i in _])
    database_file = attr.ib('/tmp/' + os.path.basename(__file__) + '.sqlite')

    # collection = attr.ib(None)
    # mongodb_options = attr.ib({
    #     'host': 'mongodb',
    #     'port': 27017,
    #     'username': 'root',
    #     'password': ''
    # })

    def __attrs_post_init__(self):
        self.database = base_database
        self.database.init(self.database_file)
        self.database.connect()
        self.database.create_tables([Data])
        self.twitter_auth = tweepy.OAuthHandler(
            self.twitter_config['client_key'],
            self.twitter_config['client_secret'],
        )
        self.twitter_auth.set_access_token(
            self.twitter_config['access_token'],
            self.twitter_config['access_token_secret'],
        )
        self.twitter_api = tweepy.API(auth_handler=self.twitter_auth)
        # self.collection = pymongo.MongoClient(**self.mongodb_options)[
        #     os.path.basename(__name__).split('.', 1)[0]
        # ]['items']

    async def send(self):
        while True:
            for item in functools.reduce(lambda a, b: list(a) + list(b), [
                    list(
                        self.twitter_api.list_timeline(
                            user, timeline, count=20))
                    for user, timeline in self.timelines
            ]):
                # if not self.collection.find_one({'id': item._json['id']}):
                #     self.collection.insert_one(dict(item._json, timestamp=datetime.datetime.utcnow()))
                if not Data.select().where(Data.data_id == item._json['id']):
                    Data(
                        data_id=item._json['id'],
                        body=item._json,
                    ).save()
                    for connection in self.connections:
                        await asyncio.wait(
                            [connection.send(self.to_json(item))])
            await asyncio.sleep(20)

    def to_json(self, item):
        return json.dumps({
            'type': 'notification',
            'data': {
                'title': item._json['user']['screen_name'],
                'options': {
                    'body':
                    re.sub(
                        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                        '', item._json['text']),
                    'icon': (jmespath.search(
                        'entities.media[*].media_url_https', item._json)
                             or item._json['user']['profile_image_url']),
                }
            }
        })

    async def echo(self, websocket, path):
        self.connections.add(websocket)
        while True:
            if websocket.state == websockets.protocol.State.OPEN:
                pass
            if websocket.state == websockets.protocol.State.CLOSED:
                break
            await asyncio.sleep(1)
        self.connections.remove(websocket)

    def serve(self):
        return websockets.serve(self.echo, self.host, self.port)


def run(**kwargs):
    notification = UmuusTwitterWebsocketsNotification(**kwargs)
    asyncio.get_event_loop().run_until_complete(
        asyncio.gather(
            notification.send(),
            notification.serve(),
        ))
    asyncio.get_event_loop().run_forever()
    return


def main(argv=None):
    fire.Fire()
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
