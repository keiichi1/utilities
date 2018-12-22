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
        payload = dict(text=content, icon_emoji=emoji, files=image)
    else:
        payload = dict(text=content, icon_emoji=emoji)

    data = json.dumps(payload)
    requests.post(url, data)


def get_host_ip():
    return socket.gethostbyname(socket.gethostname())


@contextmanager
def slack_notifier(msg=None):
    if msg is not None:
        send_slack("{}を開始します".format(msg))
    else:
        send_slack("開始します")

    try:
        yield
    except:
        if msg is not None:
            send_slack("{}が失敗しました".format(msg))
        else:
            send_slack("失敗しました")

    if msg is not None:
        send_slack("{}が完了しました".format(msg))
    else:
        send_slack("完了しました")


if __name__ == "__main__":
    hostip = get_host_ip()
    send_slack("{}から送信テスト".format(hostip), ":+1:")