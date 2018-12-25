from pathlib import Path
import json
import requests
import yaml
import socket
from contextlib import contextmanager


def send_slack(content, emoji=":robot_face:", image=None):
    SLACK_CONFIG = Path(__file__).resolve().parents[1]/'config/slack_conf.yaml'
    with open(str(SLACK_CONFIG)) as f:
        config = yaml.safe_load(f)

    url = config["url"]
    if image is not None:
        param = dict(token=config["token"], channels=config["channel"])
        files = dict(file=open(image, 'rb'))
        requests.post(url="https://slack.com/api/files.upload",params=param, files=files)
    else:
        payload = dict(text=content, icon_emoji=emoji)
        data = json.dumps(payload)
        requests.post(url, data)



def get_host_ip():
    return socket.gethostbyname(socket.gethostname())


@contextmanager
def train_notifier(msg=None):
    if msg is not None:
        send_slack("{}の学習を開始します".format(msg))
    else:
        send_slack("学習を開始します")

    try:
        yield
    finally:
        if msg is not None:
            send_slack("{}の学習が失敗しました".format(msg))
        else:
            send_slack("学習が失敗しました")

    if msg is not None:
        send_slack("{}の学習が完了しました".format(msg))
    else:
        send_slack("学習が完了しました")


if __name__ == "__main__":
    hostip = get_host_ip()
    send_slack("{}から送信テスト".format(hostip), ":+1:")

