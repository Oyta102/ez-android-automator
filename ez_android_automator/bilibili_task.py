"""
@Time: 2024/5/14 19:00
@Auth: coin
@Email: 918731093@qq.com
@File: bilibili_task.py
@IDE: PyCharm
@Motto: one coin
"""
import time
from ez_android_automator.client import Stage, PublishClient, AndroidClient, PublishTask, \
    PhoneLoginTask, WaitCallBackStage, StatisticTask, PullDataTask, TaskAsStage
from ez_android_automator.idm_task import IDMPullTask


class GetAccountStage(Stage):
    def __init__(self, from_path: str, to_path: str, server_to_path: str, serial: int, sh_name: str, tar_name: str):
        super().__init__(serial)
        self.from_path = from_path
        self.to_path = to_path
        self.server_to_path = server_to_path
        self.sh_name = sh_name
        self.tar_name = tar_name

    def run(self, client: AndroidClient):
        client.device.shell('sh ' + self.to_path + '/adbSH/' + self.sh_name)
        # 指定要拉取的文件路径和保存到本地的目录路径
        source_path = self.to_path + '/' + self.tar_name + '.tar.gz'
        destination_path = self.server_to_path
        print(source_path)
        print(destination_path)
        # client.device.pull(source_path,destination_path)
        os.system(f'adb shell {source_path} {destination_path}')
        command = f"adb pull {source_path} {destination_path}"
        subprocess.run(command, shell=True)


class CreateShStage(Stage):
    def __init__(self, from_packagename: str, from_path: str, serial: int, sh_name: str, to_path: str, tar_name: str):
        super().__init__(serial)
        self.sh_name = sh_name
        self.from_packagename = from_packagename
        self.from_path = from_path
        self.to_path = to_path
        self.tar_name = tar_name

    def run(self, client: AndroidClient):
        # 构建命令列表
        commands = [
            f'mkdir -p {self.to_path}/{self.from_path}',
            'su',
            f'cp -r {self.from_packagename}/{self.from_path} {self.to_path}',
            f'chmod 777 -R {self.to_path}/{self.from_path}',
            f'cd {self.to_path}',
            f'tar -zcvf {self.tar_name}.tar.gz {self.from_path}',
            f'chmod 777 -R {self.to_path}/{self.tar_name}.tar.gz',
            f'mkdir -p {self.to_path}/Datas'
        ]

        # 将命令连接为单个字符串，并确保使用 Unix 换行符
        script_content = "#!/bin/bash\n\n" + "\n".join(commands) + "\n"
        # 打开文件并写入命令，明确使用 Unix 换行符
        with open(self.sh_name, "w", newline='\n', encoding='utf-8') as file:
            file.write(script_content)
        # for command in commands:
        #     file.write(command + '\n')
        client.device.push(self.sh_name, self.to_path + "/adbSH/")

class PullDataShStage(Stage):
    def __init__(self, from_packagename: str, from_path: str, serial: int, sh_name: str, to_path: str, tar_name: str, server_to_path: str):
        super().__init__(serial)
        self.sh_name = sh_name
        self.from_packagename = from_packagename
        self.from_path = from_path
        self.to_path = to_path
        self.tar_name = tar_name
        self.server_to_path = server_to_path

    def run(self, client: AndroidClient):

        client.device.push(self.server_to_path+'/'+self.tar_name+'.tar.gz', self.to_path+self.from_path)

        # 构建命令列表
        commands = [
            'su',
            f'cd {self.to_path}/{self.from_path}',
            f'tar -xf {self.to_path}/{self.tar_name}.tar.gz',
            # f'tar -xf {self.from_packagename}/{self.tar_name} {self.from_packagename}',
            f'cp -r {self.to_path}/{self.from_path}/{self.tar_name} {self.from_packagename}',
            f'rm -r {self.to_path}/{self.from_path}/{self.tar_name}',
        ]
        # 将命令连接为单个字符串，并确保使用 Unix 换行符
        script_content = "#!/bin/bash\n\n" + "\n".join(commands) + "\n"
        # 打开文件并写入命令，明确使用 Unix 换行符
        with open(self.sh_name, "w", newline='\n', encoding='utf-8') as file:
            file.write(script_content)
        client.device.push(self.sh_name, self.to_path + "/adbSH/")

        client.device.shell('sh ' + self.to_path + '/adbSH/' + self.sh_name)


class OpenAppStage(Stage):
    def __init__(self, serial, clear_data: bool = False):
        self.clear_data = clear_data
        super().__init__(serial)

    def run(self, client: PublishClient):
        client.restart_app("tv.danmaku.bili", self.clear_data)
        time.sleep(7)
        if self.clear_data:
            client.wait_to_click({'text': '同意并继续'})


