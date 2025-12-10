import time
import json
import etcd3 # version 0.12.0
etcd = etcd3.client(host='localhost', port=2379)
CONFIG_KEY = "/config/monitor"
value, _ = etcd.get(CONFIG_KEY)
config_value = json.loads(value) if value else {}

def watch_config_key(watch_response):
    global config_value
    for event in watch_response.events:
        if isinstance(event, etcd3.events.PutEvent):
            config_value = json.loads(event.value.decode('utf-8'))

def main():
    watch_id = etcd.add_watch_callback(CONFIG_KEY, watch_config_key)
    try:
        while True:
            print(f"Using config: {config_value} to do something...")
            time.sleep(5)
    except KeyboardInterrupt:
        print("Stopping watcher...")
        etcd.cancel_watch(watch_id)
if __name__ == "__main__":
    main()