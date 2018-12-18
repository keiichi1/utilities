from pathlib import Path
import json
import requests
import yaml
import socket


def send_slack(content, emoji, image=False):
    SLACK_CONFIG = Path(__file__).resolve().parents[0]/'slack_conf.yaml'
    with open(str(SLACK_CONFIG)) as f:
        config = yaml.safe_load(f)

    url = config["url"]
    if image:
        payload = dict(text=content, icon_emoji=emoji, files=image)
    else:
        payload = dict(text=content, icon_emoji=emoji)

    data = json.dumps(payload)
    requests.post(url, data)


def get_host_ip():
    return socket.gethostbyname(socket.gethostname())


if __name__ == "__main__":
    hostip = get_host_ip()
    send_slack("{}から送信テスト".format(hostip), ":+1:")
