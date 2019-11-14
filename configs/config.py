# coding:utf-8

import os
from tornado.options import define
from utils import utils

root_path = os.path.join(os.path.dirname(__file__), "..")
sub_static_path = "static"
static_path = os.path.join(root_path, sub_static_path)

# json配置文件里面的所有数据
_json_items = utils.read_json_file(
    os.path.dirname(
        os.path.realpath(__file__)) +
    '/config.json')


# 是否是开发模式中
IS_DEBUG = _json_items.get('is_debug')

# 日志路径
LOG_PATH = os.path.join(os.path.dirname(__file__), "logs")



# 杀进程前的等待时间
if IS_DEBUG:
    SHUTDOWN_WAIT_SECONDS = 1
else:
    SHUTDOWN_WAIT_SECONDS = 5


def get_by_key(key):
    return _json_items.get(key)


# cookie的签名key
define("cookie_secret", default="gBxEhXW9aCs6(a/gCxThJe", help="cookie加密密钥")
define('cookie_info', default='info.gl')  # 存放用户是否已经登录等cookie信息
define('cookie_info_timeout', default=30)  # 过期时间天数

# 微信开放平台APP_ID
define("we_chat_app_id", default="wxd85416f3ddeb9ef4", help="微信开放平台APP_ID")

# 微信开放平台APP_SECRET
define("we_chat_app_secret",default="e398f866f83eaa2960f108f6c6feccec",help="微信开放平台APP_SECRET")
