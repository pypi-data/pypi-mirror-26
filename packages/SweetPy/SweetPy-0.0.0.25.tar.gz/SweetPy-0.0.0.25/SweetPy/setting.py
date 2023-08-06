from django.conf import settings
import requests
import json
from SweetPy.zookeeper_plus import ZookeeperPlus
import platform
import os

# 设置项
# SWEETPY_IS_CONNECTED_EVUN_CLOUD = True
# SWEETPY_EVUN_CLOUD_REGISTER_URL = 'http://10.86.87.180:19999/'
# SWEETPY_EVUN_CLOUD_REGISTER_APPNAME = 'python-sweet'
# SWEETPY_EVUN_CLOUD_REGISTER_APP_VERSION = '1.0'
# SWEETPY_EVUN_CLOUD_REGISTER_APP_TICKET = 'c0882ecd-5c6f-4a03-b8e9-c45b556e14dc'
# SWEETPY_EVUN_CLOUD_REGISTER_APP_HOST = '10.200.144.127'
# SWEETPY_EVUN_CLOUD_REGISTER_APP_PORT = '8000'

sweet_settings = None

def get_local_ip():
    import socket
    localIP = socket.gethostbyname(socket.gethostname())
    # localIP = socket.gethostname()
    return localIP

def get_http_port():
    result = 80
    global sweet_settings
    if not sweet_settings:
        return result
    if not sweet_settings.get('applicationInstanceConfigurations',None):
        return result
    else:
        return sweet_settings['applicationInstanceConfigurations'].get('sweet.framework.socket.server.tcp.port',result)

def get_sweet_settings_local_filename():
    app_name = settings.SWEETPY_EVUN_CLOUD_REGISTER_APPNAME
    app_port = settings.SWEETPY_EVUN_CLOUD_REGISTER_APP_PORT
    app_host = get_local_ip()#settings.SWEETPY_EVUN_CLOUD_REGISTER_APP_HOST
    sysstr = platform.system()
    if sysstr.lower() == 'windows':
        filename = os.environ["TMP"] + '\\' + app_name + app_host + str(app_port) + '.json'
    else:
        filename = '/tmp/' + app_name + app_host + str(app_port) + '.json'
    return filename

def get_sweet_settings():
    global sweet_settings
    if sweet_settings:
        return sweet_settings
    filename = get_sweet_settings_local_filename()
    if not os.path.exists(filename):
        return {}
    with open(filename,'r') as f:
        sweet_settings = json.loads(f.read())
        return sweet_settings

def write_sweet_settings(setting):
    filename = get_sweet_settings_local_filename()
    with open(filename, 'w') as f:
        f.write(json.dumps(setting,ensure_ascii=False))

def get_sweet_params_from_evun_colud():
    global sweet_settings
    if sweet_settings:
        return
    if (hasattr(settings,'SWEETPY_IS_CONNECTED_EVUN_CLOUD')) and settings.SWEETPY_IS_CONNECTED_EVUN_CLOUD:
        url = settings.SWEETPY_EVUN_CLOUD_REGISTER_URL + '?' + \
              'application=' + settings.SWEETPY_EVUN_CLOUD_REGISTER_APPNAME + \
              '&index=' + settings.SWEETPY_EVUN_CLOUD_REGISTER_APP_PORT + \
              '&version=' + settings.SWEETPY_EVUN_CLOUD_REGISTER_APP_VERSION + \
              '&ticket=' + settings.SWEETPY_EVUN_CLOUD_REGISTER_APP_TICKET

        try:
            result = requests.get(url)
            result_dict = json.loads(result.text)
            if result_dict['code'] == 'success':
                print('evun cloud connected!')
                sweet_settings = result_dict['data']
                write_sweet_settings(sweet_settings)
            else:
                print('evun cloud error:' + result_dict['message'])
                quit(0)
        except Exception as e:
            print("can't connect to the evun cloud!")
            quit(0)
    else:
        pass

