from flask import Blueprint, request, jsonify, current_app
from datetime import datetime, timedelta
import jwt
from functools import wraps
from models import db, User

auth_bp = Blueprint('auth', __name__)


# JWT认证装饰器
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': '缺少认证令牌'}), 401

        try:
            if token.startswith('Bearer '):
                token = token[7:]
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.get(data['user_id'])
        except:
            return jsonify({'message': '认证令牌无效'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@auth_bp.route('/register', methods=['POST'])
def register():
    """用户注册"""
    data = request.get_json()

    # 验证必需字段
    required_fields = ['name', 'phone', 'password', 'user_type']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'缺少必需字段: {field}'}), 400

    # 检查手机号是否已存在
    if User.query.filter_by(phone=data['phone']).first():
        return jsonify({'error': '手机号已被注册'}), 400

    # 验证用户类型
    if data['user_type'] not in ['passenger', 'driver']:
        return jsonify({'error': '用户类型无效'}), 400

    # 创建新用户
    user = User(
        name=data['name'],
        phone=data['phone'],
        user_type=data['user_type']
    )
    user.set_password(data['password'])

    # 如果是司机，添加车辆信息
    if data['user_type'] == 'driver':
        user.car_model = data.get('car_model', '')
        user.plate_number = data.get('plate_number', '')

    try:
        db.session.add(user)
        db.session.commit()

        # 生成JWT令牌
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(days=30)
        }, current_app.config['SECRET_KEY'], algorithm='HS256')

        return jsonify({
            'message': '注册成功',
            'token': token,
            'user': user.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '注册失败'}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.get_json()

    if not data.get('phone') or not data.get('password'):
        return jsonify({'error': '缺少手机号或密码'}), 400

    user = User.query.filter_by(phone=data['phone']).first()

    if not user or not user.check_password(data['password']):
        return jsonify({'error': '手机号或密码错误'}), 401

    # 生成JWT令牌
    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(days=30)
    }, current_app.config['SECRET_KEY'], algorithm='HS256')

    return jsonify({
        'message': '登录成功',
        'token': token,
        'user': user.to_dict()
    })


@auth_bp.route('/user/profile', methods=['GET'])
@token_required
def get_profile(current_user):
    """获取用户资料"""
    return jsonify(current_user.to_dict())


@auth_bp.route('/user/profile', methods=['PUT'])
@token_required
def update_profile(current_user):
    """更新用户资料"""
    data = request.get_json()

    try:
        if data.get('name'):
            current_user.name = data['name']

        if current_user.user_type == 'driver':
            if data.get('car_model'):
                current_user.car_model = data['car_model']
            if data.get('plate_number'):
                current_user.plate_number = data['plate_number']

        db.session.commit()

        return jsonify({
            'message': '资料更新成功',
            'user': current_user.to_dict()
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '更新失败'}), 500


@auth_bp.route('/messages', methods=['GET'])
@token_required
def get_messages(current_user):
    """获取消息列表"""
    from models import Message
    messages = Message.query.filter(
        (Message.sender_id == current_user.id) | (Message.receiver_id == current_user.id)
    ).order_by(Message.created_at.desc()).all()

    return jsonify([message.to_dict() for message in messages])


@auth_bp.route('/messages', methods=['POST'])
@token_required
def send_message(current_user):
    """发送消息"""
    from models import Message
    data = request.get_json()

    if not data.get('receiver_id') or not data.get('content'):
        return jsonify({'error': '缺少接收者或消息内容'}), 400

    try:
        message = Message(
            sender_id=current_user.id,
            receiver_id=data['receiver_id'],
            content=data['content']
        )

        db.session.add(message)
        db.session.commit()

        return jsonify({
            'message': '消息发送成功',
            'data': message.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '发送失败'}), 500