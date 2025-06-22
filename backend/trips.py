from flask import Blueprint, request, jsonify
from datetime import datetime
from models import db, Trip, RideRequest, Booking, User
from auth import token_required

trips_bp = Blueprint('trips', __name__)


@trips_bp.route('/trips', methods=['GET'])
def get_trips():
    """获取可用行程列表"""
    trips = Trip.query.filter_by(status='active').order_by(Trip.departure_time).all()
    return jsonify([trip.to_dict() for trip in trips])


@trips_bp.route('/trips', methods=['POST'])
@token_required
def create_trip(current_user):
    """司机创建行程"""
    if current_user.user_type != 'driver':
        return jsonify({'error': '只有司机可以创建行程'}), 403

    data = request.get_json()
    required_fields = ['start_point', 'end_point', 'departure_time', 'available_seats', 'price']

    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'缺少必需字段: {field}'}), 400

    try:
        # 解析时间
        departure_time = datetime.strptime(data['departure_time'], '%Y-%m-%dT%H:%M')

        # 验证时间不能是过去
        if departure_time <= datetime.now():
            return jsonify({'error': '出发时间不能是过去时间'}), 400

    except ValueError:
        return jsonify({'error': '时间格式错误，应为 YYYY-MM-DDTHH:MM'}), 400

    try:
        trip = Trip(
            driver_id=current_user.id,
            start_point=data['start_point'],
            end_point=data['end_point'],
            departure_time=departure_time,
            available_seats=int(data['available_seats']),
            price=float(data['price'])
        )

        db.session.add(trip)
        db.session.commit()

        return jsonify({
            'message': '行程创建成功',
            'trip': trip.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '创建行程失败'}), 500


@trips_bp.route('/my-trips', methods=['GET'])
@token_required
def get_my_trips(current_user):
    """获取我的行程"""
    if current_user.user_type == 'driver':
        # 司机查看自己创建的行程
        trips = Trip.query.filter_by(driver_id=current_user.id).order_by(Trip.departure_time.desc()).all()
        return jsonify([trip.to_dict() for trip in trips])
    else:
        # 乘客查看自己的预订
        bookings = Booking.query.filter_by(passenger_id=current_user.id).order_by(Booking.created_at.desc()).all()
        return jsonify([booking.to_dict() for booking in bookings])


@trips_bp.route('/bookings', methods=['POST'])
@token_required
def create_booking(current_user):
    """预订行程"""
    if current_user.user_type != 'passenger':
        return jsonify({'error': '只有乘客可以预订行程'}), 403

    data = request.get_json()
    trip_id = data.get('trip_id')
    seats = data.get('seats', 1)

    if not trip_id:
        return jsonify({'error': '缺少行程ID'}), 400

    trip = Trip.query.get(trip_id)
    if not trip:
        return jsonify({'error': '行程不存在'}), 404

    if trip.status != 'active':
        return jsonify({'error': '行程不可预订'}), 400

    if trip.available_seats < seats:
        return jsonify({'error': '座位不足'}), 400

    # 检查是否已经预订过这个行程
    existing_booking = Booking.query.filter_by(
        trip_id=trip_id,
        passenger_id=current_user.id
    ).first()

    if existing_booking:
        return jsonify({'error': '您已经预订过这个行程'}), 400

    try:
        # 计算总价
        amount = trip.price * seats

        booking = Booking(
            trip_id=trip_id,
            passenger_id=current_user.id,
            seats=seats,
            amount=amount
        )

        # 更新可用座位数
        trip.available_seats -= seats

        # 如果座位订满，更新行程状态
        if trip.available_seats == 0:
            trip.status = 'ongoing'

        db.session.add(booking)
        db.session.commit()

        return jsonify({
            'message': '预订成功',
            'booking': booking.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '预订失败'}), 500


@trips_bp.route('/ride-requests', methods=['GET'])
@token_required
def get_ride_requests(current_user):
    """获取拼车请求列表"""
    if current_user.user_type == 'driver':
        # 司机查看所有活跃的拼车请求
        requests = RideRequest.query.filter_by(status='active').order_by(RideRequest.departure_time).all()
    else:
        # 乘客查看自己的拼车请求
        requests = RideRequest.query.filter_by(passenger_id=current_user.id).order_by(
            RideRequest.created_at.desc()).all()

    return jsonify([req.to_dict() for req in requests])


@trips_bp.route('/ride-requests', methods=['POST'])
@token_required
def create_ride_request(current_user):
    """乘客发布拼车请求"""
    if current_user.user_type != 'passenger':
        return jsonify({'error': '只有乘客可以发布拼车请求'}), 403

    data = request.get_json()
    required_fields = ['start_point', 'end_point', 'departure_time', 'seats']

    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'缺少必需字段: {field}'}), 400

    try:
        # 解析时间
        departure_time = datetime.strptime(data['departure_time'], '%Y-%m-%dT%H:%M')

        # 验证时间不能是过去
        if departure_time <= datetime.now():
            return jsonify({'error': '出发时间不能是过去时间'}), 400

    except ValueError:
        return jsonify({'error': '时间格式错误'}), 400

    try:
        ride_request = RideRequest(
            passenger_id=current_user.id,
            start_point=data['start_point'],
            end_point=data['end_point'],
            departure_time=departure_time,
            seats=int(data['seats']),
            note=data.get('note', '')
        )

        db.session.add(ride_request)
        db.session.commit()

        return jsonify({
            'message': '拼车请求发布成功',
            'request': ride_request.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '发布失败'}), 500


@trips_bp.route('/bookings/<int:booking_id>/cancel', methods=['PUT'])
@token_required
def cancel_booking(current_user, booking_id):
    """取消预订"""
    booking = Booking.query.get(booking_id)

    if not booking:
        return jsonify({'error': '预订不存在'}), 404

    if booking.passenger_id != current_user.id:
        return jsonify({'error': '无权操作此预订'}), 403

    if booking.status != 'confirmed':
        return jsonify({'error': '预订状态不允许取消'}), 400

    try:
        # 恢复行程座位数
        trip = Trip.query.get(booking.trip_id)
        trip.available_seats += booking.seats

        # 如果行程状态是ongoing，改回active
        if trip.status == 'ongoing' and trip.available_seats > 0:
            trip.status = 'active'

        # 更新预订状态
        booking.status = 'cancelled'

        db.session.commit()

        return jsonify({'message': '取消预订成功'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '取消失败'}), 500


@trips_bp.route('/trips/<int:trip_id>/complete', methods=['PUT'])
@token_required
def complete_trip(current_user, trip_id):
    """结束行程（司机操作）"""
    trip = Trip.query.get(trip_id)

    if not trip:
        return jsonify({'error': '行程不存在'}), 404

    if trip.driver_id != current_user.id:
        return jsonify({'error': '无权操作此行程'}), 403

    if trip.status not in ['active', 'ongoing']:
        return jsonify({'error': '行程状态不允许结束'}), 400

    try:
        # 更新行程状态
        trip.status = 'completed'

        # 更新所有相关预订状态
        bookings = Booking.query.filter_by(trip_id=trip_id).all()
        for booking in bookings:
            if booking.status == 'confirmed':
                booking.status = 'completed'

        # 更新司机完成行程数
        current_user.completed_trips += 1

        db.session.commit()

        return jsonify({'message': '行程已结束'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '操作失败'}), 500