def set_django_connection(sweet_settings):
    if sweet_settings['applicationInstanceConfigurations'].get('spring.datasource.db-type', None) == None:
        return
    default = None
    try:
        _driver_name = sweet_settings['applicationInstanceConfigurations']['spring.datasource.db-type'].lower()
        _url = sweet_settings['applicationInstanceConfigurations']['spring.datasource.url']
        if _url.find(':') != -1:
            _ip = _url[:_url.find(':')]
            _port = _url[_url.find(':') + 1:]
        if _driver_name == 'postgres':
            default = {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': sweet_settings['applicationInstanceConfigurations']['spring.datasource.name'],
                'USER': sweet_settings['applicationInstanceConfigurations']['spring.datasource.username'],
                'PASSWORD': sweet_settings['applicationInstanceConfigurations']['spring.datasource.password'],
                'HOST': _ip,
                'PORT': _port,
                'CONN_MAX_AGE': int(sweet_settings['applicationInstanceConfigurations']['spring.datasource.maxActive'])
            }
        elif _driver_name == 'mysql':
            default = {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': sweet_settings['applicationInstanceConfigurations']['spring.datasource.name'],
                'USER': sweet_settings['applicationInstanceConfigurations']['spring.datasource.username'],
                'PASSWORD': sweet_settings['applicationInstanceConfigurations']['spring.datasource.password'],
                'HOST': _ip,
                'PORT': _port,
                'CONN_MAX_AGE': int(sweet_settings['applicationInstanceConfigurations']['spring.datasource.maxActive'])
            }
        elif _driver_name == 'sqlite':
            default = {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': _url,
            }
        if default:
            settings.DATABASES['default'] = default
    except Exception as e:
        print("数据配置错误,请配置以下字段:["
              "'spring.datasource.db-type':'数据库类型postgres,mysql等',"
              "'spring.datasource.username':'用户名',"
              "'spring.datasource.password':'密码',"
              "'spring.datasource.url':'IP地址和端口号以:号分隔',"
              "'spring.datasource.maxActive':'连接池大小',"
              "'spring.datasource.name':'要连接的仓库名',"
              "'spring.datasource.minIdle':'连接池回收时间(暂时未启用)']")
        quit(0)

zk_plus = None
def process_realms_change(*args):
    # print('process_realms_change')
    pass

def process_applicatins_change(*args):
    # print('process_applicatins_change')
    pass

def process_data_change(*args):
    # print('process_data_change')
    pass

def add_data_watch(node_path,func):
    global zk_plus
    if zk_plus == None:
        print('add_data_watch error: zk is None')
        return
    process_data_change = func
    @zk_plus.DataWatch(node_path)    #'/realms/python-sweet/8888'
    def data_watch(*args):
        process_data_change(args)

def process_node_change(*args):
    # print('process_node_change')
    pass

def add_node_watch(node_path,func):
    global zk_plus
    if zk_plus == None:
        print('add_node_watch error: zk is None')
        return
    process_node_change = func
    @zk_plus.ChildrenWatch(node_path)    #'/realms/python-sweet/8888'
    def children_watch(*args):
        process_node_change(args)

def zookeeper_on_line(sweet_settings):
    _zk_info = sweet_settings['zk']['zkConnectionString']
    _n_p = sweet_settings['zk']['zkDigestAuthString']
    _zk_username = _n_p[:_n_p.find(':')]
    _zk_password = _n_p[_n_p.find(':') + 1:]

    global zk_plus
    zk_plus = ZookeeperPlus(_zk_info, _zk_username, _zk_password)

    app_name = settings.SWEETPY_EVUN_CLOUD_REGISTER_APPNAME
    app_host = get_local_ip()#settings.SWEETPY_EVUN_CLOUD_REGISTER_APP_HOST
    app_port = settings.SWEETPY_EVUN_CLOUD_REGISTER_APP_PORT
    app_version = settings.SWEETPY_EVUN_CLOUD_REGISTER_APP_VERSION
    app_info_appliacations = zk_plus.create_app_infomation(app_name, app_version, app_host, app_port, '1.0')
    app_info_realms = zk_plus.create_app_infomation(app_name, app_version, app_host, app_port, '1.0',
                                                    state='Running')  # Running  Stoped
    app_runtime_data = zk_plus.create_runtime_data()

    # zk_plus.delete_app_path(app_name)
    zk_plus.set_configuration(app_name, app_port)
    zk_plus.set_dependencies(app_name, app_port)
    zk_plus.set_information(app_name, app_port, app_info_appliacations)
    zk_plus.set_metadata(app_name, app_port)
    zk_plus.set_runtime_data(app_name, app_port, app_runtime_data)
    zk_plus.set_realms(app_name, app_port, app_info_realms)
    print('APP['+ app_name + ']已注册到应用云平台!')

    # add_data_watch('/realms/python-sweet/8889',p_tes)
    # add_node_watch('/realms/python-sweet',p_tess)
    @zk_plus.ChildrenWatch('/realms')
    def watch_realms(*args):
        process_realms_change(args)

    @zk_plus.ChildrenWatch('/applications')
    def watch_applicatins(*args):
        process_applicatins_change(args)


