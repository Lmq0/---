#!/usr/bin/env python3
"""
数据库初始化脚本
用于创建数据库表和初始化测试数据
"""

import os
import sys
from datetime import datetime, timedelta

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db, User, Trip, RideRequest, Booking, Message


def create_database():
    """创建数据库表"""
    print("正在创建数据库表...")
    db.create_all()
    print("✅ 数据库表创建成功!")


def drop_database():
    """删除所有数据库表"""
    print("正在删除数据库表...")
    db.drop_all()
    print("✅ 数据库表删除成功!")


def create_test_users():
    """创建测试用户"""
    print("正在创建测试用户...")

    # 检查是否已存在用户
    if User.query.first():
        print("⚠️  用户已存在，跳过用户创建")
        return

    # 创建测试司机
    drivers_data = [
        {
            'name': '张师傅',
            'phone': '13812345678',
            'password': '123456',
            'car_model': '大众朗逸',
            'plate_number': '沪A12345',
            'rating': 4.8,
            'completed_trips': 156
        },
        {
            'name': '王师傅',
            'phone': '13812345679',
            'password': '123456',
            'car_model': '本田雅阁',
            'plate_number': '沪B67890',
            'rating': 4.9,
            'completed_trips': 200
        },
        {
            'name': '李师傅',
            'phone': '13812345680',
            'password': '123456',
            'car_model': '丰田凯美瑞',
            'plate_number': '沪C88888',
            'rating': 4.7,
            'completed_trips': 120
        }
    ]

    drivers = []
    for driver_data in drivers_data:
        driver = User(
            name=driver_data['name'],
            phone=driver_data['phone'],
            user_type='driver',
            car_model=driver_data['car_model'],
            plate_number=driver_data['plate_number'],
            rating=driver_data['rating'],
            completed_trips=driver_data['completed_trips']
        )
        driver.set_password(driver_data['password'])
        drivers.append(driver)
        db.session.add(driver)

    # 创建测试乘客
    passengers_data = [
        {
            'name': '小明同学',
            'phone': '13987654321',
            'password': '123456'
        },
        {
            'name': '小红同学',
            'phone': '13987654322',
            'password': '123456'
        },
        {
            'name': '小华同学',
            'phone': '13987654323',
            'password': '123456'
        }
    ]

    passengers = []
    for passenger_data in passengers_data:
        passenger = User(
            name=passenger_data['name'],
            phone=passenger_data['phone'],
            user_type='passenger'
        )
        passenger.set_password(passenger_data['password'])
        passengers.append(passenger)
        db.session.add(passenger)

    db.session.commit()
    print(f"✅ 创建了 {len(drivers)} 个司机和 {len(passengers)} 个乘客")
    return drivers, passengers


def create_test_trips():
    """创建测试行程"""
    print("正在创建测试行程...")

    # 获取司机用户
    drivers = User.query.filter_by(user_type='driver').all()
    if not drivers:
        print("❌ 没有找到司机用户，请先创建用户")
        return

    # 检查是否已存在行程
    if Trip.query.first():
        print("⚠️  行程已存在，跳过行程创建")
        return

    trips_data = [
        {
            'start_point': '同济大学（嘉定校区）',
            'end_point': '虹桥火车站',
            'departure_time': datetime.now() + timedelta(hours=2),
            'available_seats': 3,
            'price': 25,
            'status': 'active'
        },
        {
            'start_point': '嘉定北站',
            'end_point': '人民广场',
            'departure_time': datetime.now() + timedelta(hours=4),
            'available_seats': 2,
            'price': 28,
            'status': 'active'
        },
        {
            'start_point': '同济大学（嘉定校区）',
            'end_point': '上海迪士尼度假区',
            'departure_time': datetime.now() + timedelta(hours=6),
            'available_seats': 4,
            'price': 35,
            'status': 'active'
        },
        {
            'start_point': '安亭地铁站',
            'end_point': '徐家汇',
            'departure_time': datetime.now() + timedelta(hours=8),
            'available_seats': 3,
            'price': 32,
            'status': 'active'
        },
        {
            'start_point': '同济大学（嘉定校区）',
            'end_point': '浦东机场',
            'departure_time': datetime.now() + timedelta(days=1, hours=2),
            'available_seats': 2,
            'price': 45,
            'status': 'active'
        }
    ]

    trips = []
    for i, trip_data in enumerate(trips_data):
        trip = Trip(
            driver_id=drivers[i % len(drivers)].id,
            start_point=trip_data['start_point'],
            end_point=trip_data['end_point'],
            departure_time=trip_data['departure_time'],
            available_seats=trip_data['available_seats'],
            price=trip_data['price'],
            status=trip_data['status']
        )
        trips.append(trip)
        db.session.add(trip)

    db.session.commit()
    print(f"✅ 创建了 {len(trips)} 个测试行程")
    return trips


