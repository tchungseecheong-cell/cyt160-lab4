
Q1: SID 2000001 uses threshold: type threshold, track by_src, count 100, seconds 60. The flood 
script sends 150 messages at 0.35-second intervals. How many alert events for SID 2000001 did 
you see in eve.json? Explain why the threshold keyword controls how many alerts fire, not just 
whether one fires at all. 

<<<<<<< HEAD

When reviewing my eve.json, I noticed only one or two alerts for SID 2000001 instead of the expected 150. This is because the Suricata rule uses a threshold setting. The rule tracks traffic by source IP and counts matching events over a 60‑second window. An alert is generated only after the count exceeds 100, and once that alert fires, additional alerts are suppressed until the threshold resets. As a result, even though 150 packets matched the rule, Suricata consolidated them into a small number of alerts. 


=======
When reviewing my eve.json, I noticed only one or two alerts for SID 2000001 instead of the expected 150. This is because the Suricata rule uses a threshold setting. The rule tracks traffic by source IP and counts matching events over a 60‑second window. An alert is generated only after the count exceeds 100, and once that alert fires, additional alerts are suppressed until the threshold resets. As a result, even though 150 packets matched the rule, Suricata consolidated them into a small number of alerts. 

>>>>>>> 6d70393 (Project 2 Answers)
Q2: The flood simulation uses paho-mqtt on port 1883 (plaintext) rather than port 8883 (TLS). 
Looking at your Lab 5 analysis Q3 answer, explain why Suricata can inspect the payload on port 
1883 but not on port 8883. What are the trade-offs between running attacks on the plaintext 
versus TLS port for testing purposes? 

Suricata is able to inspect traffic on port 1883 because MQTT on this port is sent in plaintext. This allows Suricata to view packet contents such as message payloads and topics, and to apply rules that match specific strings or patterns in the data. However, on port 8883 the MQTT traffic is encrypted using TLS. Because of this encryption, the payload is no longer readable, so Suricata cannot inspect or match application-layer content. In that case, it can only see basic metadata like IP addresses, port numbers, and limited TLS handshake information.


<<<<<<< HEAD

=======
>>>>>>> 6d70393 (Project 2 Answers)
Q3: SID 2000003 uses depth:100. The malformed script sends 'A'*400. Would the rule still fire if 
the repeated pattern started at byte 200 of the payload? Explain what depth: means and how 
you would change the rule to detect a late-starting pattern. 

The rule for SID 2000003 uses depth:100, which means Suricata only checks the first 100 bytes of the payload for the pattern of repeated “A” characters.

In this project, the script sends 400 “A” characters starting right at the beginning of the payload, so the rule is triggered successfully. However, if the repeated pattern started later, like at byte 200, the rule would not detect it because that is beyond the first 100 bytes being inspected.

The depth option basically limits how far into the payload Suricata looks. This helps improve performance because it doesn’t need to scan the entire packet.

To detect patterns that appear later in the payload, the rule can be adjusted by removing the depth limit, increasing the depth value (for example to 400), or using an offset to tell Suricata to start checking further into the payload.


<<<<<<< HEAD




=======
>>>>>>> 6d70393 (Project 2 Answers)
Q4: Your rules use the alert action (IDS mode — log only). Name two specific changes you would 
make — one in the rule file and one in the Suricata/Docker configuration — to switch to IPS 
mode and actively drop matching packets instead of just alerting.

 Suricata is running in IDS mode because the rules use the alert action, which only detects and logs suspicious traffic. To switch Suricata into IPS mode so it can actively block traffic, two changes are required. First, the rule action must be changed from alert to drop, which tells Suricata to stop packets that match the rule instead of just recording them. Second, Suricata must be run in inline mode so it sits directly in the traffic path. This involves updating the Docker configuration (such as using host networking and adding NET_ADMIN and NET_RAW capabilities) and enabling an inline mode like AF_PACKET or NFQUEUE in Suricata’s configuration. With these changes, Suricata can actively block malicious traffic rather than only monitoring it.
