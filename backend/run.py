#!/usr/bin/env python3
"""
Flask应用启动脚本
提供灵活的启动选项和环境配置
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db
from config import get_config


def check_dependencies():
    """检查必要的依赖是否已安装"""
    print("🔍 检查依赖...")

    try:
        import flask
        import flask_sqlalchemy
        import flask_cors
        import jwt
        print("✅ 所有依赖已安装")
        return True
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("请运行: pip install -r requirements.txt")
        return False


def check_database():
    """检查数据库是否存在并已初始化"""
    config = get_config()
    db_path = config.SQLALCHEMY_DATABASE_URI.replace('sqlite:///', '')

    if not os.path.exists(db_path):
        print(f"⚠️  数据库文件不存在: {db_path}")
        return False

    # 检查是否有表
    app = create_app()
    with app.app_context():
        try:
            from models import User
            user_count = User.query.count()
            print(f"✅ 数据库已初始化，用户数: {user_count}")
            return True
        except Exception as e:
            print(f"⚠️  数据库可能未初始化: {e}")
            return False


def init_database():
    """初始化数据库"""
    print("🚀 初始化数据库...")

    try:
        from init_db import init_all_data
        app = create_app()
        with app.app_context():
            init_all_data()
        print("✅ 数据库初始化完成")
        return True
    except Exception as e:
        print(f"❌ 数据库初始化失败: {e}")
        return False


def run_development_server(host='0.0.0.0', port=5000, debug=True):
    """运行开发服务器"""
    print(f"🚀 启动开发服务器...")
    print(f"📍 地址: http://{host}:{port}")
    print(f"🔧 调试模式: {'开启' if debug else '关闭'}")

    app = create_app()

    # 确保数据库表存在
    with app.app_context():
        db.create_all()

    try:
        app.run(
            host=host,
            port=port,
            debug=debug,
            use_reloader=debug,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n⏹️  服务器已停止")
    except Exception as e:
        print(f"❌ 服务器启动失败: {e}")


def run_production_server(host='0.0.0.0', port=5000, workers=4):
    """使用Gunicorn运行生产服务器"""
    print(f"🏭 启动生产服务器...")
    print(f"📍 地址: http://{host}:{port}")
    print(f"👷 工作进程: {workers}")

    # 检查是否安装了gunicorn
    try:
        import gunicorn
    except ImportError:
        print("❌ 未安装gunicorn，正在安装...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'gunicorn'])

    # 设置生产环境
    os.environ['FLASK_CONFIG'] = 'production'

    # 启动gunicorn
    cmd = [
        'gunicorn',
        '-w', str(workers),
        '-b', f'{host}:{port}',
        '--access-logfile', '-',
        '--error-logfile', '-',
        'app:create_app()'
    ]

    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n⏹️  生产服务器已停止")
    except Exception as e:
        print(f"❌ 生产服务器启动失败: {e}")


def run_tests():
    """运行测试"""
    print("🧪 运行测试...")

    # 设置测试环境
    os.environ['FLASK_CONFIG'] = 'testing'

    try:
        # 使用pytest运行测试
        import pytest
        pytest.main(['-v', 'tests/'])
    except ImportError:
        print("⚠️  pytest未安装，尝试使用unittest...")
        import unittest
        loader = unittest.TestLoader()
        suite = loader.discover('tests')
        runner = unittest.TextTestRunner(verbosity=2)
        runner.run(suite)


def show_routes():
    """显示所有路由"""
    print("🗺️  应用路由:")

    app = create_app()

    with app.app_context():
        for rule in app.url_map.iter_rules():
            methods = ', '.join(sorted(rule.methods - {'HEAD', 'OPTIONS'}))
            print(f"  {rule.endpoint:30} {methods:10} {rule.rule}")


def create_admin_user():
    """创建管理员用户"""
    print("👑 创建管理员用户...")

    app = create_app()

    with app.app_context():
        from models import User

        # 检查是否已有管理员
        admin = User.query.filter_by(phone='admin').first()
        if admin:
            print("⚠️  管理员用户已存在")
            return

        # 创建管理员用户
        admin = User(
            name='系统管理员',
            phone='admin',
            user_type='admin'
        )
        admin.set_password('admin123')

        db.session.add(admin)
        db.session.commit()

        print("✅ 管理员用户创建成功")
        print("📧 账号: admin")
        print("🔑 密码: admin123")


def show_status():
    """显示应用状态"""
    print("📊 应用状态:")

    # 检查配置
    config = get_config()
    print(f"  🔧 配置: {config.__name__}")
    print(f"  🗄️  数据库: {config.SQLALCHEMY_DATABASE_URI}")
    print(f"  🔐 密钥: {'已设置' if config.SECRET_KEY != 'dev' else '默认值'}")

    # 检查数据库
    if check_database():
        app = create_app()
        with app.app_context():
            from models import User, Trip, RideRequest, Booking
            print(f"  👥 用户数: {User.query.count()}")
            print(f"  🚗 行程数: {Trip.query.count()}")
            print(f"  📝 请求数: {RideRequest.query.count()}")
            print(f"  🎫 预订数: {Booking.query.count()}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='拼车应用启动脚本')

    # 子命令
    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # 开发服务器
    dev_parser = subparsers.add_parser('dev', help='启动开发服务器')
    dev_parser.add_argument('--host', default='0.0.0.0', help='主机地址')
    dev_parser.add_argument('--port', type=int, default=5000, help='端口号')
    dev_parser.add_argument('--no-debug', action='store_true', help='禁用调试模式')

    # 生产服务器
    prod_parser = subparsers.add_parser('prod', help='启动生产服务器')
    prod_parser.add_argument('--host', default='0.0.0.0', help='主机地址')
    prod_parser.add_argument('--port', type=int, default=5000, help='端口号')
    prod_parser.add_argument('--workers', type=int, default=4, help='工作进程数')

    # 数据库管理
    subparsers.add_parser('init-db', help='初始化数据库')
    subparsers.add_parser('reset-db', help='重置数据库')

    # 其他工具
    subparsers.add_parser('test', help='运行测试')
    subparsers.add_parser('routes', help='显示路由')
    subparsers.add_parser('status', help='显示状态')
    subparsers.add_parser('create-admin', help='创建管理员用户')

    args = parser.parse_args()

    # 如果没有提供命令，默认启动开发服务器
    if not args.command:
        args.command = 'dev'
        args.host = '0.0.0.0'
        args.port = 5000
        args.no_debug = False

    # 检查依赖
    if not check_dependencies():
        sys.exit(1)

    # 执行命令
    if args.command == 'dev':
        # 检查数据库
        if not check_database():
            print("🔧 自动初始化数据库...")
            if not init_database():
                sys.exit(1)

        run_development_server(
            host=args.host,
            port=args.port,
            debug=not args.no_debug
        )

    elif args.command == 'prod':
        run_production_server(
            host=args.host,
            port=args.port,
            workers=args.workers
        )

    elif args.command == 'init-db':
        init_database()

    elif args.command == 'reset-db':
        from init_db import reset_database
        app = create_app()
        with app.app_context():
            reset_database()

    elif args.command == 'test':
        run_tests()

    elif args.command == 'routes':
        show_routes()

    elif args.command == 'status':
        show_status()

    elif args.command == 'create-admin':
        create_admin_user()


if __name__ == '__main__':
    main()