def create_test_ride_requests():
    """创建测试拼车请求"""
    print("正在创建测试拼车请求...")

    # 获取乘客用户
    passengers = User.query.filter_by(user_type='passenger').all()
    if not passengers:
        print("❌ 没有找到乘客用户，请先创建用户")
        return

    # 检查是否已存在拼车请求
    if RideRequest.query.first():
        print("⚠️  拼车请求已存在，跳过创建")
        return

    requests_data = [
        {
            'start_point': '同济大学嘉定校区',
            'end_point': '人民广场',
            'departure_time': datetime.now() + timedelta(hours=3),
            'seats': 1,
            'note': '希望拼车去市区逛街',
            'status': 'active'
        },
        {
            'start_point': '同济大学嘉定校区',
            'end_point': '浦东机场',
            'departure_time': datetime.now() + timedelta(hours=5),
            'seats': 2,
            'note': '赶飞机，时间比较急，谢谢！',
            'status': 'active'
        },
        {
            'start_point': '嘉定北站',
            'end_point': '静安寺',
            'departure_time': datetime.now() + timedelta(hours=4),
            'seats': 1,
            'note': '去市区办事',
            'status': 'active'
        }
    ]

    requests = []
    for i, request_data in enumerate(requests_data):
        ride_request = RideRequest(
            passenger_id=passengers[i % len(passengers)].id,
            start_point=request_data['start_point'],
            end_point=request_data['end_point'],
            departure_time=request_data['departure_time'],
            seats=request_data['seats'],
            note=request_data['note'],
            status=request_data['status']
        )
        requests.append(ride_request)
        db.session.add(ride_request)

    db.session.commit()
    print(f"✅ 创建了 {len(requests)} 个测试拼车请求")
    return requests


def create_sample_bookings():
    """创建示例预订记录"""
    print("正在创建示例预订记录...")

    # 获取用户和行程
    passengers = User.query.filter_by(user_type='passenger').all()
    trips = Trip.query.filter_by(status='active').all()

    if not passengers or not trips:
        print("⚠️  没有足够的用户或行程数据，跳过预订创建")
        return

    # 创建几个预订记录
    bookings_data = [
        {
            'trip_index': 0,
            'passenger_index': 0,
            'seats': 1,
            'status': 'confirmed',
            'paid': True
        },
        {
            'trip_index': 1,
            'passenger_index': 1,
            'seats': 2,
            'status': 'confirmed',
            'paid': False
        }
    ]

    bookings = []
    for booking_data in bookings_data:
        if (booking_data['trip_index'] < len(trips) and
                booking_data['passenger_index'] < len(passengers)):
            trip = trips[booking_data['trip_index']]
            passenger = passengers[booking_data['passenger_index']]

            booking = Booking(
                trip_id=trip.id,
                passenger_id=passenger.id,
                seats=booking_data['seats'],
                amount=trip.price * booking_data['seats'],
                status=booking_data['status'],
                paid=booking_data['paid']
            )

            # 更新行程可用座位
            trip.available_seats -= booking_data['seats']

            bookings.append(booking)
            db.session.add(booking)

    db.session.commit()
    print(f"✅ 创建了 {len(bookings)} 个示例预订")
    return bookings


def init_all_data():
    """初始化所有测试数据"""
    print("🚀 开始初始化数据库...")

    try:
        # 创建数据库表
        create_database()

        # 创建测试数据
        drivers, passengers = create_test_users()
        trips = create_test_trips()
        requests = create_test_ride_requests()
        bookings = create_sample_bookings()

        print("\n🎉 数据库初始化完成!")
        print(f"📊 数据统计:")
        print(f"   👥 用户: {User.query.count()} 个")
        print(f"   🚗 行程: {Trip.query.count()} 个")
        print(f"   📝 拼车请求: {RideRequest.query.count()} 个")
        print(f"   🎫 预订记录: {Booking.query.count()} 个")

        print(f"\n🔑 测试账号:")
        print(f"   🚗 司机: 13812345678 / 123456")
        print(f"   👤 乘客: 13987654321 / 123456")

    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        db.session.rollback()
        raise


def reset_database():
    """重置数据库（删除所有数据并重新创建）"""
    print("🔄 重置数据库...")

    try:
        drop_database()
        init_all_data()
        print("✅ 数据库重置完成!")

    except Exception as e:
        print(f"❌ 重置失败: {e}")
        raise


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description='数据库管理脚本')
    parser.add_argument('action', choices=['init', 'reset', 'create', 'drop'],
                        help='要执行的操作')

    args = parser.parse_args()

    # 创建应用上下文
    app = create_app()

    with app.app_context():
        if args.action == 'init':
            init_all_data()
        elif args.action == 'reset':
            reset_database()
        elif args.action == 'create':
            create_database()
        elif args.action == 'drop':
            drop_database()


if __name__ == '__main__':
    main()