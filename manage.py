from flask_script import Manager
from app import create_app
from flask_migrate import MigrateCommand
import os


# 获取配置
config_name = os.environ.get('FLASK_CONFIG') or 'default'

# 根据配置创建app实例对象
app = create_app(config_name)

# 生成Manager实例
manager = Manager(app)

# 配置迁移
manager.add_command('db', MigrateCommand)

# 启动
if __name__ == '__main__':
    manager.run()