from pathlib import Path
import json
import requests
import yaml
import socket
from contextlib import contextmanager

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


@contextmanager
def train_notifier(msg=None):
    if msg is not None:
        send_slack("{}の学習を開始します".format(msg), ":robot_face:")
    else:
        send_slack("学習を開始します", ":robot_face:")

    try:
        yield
    except:
        if msg is not None:
            send_slack("{}の学習が失敗しました".format(msg), ":robot_face:")
        else:
            send_slack("学習が失敗しました", ":robot_face:")

    if msg is not None:
        send_slack("{}の学習が完了しました".format(msg), ":robot_face:")
    else:
        send_slack("学習が完了しました", ":robot_face:")


if __name__ == "__main__":
    hostip = get_host_ip()
    send_slack("{}から送信テスト".format(hostip), ":+1:")
