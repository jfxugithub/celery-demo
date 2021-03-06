#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/1/16 下午3:58
# @Author : Matrix
# @Github : https://github.com/blackmatrix7/
# @Blog : http://www.cnblogs.com/blackmatrix/
# @File : config.py.py
# @Software: PyCharm
from kombu import Queue
from datetime import timedelta
from toolkit.config import BaseConfig, get_current_config

__author__ = 'blackmatrix'


class CommonConfig(BaseConfig):

    # Celery 配置
    # broker 推荐 rabbitmq
    CELERY_BROKER_URL = 'amqp://user:password@127.0.0.1:5672//'
    # backend 用于存储数据，推荐redis
    CELERY_RESULT_BACKEND = 'amqp://user:password@127.0.0.1:5672//'
    CELERY_ACCEPT_CONTENT = ['json', 'pickle']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'pickle'
    CELERY_REDIRECT_STDOUTS_LEVEL = 'INFO'
    CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
    # 导入Task所在的模块
    CELERY_IMPORTS = ('handlers.async_tasks', 'handlers.schedules')
    # celery worker 的并发数
    CELERYD_CONCURRENCY = 3
    # 创建多个队列，及对应的交换机
    CELERY_QUEUES = (
        Queue(name='email_queue', routing_key='email_router'),
        Queue(name='message_queue', routing_key='message_router'),
        Queue(name='schedules_queue', routing_key='schedules_router'),
    )
    # 为不同的task指派不同的队列
    CELERY_ROUTES = {
        'handlers.async_tasks.async_send_email': {
            'queue': 'email_queue',
            'routing_key': 'vcan.email_router',
        },
        'handlers.async_tasks.async_push_message': {
            'queue': 'message_queue',
            'routing_key': 'message_router',
        },
        'handlers.schedules.test_func_a': {
            'queue': 'schedules_queue',
            'routing_key': 'schedules_router',
        },
        'handlers.schedules.test_func_b': {
            'queue': 'schedules_queue',
            'routing_key': 'schedules_router',
        }
    }
    # Celery 时区，定时任务需要
    CELERY_TIMEZONE = 'Asia/Shanghai'
    # 定时任务 schedules
    CELERYBEAT_SCHEDULE = {
        'every-30-seconds': {
             'task': 'handlers.schedules.test_func_a',
             # 每 30 秒执行一次
             'schedule': timedelta(seconds=30),
             # 任务函数参数
             'args': {'value': '2333333'}
        }
    }


class DefaultConfig(CommonConfig):
    pass


default = DefaultConfig()

configs = {
    'default': default
}

# 读取配置文件的名称，在具体的应用中，可以从环境变量、命令行参数等位置获取配置文件名称
config_name = 'default'
current_config = get_current_config(config_name)
