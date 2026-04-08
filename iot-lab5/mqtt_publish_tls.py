import paho.mqtt.client as mqtt
import ssl, time, json, os

BROKER = '18.208.138.89'
PORT   = 8883
TOPIC  = 'iot/lab/topic'

CA   = os.path.expanduser('~/mqtt-certs/ca.crt')
CERT = os.path.expanduser('~/mqtt-certs/client.crt')
KEY  = os.path.expanduser('~/mqtt-certs/client.key')

client = mqtt.Client(client_id='rpi-tls-client')

client.tls_set(
    ca_certs=CA,
    certfile=CERT,
    keyfile=KEY,
    tls_version=ssl.PROTOCOL_TLSv1_2
)

client.tls_insecure_set(True)

print('[*] Connecting to broker with TLS...')
client.connect(BROKER, PORT, 60)
print('[*] Connected.')

for i in range(10):
    payload = json.dumps({
        "device": "rpi-tls-client",
        "temp": 20 + i * 0.5,
        "unit": "C"
    })
    client.publish(TOPIC, payload)
    print(f'  Sent: {payload}')
    time.sleep(1)

client.disconnect()
print('[*] Done.')
