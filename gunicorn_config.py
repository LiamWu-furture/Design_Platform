# Gunicorn 配置文件
import multiprocessing
import os

# 监听地址 (宝塔会自动覆盖此配置，但保留作为默认值)
bind = "0.0.0.0:8000"

# 进程数
workers = 4

# 工作模式：gevent (必须使用 gevent 以支持 Flask 的流式响应)
worker_class = "gevent"

# 超时时间：600秒 (AI生成内容耗时较长，必须设置较大的超时时间，否则会报502错误)
timeout = 600

# 保持连接
keepalive = 5

# 日志级别
loglevel = 'info'
accesslog = '-'
errorlog = '-'

# 预加载应用代码，加快启动速度
preload_app = True