class BeforeLoginStage(Stage):
    def __init__(self, serial, phone: str):
        super().__init__(serial)
        self.phone = phone

    def run(self, client: AndroidClient):
        client.wait_to_click({"content-desc": "登录，按钮"})
        client.wait_to_click({"text": "请输入手机号码"})
        client.device.send_keys(self.phone)
        client.wait_to_click({"text": "获取验证码"})


class PhoneAuthCodeStage(Stage):
    def __init__(self, serial):
        super().__init__(serial)
        self.code = None

    def run(self, client: AndroidClient):
        client.device.send_keys(self.code)
        client.wait_to_click({"text": "同意并登录"})

    def code_callback(self, code: str):
        self.code = code


class PressPublishButtonStage(Stage):
    def run(self, client: PublishClient):
        client.wait_to_click({"content-desc": "发布内容,5之3,标签"}, gap=3)


class ChooseFirstVideoStage(Stage):
    def run(self, client: PublishClient):
        client.wait_to_click({'text': '视频'})
        time.sleep(7)
        client.device.click(190, 970)
        client.wait_to_click({'text': '发布'})


class SetVideoOptionsStage(Stage):
    def __init__(self, serial, content: str):
        super().__init__(serial)
        self.content = content

    def run(self, client: PublishClient):
        client.wait_to_click({"text": "合适的标题可以吸引更多人观看～"})
        client.device.send_keys(self.content)
        client.wait_to_click({"text": "发布"})


class StatisticCenterStage(Stage):
    def run(self, client: AndroidClient):
        time.sleep(7)  # wait for ad to be finished
        client.wait_to_click({'text': '我的'})
        client.wait_to_click({'text': '稿件管理'})


class GetStatisticStage(Stage):
    def __init__(self, stage_serial: int, video_title: str, statistic_callback: callable):
        super().__init__(stage_serial)
        self.video_title = video_title
        self.statistic_callback = statistic_callback

    def run(self, client: AndroidClient):
        client.wait_until_found({'text': '数据'})  # wait for list to be loaded
        client.wait_until_found({'text': self.video_title})
        parser = client.find_xml_by_attr({'text': self.video_title})
        parser = parser[0]
        parent = parser.parent.parent.parent
        last = parent.contents[-2]
        statistic_btn = last.find('node', {'text': '数据'})
        client.click_xml_node(statistic_btn)
        client.wait_until_found({'text': '播放量'})
        time.sleep(2)
        client.refresh_xml()

        def get_statistic_by_attr_name(name):
            label_node = client.find_xml_by_attr({'text': name})[0]
            data_node = label_node.next.next
            return int(data_node['text'])

        statistic = {
            'view': get_statistic_by_attr_name('播放量'),
            'like': get_statistic_by_attr_name('点赞'),
            'comment': get_statistic_by_attr_name('评论'),
            'collect': get_statistic_by_attr_name('收藏'),
            'coin': get_statistic_by_attr_name('投币'),
            'share': get_statistic_by_attr_name('分享')
        }
        self.statistic_callback(statistic)
        pass


class BilibiliStatisticTask(StatisticTask):
    def __init__(self, video_title):
        super().__init__()
        self.statistic = None
        # self.append(TaskAsStage(0, ))
        self.append(OpenAppStage(1))
        self.append(StatisticCenterStage(2))
        self.append(GetStatisticStage(3, video_title, self.statistic_callback))

    def statistic_callback(self, statistic: dict):
        self.statistic = statistic


class BilibiliPublishVideoTask(PublishTask):
    """
    Publish a video on Bilibili.
    """

    def __init__(self, priority: int, title: str, content: str, video: str):
        super().__init__(priority, title, content, video, '')
        task = IDMPullTask(video)
        self.stages.append(TaskAsStage(0, task))
        self.stages.append(OpenAppStage(1))
        self.stages.append(PressPublishButtonStage(2))
        self.stages.append(ChooseFirstVideoStage(3))
        self.stages.append(SetVideoOptionsStage(4, self.content))


class BilibiliPhoneLoginTask(PhoneLoginTask):
    def __init__(self, phone: str):
        super().__init__(phone)
        self.stages.append(OpenAppStage(0, True))
        self.stages.append(BeforeLoginStage(1, phone))
        auth_stage = PhoneAuthCodeStage(3)
        self.stages.append(WaitCallBackStage(2, 60, self.get_code, auth_stage.code_callback))
        self.stages.append(auth_stage)


class BilibiliGetAccountTask(PullDataTask):
    def __init__(self, from_package_name: str, from_path: str, sh_name: str, to_path: str, server_to_path: str,
                 tar_name: str):
        super().__init__(from_package_name, from_path, sh_name, to_path, server_to_path, tar_name)
        self.stages.append(
            CreateShStage(from_package_name, from_path, 0, sh_name, to_path, tar_name))
        # self.stages.append(GetAccountStage(to_path + from_path, server_to_path, 1, sh_name))
        self.stages.append(GetAccountStage(from_path, to_path, server_to_path, 1, sh_name, tar_name))