def zookeeper_off_line():
    global sweet_settings
    if sweet_settings == None:
        return
    _zk_info = sweet_settings['zk']['zkConnectionString']
    _n_p = sweet_settings['zk']['zkDigestAuthString']
    _zk_username = _n_p[:_n_p.find(':')]
    _zk_password = _n_p[_n_p.find(':') + 1:]
    zk_plus = ZookeeperPlus(_zk_info, _zk_username, _zk_password)

    app_name = settings.SWEETPY_EVUN_CLOUD_REGISTER_APPNAME
    app_host = get_local_ip()#settings.SWEETPY_EVUN_CLOUD_REGISTER_APP_HOST
    app_port = settings.SWEETPY_EVUN_CLOUD_REGISTER_APP_PORT
    app_version = settings.SWEETPY_EVUN_CLOUD_REGISTER_APP_VERSION

    app_info_realms = zk_plus.create_app_infomation(app_name, app_version, app_host, app_port, '1.0',
                                                    state='Stoped')  # Running  Stoped
    zk_plus.set_realms(app_name, app_port, app_info_realms)
    print('APP[' + app_name + ']已从应用云平台离线!')
    filename = get_sweet_settings_local_filename()
    if os.path.exists(filename):
        with open(filename,'w') as f:
            f.write(json.dumps({},ensure_ascii=False))

def zookeeper_delete_self(sweet_settings):
    _zk_info = sweet_settings['zk']['zkConnectionString']
    _n_p = sweet_settings['zk']['zkDigestAuthString']
    _zk_username = _n_p[:_n_p.find(':')]
    _zk_password = _n_p[_n_p.find(':') + 1:]
    zk_plus = ZookeeperPlus(_zk_info, _zk_username, _zk_password)
    app_name = settings.SWEETPY_EVUN_CLOUD_REGISTER_APPNAME
    app_port = settings.SWEETPY_EVUN_CLOUD_REGISTER_APP_PORT
    zk_plus.delete_app_path(app_name,app_port)
    print('APP[' + app_name + ']已从应用云平台删除!')

def check_force_off_line_zookeeper():
    from sys import argv
    _argv_count = len(argv)
    if _argv_count > 1:
        for i in range(1, _argv_count):
            _argv = argv[i].lower()
            if _argv.startswith('--quitzookeeper'):
                print('--quitzookeeper')
                _sweet_settings = get_sweet_settings()
                zookeeper_delete_self(_sweet_settings)
                quit(0)

def isrun():
    filename = get_sweet_settings_local_filename()
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            sweet_settings = json.loads(f.read())
            return not sweet_settings
    else:
        return True

# check_force_off_line_zookeeper()
get_sweet_settings()

import signal

def stop(sig, former):
    zookeeper_off_line()
    quit(0)
signal.signal(signal.SIGINT, stop)
signal.signal(signal.SIGTERM, stop)
sysstr = platform.system()
if sysstr.lower() != 'windows':
    signal.signal(signal.SIGHUP, stop)

def set_http_port():
    global sweet_settings
    if not sweet_settings:
        return
    from django.core.management.commands.runserver import Command
    Command.default_port = settings.SWEETPY_EVUN_CLOUD_REGISTER_APP_PORT#get_http_port()

set_http_port()

if isrun():
    get_sweet_params_from_evun_colud()

    if sweet_settings:
        #设置django数据库
        set_django_connection(sweet_settings)
        #向应用云注册
        zookeeper_on_line(sweet_settings)
