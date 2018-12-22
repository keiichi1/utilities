import schedule
import time
import subprocess
import sys
from utils import slack_notifier

def job():
    #ここにメインの処理を書く
    with slack_notifier("スケジュールジョブ"):
        command = [
                ]
        res = subprocess.run(command, stdout=subprocess.PIPE)
        sys.stdout.buffer.write(res.stdout)


#5秒ごとにjobを実行
# schedule.every(5).minutes.do(job)

# schedule.every(10).minutes.do(job)

#毎時間ごとにjobを実行
# schedule.every().hour.do(job)

#AM10:30にjobを実行
# schedule.every().day.at("10:30").do(job)

#月曜日にjobを実行
schedule.every().monday.do(job)

#水曜日の13:15にjobを実行
# schedule.every().wednesday.at("13:15").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)