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