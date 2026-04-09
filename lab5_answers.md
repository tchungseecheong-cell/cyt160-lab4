Q1: Open both pcaps with tcpdump -r <file> -nn -A and compare the output. List three specific 
things that are visible in the plaintext capture but hidden in the TLS capture. What does this 
mean for an attacker who can intercept network traffic between the Pi and the broker? 

In the plaintext capture (mqtt_plaintext.pcap), several pieces of sensitive information are clearly visible that are completely hidden in the TLS capture (mqtt_tls.pcap). First, the actual MQTT message content (e.g., sensor.datatemp:21C, 22C, etc.) can be read directly in plaintext. Second, topic names such as sensor/data are visible, revealing the structure and purpose of the communication. Third, the payload values (temperature readings) and application-level data are fully exposed and human-readable.
On the otherhand, the TLS capture only shows encrypted binary data, making the payload, topics, and message contents unreadable. For an attacker intercepting traffic, this means that without TLS they can easily read and potentially manipulate sensitive IoT data, while with TLS they can only see metadata (like IPs and ports) but cannot understand or alter the actual communication. This significantly reduces the risk of data leakage and tampering.



Q2: Your mosquitto.conf sets require_certificate true. What does this mean for a client that tries 
to connect without a certificate? Test it: run mosquitto_sub -h <VM_IP> -p 8883 -t '#' from a 
terminal that does NOT provide --cafile, --cert, and --key flags. What error message do you get? 
Why is this a security improvement over allow_anonymous true? 

By setting require_certificate true in the Mosquitto configuration enforces mutual TLS (mTLS), meaning that clients must present a valid certificate to authenticate themselves to the broker. When attempting to connect without providing --cafile, --cert, and --key, the connection fails. The typical error message is something like: “Connection error: Protocol error” or “TLS error: certificate required”, depending on the client output.

This is a major security improvement over allow_anonymous true because it prevents unauthorized clients from connecting to the broker. With anonymous access enabled, anyone who can reach the broker could subscribe or publish to topics, potentially injecting malicious data or eavesdropping. Requiring certificates ensures that only trusted, verified clients can connect, enforcing strong authentication and reducing the attack surface.


Q3: Suricata is monitoring port 1883 (plaintext). It cannot read the encrypted payload on port 
8883 without the TLS session keys. Given this limitation, what can Suricata still usefully observe 
about TLS traffic — and how would you use that to detect a threat on port 8883? This is relevant 
to the rules you will write in Project 2.

Even though Suricata cannot decrypt TLS traffic on port 8883 without session keys, it can still observe important metadata about the encrypted communication. This includes source and destination IP addresses, ports, packet sizes, timing patterns, TLS handshake details (such as certificate information), and connection frequency. Suricata can also detect anomalies like unusual traffic spikes, repeated failed connection attempts, or connections to suspicious or unknown endpoints.
