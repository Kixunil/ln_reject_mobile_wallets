from rules import is_channel_allowed
import donate
import rpc_pb2 as lnd
import rpc_pb2_grpc as lndrpc
import grpc
import os
import sys
import queue
import codecs

class LNNode:
    def __init__(self, node_id, client):
        self._node_id = node_id
        self._client = client

    def public_channel_count(self):
        try:
            pub_key = codecs.encode(self._node_id, "hex")
            request = lnd.NodeInfoRequest(pub_key = pub_key, include_channels = True)

            return self._client.GetNodeInfo(request).num_channels
        except:
            return 0

class ChannelRequest:
    def __init__(self, request, client):
        self._request = request
        self._client = client

    def capacity_sats(self):
        return self._request.funding_amt

    def is_public_channel(self):
        return self._request.channel_flags & 1 == 1

    def node(self):
        return LNNode(self._request.node_pubkey, self._client)

def handle_donation(client):
    donation_invoice = donate.check_donate()
    if donation_invoice is not None:
        client.SendPaymentSync(lnd.SendRequest(payment_request=donation_invoice))
        print("Thank you for your support!")


def handle_channel_open_requests():
    os.environ["GRPC_SSL_CIPHER_SUITES"] = "HIGH+ECDSA"

    with open(os.path.expanduser("~/.lnd/data/chain/bitcoin/mainnet/admin.macaroon"), "rb") as macaroon_file:
        macaroon = macaroon_file.read()
        macaroon = codecs.encode(macaroon, "hex")

    with open(os.path.expanduser("~/.lnd/tls.cert"), "rb") as cert_file:
        cert = cert_file.read()

    def metadata_callback(context, callback):
        callback([("macaroon", macaroon)], None)

    cert_creds = grpc.ssl_channel_credentials(cert)
    auth_creds = grpc.metadata_call_credentials(metadata_callback)
    creds = grpc.composite_channel_credentials(cert_creds, auth_creds)

    connection = grpc.secure_channel("localhost:10009", creds)
    client = lndrpc.LightningStub(connection)

    handle_donation(client)

    response_queue = queue.Queue()

    def responses(queue):
        while True:
            yield queue.get()

    for request in client.ChannelAcceptor(responses(response_queue)): 
        req = ChannelRequest(request, client)
        accept = is_channel_allowed(req)
        resp = lnd.ChannelAcceptResponse(accept = accept, pending_chan_id = request.pending_chan_id)
        response_queue.put(resp)

if __name__ == "__main__":
    print("Running LND forwarding node acceptor.")
    print("If you find the project useful, you can donate to the author by running:")
    print("%s --donate [AMOUNT [MEMO]]" % sys.argv[0])
    print("The AMOUNT defaults to 50k sats, memo to empty")

    handle_channel_open_requests()
