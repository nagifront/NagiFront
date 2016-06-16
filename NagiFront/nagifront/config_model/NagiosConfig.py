'''
  나기오스 설정 파일 읽기 변경 쓰기 모듈입니다
'''

import re
import os

from django.conf import settings

from nagifront.config_model.Password import password

'''
  Nagios Overall Configuration Module
'''
class NagiosConfig:
    def restart(self):
        command = 'echo %s | sudo -S service nagios3 restart' % password
        ret = os.system(command)
        return ret == 0
        
    def valid(self):
        command = 'echo %s | sudo -S nagios3 -v %s' % (password, os.path.join(settings.NAGIOS_ROOT, 'nagios.cfg'))
        ret = os.system(command)
        return ret == 0

    def move(self, temp, real):
        command = 'echo %s | sudo -S mv %s %s' % (password, temp, real)
        ret = os.system(command)
        return ret == 0

    def erase(self, filename):
        command = 'echo %s | sudo -S rm %s' % (password, filename)
        ret = os.system(command)
        return ret == 0

'''
  Nagios Host Configuration Module
'''
class NagiosHostConfig(NagiosConfig):
    # [{ name: , description: , default: , is_necessary: , is_advanced: }]
    directives_list = [
        { 'name': 'host_name', 'description': '호스트 이름 (필수)', 'default': None, 'is_necessary': True, 'is_advanced': False, 'option_kind': 0 },
        { 'name': 'address', 'description': '주소 (필수)', 'default': None, 'is_necessary': True, 'is_advanced': False, 'option_kind': 0 },
        { 'name': 'max_check_attempts', 'description': '체크를 몇 번이나 시도할 지 (필수)', 'default': '10', 'is_necessary': True, 'is_advanced': False, 'option_kind': 0 },
        { 'name': 'contacts', 'description': '알림을 받을 사람 (필수)', 'default': None, 'is_necessary': True, 'is_advanced': False, 'option_kind': 11 },
        { 'name': 'contact_groups', 'description': '알림을 받을 그룹 (필수)', 'default': None, 'is_necessary': True, 'is_advanced': False, 'option_kind': 10 },
        { 'name': 'notification_interval', 'description': '재알림 간격 (분, 0이면 다시 안 알려줌) (필수)', 'default': '60', 'is_necessary': True, 'is_advanced': False, 'option_kind': 0 },
        { 'name': 'notification_period', 'description': '알림을 받는 시간대 (필수)', 'default': None, 'is_necessary': True, 'is_advanced': False, 'option_kind': 9 },
        { 'name': 'check_period', 'description': '어떤 시간대에 체크할 지 (필수)', 'default': None, 'is_necessary': True, 'is_advanced': False, 'option_kind': 9 },
        { 'name': 'alias', 'description': '호스트 별명 (필수)', 'default': None, 'is_necessary': True, 'is_advanced': False, 'option_kind': 0 },
        { 'name': 'check_command', 'description': '어떤 커맨드로 Host를 체크할 지 (필수)', 'default': 'check-host-alive', 'is_necessary': True, 'is_advanced': False, 'option_kind': 0 },
        # Necessary
        { 'name': 'display_name', 'description': '', 'default': None, 'is_necessary': False, 'is_advanced': False, 'option_kind': 0 },
        { 'name': 'parents', 'description': '부모 호스트의 이름', 'default': None, 'is_necessary': False, 'is_advanced': False, 'option_kind':1 },
        { 'name': 'hostgroups', 'description': '속해 있는 호스트 그룹들', 'default': None, 'is_necessary': False, 'is_advanced': False, 'option_kind': 2 },
        { 'name': 'initial_state', 'description': '초기 상태', 'default': None, 'is_necessary': False, 'is_advanced': False, 'option_kind': 0 },
        { 'name': 'check_interval', 'description': '체크 간격 (분), 0이면 ', 'default': None, 'is_necessary': False, 'is_advanced': False, 'option_kind': 0 },
        { 'name': 'retry_interval', 'description': '재시도 간격', 'default': None, 'is_necessary': False, 'is_advanced': False, 'option_kind': 0 },
        { 'name': 'active_checks_enabled', 'description': '나기오스의 액티브 체크 활성화', 'default': None, 'is_necessary': False, 'is_advanced': False, 'option_kind': 0 },
        { 'name': 'first_notification_delay', 'description': '문제 발생 시 복구까지 알림 대기', 'default': None, 'is_necessary': False, 'is_advanced': False, 'option_kind': 0 },
        { 'name': 'notification_options', 'description': '알림 옵션', 'default': 'd,r', 'is_necessary': False, 'is_advanced': False, 'option_kind': 0 },
        { 'name': 'notifications_enabled', 'description': '알림 끄고 켜기', 'default': '1', 'is_necessary': False, 'is_advanced': False, 'option_kind': 0 },
        { 'name': 'notes', 'description': '', 'default': None, 'is_necessary': False, 'is_advanced': False, 'option_kind': 0 },
        # Intermediate
        { 'name': 'notes_url', 'description': '', 'default': None, 'is_necessary': False, 'is_advanced': True, 'option_kind': 0 },
        { 'name': 'action_url', 'description': '', 'default': None, 'is_necessary': False, 'is_advanced': True, 'option_kind': 0 },
        { 'name': 'icon_image', 'description': '', 'default': None, 'is_necessary': False, 'is_advanced': True, 'option_kind': 0 },
        { 'name': 'icon_image_alt', 'description': '', 'default': None, 'is_necessary': False, 'is_advanced': True, 'option_kind': 0 },
        { 'name': 'vrml_image', 'description': '', 'default': None, 'is_necessary': False, 'is_advanced': True, 'option_kind': 0 },
        { 'name': 'statusmap_image', 'description': '', 'default': None, 'is_necessary': False, 'is_advanced': True, 'option_kind': 0 },
        { 'name': 'passive_checks_enabled', 'description': '', 'default': None, 'is_necessary': False, 'is_advanced': True, 'option_kind': 0 },
        { 'name': 'obsess_over_host', 'description': '', 'default': None, 'is_necessary': False, 'is_advanced': True, 'option_kind': 0 },
        { 'name': 'check_freshness', 'description': '', 'default': None, 'is_necessary': False, 'is_advanced': True, 'option_kind': 0 },
        { 'name': 'freshness_threshold', 'description': '', 'default': None, 'is_necessary': False, 'is_advanced': True, 'option_kind': 0 },
        { 'name': 'event_handler', 'description': '', 'default': None, 'is_necessary': False, 'is_advanced': True, 'option_kind': 0 },
        { 'name': 'event_handler_enabled', 'description': '', 'default': None, 'is_necessary': False, 'is_advanced': True, 'option_kind': 0 },
        { 'name': 'low_flap_threshold', 'description': '', 'default': None, 'is_necessary': False, 'is_advanced': True, 'option_kind': 0 },
        { 'name': 'high_flap_threshold', 'description': '', 'default': None, 'is_necessary': False, 'is_advanced': True, 'option_kind': 0 },
        { 'name': 'flap_detection_enabled', 'description': '', 'default': None, 'is_necessary': False, 'is_advanced': True, 'option_kind': 0 },
        { 'name': 'flap_detection_options', 'description': '', 'default': None, 'is_necessary': False, 'is_advanced': True, 'option_kind': 0 },
        { 'name': 'process_perf_data', 'description': '', 'default': None, 'is_necessary': False, 'is_advanced': True, 'option_kind': 0 },
        { 'name': 'retain_status_information', 'description': '', 'default': None, 'is_necessary': False, 'is_advanced': True, 'option_kind': 0 },
        { 'name': 'retain_nonstatus_information', 'description': '', 'default': None, 'is_necessary': False, 'is_advanced': True, 'option_kind': 0 },
        { 'name': 'stalking_options', 'description': '', 'default': None, 'is_necessary': False, 'is_advanced': True, 'option_kind': 0 },
        { 'name': '2d_coords', 'description': '', 'default': None, 'is_necessary': False, 'is_advanced': True, 'option_kind': 0 },
        { 'name': '3d_coords', 'description': '', 'default': None, 'is_necessary': False, 'is_advanced': True, 'option_kind': 0 },
        # Advanced
    ]
    # Necessary Directive List
    # 
    necessary_directives_list = [
        'host_name',
        'address',
        'max_check_attempts',
        'contacts',
        'contact_groups',
        'notification_interval',
        'notification_period',
        'check_period',
    ]
    def __init__(self):
        self.config = {}
        self.backup = ''

    def __str__(self):
        print('define host {')
        for k, v in self.config.items():
            if v is not None:
        # 근데 None 이면 안 됨
                print('    ' + k + ' ' + v)
            else:
                print('    ' + '# ' + k)
        print('}')

    def read(self, filename):
        read_config = dict()
        try:
            f = open(filename, 'r')
            while True:
                line = f.readline()
                if not line: break
                if re.match('\s*#.*', line) is not None: continue # comment
                r = re.match('\s*([a-zA-Z_]*)\s+(.*)', line)
                if r is None: continue
                key = r.group(1)
                value = r.group(2)
                read_config[key] = value
            f.close()
        except FileNotFoundError:
            pass
        # 읽어온다
        for directive in NagiosHostConfig.directives_list:
            key = directive['name']
            if key in read_config.keys():
                self.config[key] = read_config[key]
            else:
                self.config[key] = directive['default']
        # 키 리스트를 돌면서 넣는데
        # 그 키가 읽어온 거에 있으면
          # 그걸 넣고
        # 아니면
          # 디폴트를 넣는다
        self.backup = (
'''
# 이 설정 파일은 Nagifront로부터 생성된 설정 파일입니다
# 수정하지 마세요

'''
        )
        self.backup += ('define host {\n')
        for k, v in self.config.items():
            if v is not None:
                self.backup += ('    ' + k + ' ' + v + '\n')
            else:
                self.backup += ('    ' + '# ' + k + '\n')
        self.backup += ('}')

    def write(self, filename):
        f = open(filename, 'w')
        # 주어진 포맷에 맞게 저장
        f.write(
'''
# 이 설정 파일은 Nagifront로부터 생성된 설정 파일입니다
# 수정하지 마세요

'''
        )
        f.write('define host {\n')
        for k, v in self.config.items():
            if v is not None:
        # 근데 None 이면 안 됨
                f.write('    ' + k + ' ' + v + '\n')
            else:
                f.write('    ' + '# ' + k + '\n')
        f.write('}')
        f.close()

    def edit(self, key, value):
        # 해당 키에서 value를 고친다
        if value == '':
            value = None
        self.config[key] = value

    def valid(self):
        # 필수가 있는지 확인
        return super().valid()

    def gen_filename(self):
        return self.config['host_name'] + '.cfg'


