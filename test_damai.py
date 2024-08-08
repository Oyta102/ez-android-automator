"""
@Time: 2024/7/27 7:19
@Auth: EnderTheCoder
@Email: ggameinvader@gmail.com
@File: test_damai.py
@IDE: PyCharm
@Motto：The only one true Legendary Grandmaster.
"""
import os

from ez_android_automator.client import create_usb_client
from ez_android_automator.damai_task import DaMaiBuyTask

task = DaMaiBuyTask(
    [('祁佩璇', '152701199203060928')],
    "厦门林俊杰",
    None,
    [0],
    [0],
    os.environ.get("YM_TOKEN")
)

client = create_usb_client()
client.set_task(
    task
)

client.run_current_task()