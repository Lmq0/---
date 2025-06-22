from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime
import os

# 导入配置和模型
from config import get_config
from models import db
from auth import auth_bp
from trips import trips_bp


def create_app(config_name=None):
    """应用工厂函数"""
    app = Flask(__name__)

    # 加载配置
    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG', 'development')

    config_class = get_config()
    app.config.from_object(config_class)

    # 初始化扩展
    db.init_app(app)
    CORS(app, origins=app.config['CORS_ORIGINS'])

    # 注册蓝图
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(trips_bp, url_prefix='/api')

    # 注册路由
    register_routes(app)

    # 注册错误处理器
    register_error_handlers(app)

    # 注册CLI命令
    register_cli_commands(app)

    return app


def register_routes(app):
    """注册基础路由"""

    @app.route('/')
    def index():
        """主页"""
        return jsonify({
            'message': '拼车应用API',
            'version': '1.0.0',
            'docs': '/api/health'
        })

    @app.route('/api/health', methods=['GET'])
    def health_check():
        """健康检查端点"""
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'version': '1.0.0',
            'environment': app.config.get('ENV', 'development')
        })

    @app.route('/api/info', methods=['GET'])
    def app_info():
        """应用信息"""
        with app.app_context():
            from models import User, Trip, RideRequest, Booking

            try:
                stats = {
                    'users': User.query.count(),
                    'trips': Trip.query.count(),
                    'ride_requests': RideRequest.query.count(),
                    'bookings': Booking.query.count()
                }
            except Exception:
                stats = {
                    'users': 0,
                    'trips': 0,
                    'ride_requests': 0,
                    'bookings': 0,
                    'note': '数据库未初始化'
                }

        return jsonify({
            'app': '拼车应用',
            'version': '1.0.0',
            'environment': app.config.get('ENV', 'development'),
            'debug': app.debug,
            'database_stats': stats,
            'endpoints': {
                'health': '/api/health',
                'auth': '/api/login, /api/register',
                'trips': '/api/trips',
                'requests': '/api/ride-requests',
                'bookings': '/api/bookings'
            }
        })


def register_error_handlers(app):
    """注册错误处理器"""

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': '请求参数错误'}), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({'error': '未授权访问'}), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({'error': '禁止访问'}), 403

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': '请求的资源不存在'}), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({'error': '请求方法不被允许'}), 405

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({'error': '服务器内部错误'}), 500

    @app.errorhandler(Exception)
    def handle_exception(error):
        # 记录错误日志
        app.logger.error(f'Unhandled exception: {error}')
        db.session.rollback()

        if app.debug:
            # 开发环境返回详细错误信息
            return jsonify({
                'error': '服务器错误',
                'message': str(error),
                'type': error.__class__.__name__
            }), 500
        else:
            # 生产环境返回通用错误信息
            return jsonify({'error': '服务器内部错误'}), 500


def register_cli_commands(app):
    """注册CLI命令"""

    @app.cli.command()
    def init_db():
        """初始化数据库"""
        from init_db import init_all_data
        with app.app_context():
            init_all_data()

    @app.cli.command()
    def reset_db():
        """重置数据库"""
        from init_db import reset_database
        with app.app_context():
            reset_database()

    @app.cli.command()
    def create_admin():
        """创建管理员用户"""
        from models import User
        with app.app_context():
            admin = User.query.filter_by(phone='admin').first()
            if admin:
                print('管理员已存在')
                return

            admin = User(
                name='管理员',
                phone='admin',
                user_type='admin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print('管理员创建成功: admin / admin123')


# 创建应用实例（用于直接运行）
app = create_app()

if __name__ == '__main__':
    # 直接运行时的配置
    with app.app_context():
        # 确保数据库表存在
        db.create_all()

        # 检查是否需要初始化数据
        from models import User

        if User.query.count() == 0:
            print("🔧 检测到空数据库，自动初始化...")
            from init_db import init_all_data

            init_all_data()

    # 启动开发服务器
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'

    print(f"🚀 启动拼车应用...")
    print(f"📍 访问地址: http://localhost:{port}")
    print(f"📍 健康检查: http://localhost:{port}/api/health")
    print(f"📍 应用信息: http://localhost:{port}/api/info")

    app.run(
        debug=debug,
        host='0.0.0.0',
        port=port
    )