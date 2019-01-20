from pathlib import Path
import json
import requests
import yaml
import socket
import time
import shutil
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
def train_notifier(title=None):
    if title is not None:
        send_slack("{}の学習を開始します".format(title))
    else:
        send_slack("学習を開始します")

    try:
        yield
        if title is not None:
            send_slack("{}の学習が完了しました".format(title))
        else:
            send_slack("学習が完了しました")

    except:
        import traceback
        traceback.print_exc()
        if title is not None:
            send_slack("{}の学習が失敗しました".format(title))
        else:
            send_slack("学習が失敗しました")


@contextmanager
def lap_timer():
    start = time.time()

    yield

    laptime = time.time() - start
    print("Lap Time: {}".format(laptime))


def make_directory(directory_path):
    directory_path = Path(directory_path)

    if not directory_path.exists():
        directory_path.mkdir(parents=True, exist_ok=True)
    else:
        print("既にディレクトリが存在します")

def get_path_list(directory_path):
    ROOT_PATH = Path(directory_path)
    file_list = ROOT_PATH.glob("*")
    return file_list



if __name__ == "__main__":
    hostip = get_host_ip()
    send_slack("{}から送信テスト".format(hostip), ":+1:")

