
from Adafruit_IO import MQTTClient
import sys

class mqtt_client:
  AIO_FEED_IDs = []
  AIO_USERNAME = 'nguyentruongthan'
  AIO_KEY = 'aio_msFs10ZtvnluSAJeoogfJl1ubh0T'

  def __init__(self):
    self.client = MQTTClient(self.AIO_USERNAME, self.AIO_KEY)
    self.client.on_connect = self.connected
    self.client.on_disconnect = self.disconnected
    self.client.on_message = self.message
    self.client.on_subscribe = self.subscribe

    self.client.connect()
    self.client.loop_background()

  
  def connected(self, client, ):
    print('Connected successful ...')
    for topic in self.AIO_FEED_IDs:
      client.subscribe(topic)

  def subscribe(self, client, userdata, mid, granted_qos):
    print('Subscribe successful ...')

  def disconnected(self, client):
    print('Disconnect ...')
    sys.exit(1)

  def message(self, client, feed_id, payload):
    print(f'Receive data: {payload}, feed id: {feed_id}')

  def publish(self, feed_id, message):
    self.client.publish(feed_id, message)
