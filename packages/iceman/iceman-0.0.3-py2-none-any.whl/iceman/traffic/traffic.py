# -*- coding: utf-8 -*-
"""iceman/traffic/traffic.py
"""

import nfqueue
from scapy.layers.inet import IP, TCP

class Traffic(object):
    """Abstracted Egress/Ingress class
    :param callback: inherited function callback
    :type callback: instancemethod

    :param queue: nfqueue number
    :type queue: int

    :param cipher_suite: crypto wrapper cipher strategy
    :type cipher_suite: instance

    :param encryption_enabled: encryption flag
    :type encryption_enabled: bool
    """

    def __init__(self, queue, cipher_suite, encryption_enabled):
        self.queue = queue
        self.cipher_suite = cipher_suite
        self.encryption_enabled = encryption_enabled

    def transform(self, method, payload):
        """Abstracted transformation scapy callback.  This method
        handles packets sent to a given queue defined in iptables.
        This will ignore any packet whose payload is empty and will
        encrypt/decrypt packet payload otherwise.

        :param method: encrypt or decrypt directive
        :type method: str

        :param payload:
        :type payload: <class 'nfqueue.payload'>
        """
        pkt = IP(payload.get_data())
        text = str(pkt[TCP].payload)

        len_before = len(text)
        if len_before > 0:
            if self.encryption_enabled:
                pkt[TCP].payload = getattr(self.cipher_suite, method)(text)
            len_after = len(pkt[TCP].payload)

            diff = len_after - len_before
            pkt[IP].len = pkt[IP].len + diff

            del pkt[TCP].chksum
            del pkt[IP].chksum

        payload.set_verdict_modified(nfqueue.NF_ACCEPT, str(pkt), len(pkt))
