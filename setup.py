
from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    def run_tests(self):
        import sys
        import shlex
        import pytest
        errno = pytest.main(['--doctest-modules'])
        if errno != 0:
            raise Exception('An error occured during installution.')
        install.run(self)


setup(
    packages=setuptools.find_packages('.'),
    version='0.1',
    url='https://github.com/junmakii/umuus-twitter-websockets-notification',
    author='Jun Makii',
    author_email='junmakii@gmail.com',
    keywords=[],
    license='GPLv3',
    scripts=[],
    install_requires=['fire',
 'attrs',
 'addict',
 'requests',
 'jmespath',
 'tweepy==3.7.0',
 'peewee',
 'websockets'],
    dependency_links=[],
    classifiers=['Development Status :: 3 - Alpha',
 'Intended Audience :: Developers',
 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
 'Natural Language :: English',
 'Programming Language :: Python',
 'Programming Language :: Python :: 3'],
    entry_points={'console_scripts': ['umuus_twitter_websockets_notification = '
                     'umuus_twitter_websockets_notification:main'],
 'gui_scripts': []},
    project_urls={'Bug Tracker': 'https://github.com/junmakii/umuus-twitter-websockets-notification/issues',
 'Documentation': 'https://github.com/junmakii/umuus-twitter-websockets-notification/',
 'Source Code': 'https://github.com/junmakii/umuus-twitter-websockets-notification/'},
    setup_requires=['pytest-runner'],
    test_suite='umuus_twitter_websockets_notification',
    tests_require=['pytest'],
    extras_require={},
    package_data={'': []},
    python_requires='>=3.0.0',
    include_package_data=True,
    zip_safe=True,
    name='umuus-twitter-websockets-notification',
    description='umuus-websockets-notification',
    long_description=('umuus-websockets-notification\n'
 '=============================\n'
 '\n'
 'Installation\n'
 '------------\n'
 '\n'
 '    $ pip install '
 'git+https://github.com/junmakii/umuus-websockets-notification.git\n'
 '\n'
 'Example\n'
 '-------\n'
 '\n'
 '    $ umuus_websockets_notification\n'
 '\n'
 '    >>> import umuus_websockets_notification\n'
 '\n'
 'Usage\n'
 '-----\n'
 '\n'
 'twitter-oauth.json::\n'
 '\n'
 '    {\n'
 '        "client_key": "XXXXXXXXXXXXXXXXXXXXXXXXX",\n'
 '        "client_secret": '
 '"XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",\n'
 '        "access_token": '
 '"XXXXXXXXXX-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",\n'
 '        "access_token_secret": '
 '"XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"\n'
 '    }\n'
 '\n'
 'docker-compose.yml::\n'
 '\n'
 '    services:\n'
 '      umuus_twitter_websockets_notification:\n'
 '        image: "umuus-twitter-websockets-notification:0.1"\n'
 '        command: ["run", "--host", \'"0.0.0.0"\', "--port", "8888", '
 '"--twitter_config", "/app/config/twitter-oauth.json"]\n'
 '        volumes:\n'
 '          - "twitter-oauth.json:/app/config/twitter-oauth.json"\n'
 '        ports:\n'
 '          - "8888:8888"\n'
 '\n'
 'Client\n'
 '------\n'
 '\n'
 '    <script>\n'
 '      function UmuusWebsocketsNotification() {\n'
 "          this.address = 'ws://' + 'localhost' + ':' + '8888';\n"
 "          console.log('UmuusWebsocketsNotification is called: ' + "
 'this.address);\n'
 '          this.socket = new ReconnectingWebSocket(this.address, '
 "['protocol1', 'protocol2'], {debug: true, reconnectInterval: 1000});\n"
 '\n'
 '          this.socket.addEventListener(\n'
 "              'message', \n"
 '              function(event){\n'
 '                  const data = JSON.parse(event.data).data;\n'
 '                  new Notification(data.title, data.options);\n'
 '              });\n'
 '          \n'
 '          this.socket.addEventListener(\n'
 "              'close',\n"
 '              function(event){\n'
 "                  console.log('Connection has closed.');\n"
 '              });\n'
 '      }\n'
 '      \n'
 "      window.addEventListener('load', function() { new "
 'UmuusWebsocketsNotification(); });\n'
 '    </script>\n'
 '\n'
 'Authors\n'
 '-------\n'
 '\n'
 '- Jun Makii <junmakii@gmail.com>\n'
 '\n'
 'License\n'
 '-------\n'
 '\n'
 'GPLv3 <https://www.gnu.org/licenses/>'),
    cmdclass={"pytest": PyTest},
)
