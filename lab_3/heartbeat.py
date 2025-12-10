import time
import json
import etcd3 # version 0.12.0
etcd = etcd3.client(host='localhost', port=2379)
HEARTBEAT_KEY = "/monitor/heartbeat/node-1"
LEASE_TTL = 5 # seconds
def send_heartbeat():
    lease = etcd.lease(LEASE_TTL) # create a lease with TTL
    print(f"Lease created with TTL {LEASE_TTL} seconds, ID: {lease.id}")
    try:
        while True:
            data = json.dumps({"status": "alive", "ts": time.time()})
            etcd.put(HEARTBEAT_KEY, data, lease=lease) # put heartbeat key with lease attached
            print("Heartbeat sent")
            lease.refresh() # refresh the lease before it expires to keep key alive
            time.sleep(LEASE_TTL / 2) # sleep less than TTL to ensure refresh before expiry
    except KeyboardInterrupt:
        print("Stopping heartbeat")
        lease.revoke() # optional: revoke lease and delete key immediately
if __name__ == "__main__":
    send_heartbeat()
