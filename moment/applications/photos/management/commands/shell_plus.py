from django.core.management.base import BaseCommand
from django.conf import settings
from django.apps import apps
import traceback


class Command(BaseCommand):
    help = "增强版的Django shell,自动导入常用模块"

    def import_models(self):
        """自动导入所有已注册的model"""
        model_dict = {}
        for app_config in apps.get_app_configs():
            app_label = app_config.label
            for model in app_config.get_models():
                model_name = model.__name__
                model_dict[model_name] = model
                # 添加 <app_label>_<model_name> 形式的别名
                model_dict[f"{app_label}_{model_name}"] = model
        return model_dict

    def handle(self, *args, **options):
        # 导入常用模块
        import code
        import datetime
        import decimal
        import json
        import os
        import sys
        import time
        import random

        # 导入Django相关
        from django.db.models import (
            Q, F, Count, Sum, Max, Min, Avg,
            Prefetch, Case, When, Value, ExpressionWrapper,
            IntegerField, FloatField, DateTimeField
        )
        from django.utils import timezone
        from django.core.cache import cache
        from django.db import transaction, connection
        from django.conf import settings

        # 导入项目模块
        from applications.photos import tasks, models
        
        # 自动导入所有已注册的model
        model_dict = self.import_models()
        
        # 合并所有本地变量
        context = globals().copy()
        context.update(locals())
        context.update(model_dict)

        # 打印帮助信息
        banner = """Django Shell Plus
            已导入模块:
            - Python: datetime, decimal, json, os, sys, time, random
            - Django ORM: Q, F, Count, Sum, Max, Min, Avg, Prefetch, Case, When, Value, ExpressionWrapper
            - Django: timezone, cache, transaction, connection, settings
            - 项目: utils, tasks, models
            - 所有Model都已自动导入,支持两种引用方式:
            1. 直接使用Model名称(如 User)
            2. 使用 app标签_Model名称(如 auth_User)
            """
        
        try:
            # 使用IPython shell如果已安装
            import IPython
            IPython.start_ipython(argv=[], user_ns=context, banner=banner)
        except ImportError:
            # 回退到标准Python shell    
            code.interact(banner=banner, local=context)
