import React, { useState, useEffect } from 'react';
import {
  MapPin,
  Search,
  Plus,
  Minus,
  Car,
  Clock,
  Users,
  DollarSign,
  MessageCircle,
  User,
  Home,
  Route,
  Star,
  Check,
  X,
  Navigation,
  Calendar,
  CreditCard,
  Settings,
  Phone,
  Shield
} from 'lucide-react';

const RideShareApp = () => {
  const [currentPage, setCurrentPage] = useState('login');
  const [userType, setUserType] = useState('passenger'); // 'passenger' or 'driver'
  const [user, setUser] = useState(null);
  const [activeTab, setActiveTab] = useState('home');
  const [seatCount, setSeatCount] = useState(1);
  const [showError, setShowError] = useState('');

  // 模拟数据
  const [trips, setTrips] = useState([
    {
      id: 1,
      startPoint: '同济大学（嘉定校区）',
      endPoint: '虹桥火车站',
      departureTime: '2025-06-23 08:00',
      availableSeats: 3,
      price: 25,
      carModel: '大众朗逸',
      plateNumber: '沪A12345',
      status: 'completed',
      paid: true,
      amount: 25
    },
    {
      id: 2,
      startPoint: '同济大学（嘉定校区）',
      endPoint: '上海迪士尼度假区',
      departureTime: '2025-06-23 14:00',
      availableSeats: 2,
      price: 35,
      carModel: '本田雅阁',
      plateNumber: '沪B67890',
      status: 'completed',
      paid: false,
      amount: 35
    }
  ]);

  const [rideRequests, setRideRequests] = useState([
    {
      id: 1,
      passengerName: '张同学',
      startPoint: '同济大学嘉定校区',
      endPoint: '人民广场',
      departureTime: '2025-06-23 09:00',
      seats: 2,
      price: 30,
      distance: '32km'
    },
    {
      id: 2,
      passengerName: '李同学',
      startPoint: '同济大学嘉定校区',
      endPoint: '浦东机场',
      departureTime: '2025-06-23 15:30',
      seats: 1,
      price: 45,
      distance: '45km'
    }
  ]);

  // 登录组件
  const LoginPage = () => {
    const [isLogin, setIsLogin] = useState(true);
    const [selectedUserType, setSelectedUserType] = useState('passenger');
    const [formData, setFormData] = useState({
      phone: '',
      password: '',
      confirmPassword: '',
      name: ''
    });

    const handleSubmit = () => {
      if (!isLogin && formData.password !== formData.confirmPassword) {
        setShowError('密码不匹配');
        return;
      }

      if (formData.phone.length !== 11) {
        setShowError('请输入正确的手机号');
        return;
      }

      if (formData.password.length < 6) {
        setShowError('密码至少6位');
        return;
      }

      // 模拟登录/注册
      setUser({
        name: formData.name || '用户',
        phone: formData.phone,
        type: selectedUserType
      });
      setUserType(selectedUserType);
      setCurrentPage('main');
      setShowError('');
    };

    return (
      <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white p-4 pb-safe">
        <div className="w-full pt-8">
          <div className="text-center mb-8">
            <div className="w-20 h-20 bg-blue-500 rounded-full flex items-center justify-center mx-auto mb-4">
              <Car className="w-10 h-10 text-white" />
            </div>
            <h1 className="text-2xl font-bold text-gray-800">拼车出行</h1>
            <p className="text-gray-600">便捷、安全、实惠</p>
          </div>

          <div className="bg-white rounded-2xl shadow-lg p-6">
            <div className="flex mb-6 bg-gray-100 rounded-lg p-1">
              <button
                className={`flex-1 py-2 px-4 rounded-md text-sm font-medium transition-colors ${
                  isLogin ? 'bg-white text-blue-600 shadow-sm' : 'text-gray-600'
                }`}
                onClick={() => setIsLogin(true)}
              >
                登录
              </button>
              <button
                className={`flex-1 py-2 px-4 rounded-md text-sm font-medium transition-colors ${
                  !isLogin ? 'bg-white text-blue-600 shadow-sm' : 'text-gray-600'
                }`}
                onClick={() => setIsLogin(false)}
              >
                注册
              </button>
            </div>

            {/* 用户类型选择 - 登录和注册都显示 */}
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">用户类型</label>
              <div className="flex gap-4">
                <label className="flex items-center">
                  <input
                    type="radio"
                    value="passenger"
                    checked={selectedUserType === 'passenger'}
                    onChange={(e) => setSelectedUserType(e.target.value)}
                    className="mr-2"
                  />
                  <Users className="w-4 h-4 mr-1" />
                  乘客
                </label>
                <label className="flex items-center">
                  <input
                    type="radio"
                    value="driver"
                    checked={selectedUserType === 'driver'}
                    onChange={(e) => setSelectedUserType(e.target.value)}
                    className="mr-2"
                  />
                  <Car className="w-4 h-4 mr-1" />
                  司机
                </label>
              </div>
            </div>

            <div className="space-y-4">
              {!isLogin && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">姓名</label>
                  <input
                    type="text"
                    value={formData.name}
                    onChange={(e) => setFormData({...formData, name: e.target.value})}
                    className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="请输入真实姓名"
                  />
                </div>
              )}

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">手机号</label>
                <input
                  type="tel"
                  value={formData.phone}
                  onChange={(e) => setFormData({...formData, phone: e.target.value})}
                  className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="请输入手机号"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">密码</label>
                <input
                  type="password"
                  value={formData.password}
                  onChange={(e) => setFormData({...formData, password: e.target.value})}
                  className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="请输入密码"
                />
              </div>

              {!isLogin && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">确认密码</label>
                  <input
                    type="password"
                    value={formData.confirmPassword}
                    onChange={(e) => setFormData({...formData, confirmPassword: e.target.value})}
                    className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="请再次输入密码"
                  />
                </div>
              )}

              {showError && (
                <div className="bg-red-50 border border-red-200 rounded-lg p-3 flex items-center">
                  <X className="w-4 h-4 text-red-500 mr-2" />
                  <span className="text-red-600 text-sm">{showError}</span>
                </div>
              )}

              <button
                onClick={handleSubmit}
                className="w-full bg-blue-500 text-white py-4 rounded-lg font-medium hover:bg-blue-600 transition-colors text-lg"
              >
                {isLogin ? '登录' : '注册'}
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  };

  // 乘客首页
  const PassengerHome = () => {
    return (
      <div className="pb-20">
        <div className="bg-blue-500 text-white p-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-lg font-medium">你好，{user.name}</h1>
              <p className="text-blue-100 text-sm flex items-center">
                <Users className="w-4 h-4 mr-1" />
                乘客
              </p>
            </div>
            <User className="w-8 h-8" />
          </div>
        </div>

        {/* 快捷功能区 */}
        <div className="p-4 bg-white">
          <div className="grid grid-cols-4 gap-4">
            <div className="text-center">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mx-auto mb-2">
                <Clock className="w-6 h-6 text-blue-600" />
              </div>
              <span className="text-xs text-gray-600">定时拼车</span>
            </div>
            <div className="text-center">
              <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mx-auto mb-2">
                <MapPin className="w-6 h-6 text-green-600" />
              </div>
              <span className="text-xs text-gray-600">常用路线</span>
            </div>
            <div className="text-center">
              <div className="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center mx-auto mb-2">
                <Star className="w-6 h-6 text-orange-600" />
              </div>
              <span className="text-xs text-gray-600">收藏地点</span>
            </div>
            <div className="text-center">
              <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mx-auto mb-2">
                <CreditCard className="w-6 h-6 text-purple-600" />
              </div>
              <span className="text-xs text-gray-600">我的钱包</span>
            </div>
          </div>
        </div>

        {/* 优惠活动 */}
        <div className="p-4">
          <div className="bg-gradient-to-r from-orange-400 to-pink-400 rounded-lg p-4 text-white">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="font-bold text-lg">新用户专享</h3>
                <p className="text-sm opacity-90">首次拼车立减10元</p>
              </div>
              <div className="bg-white bg-opacity-20 px-3 py-1 rounded-full">
                <span className="text-sm font-medium">立即使用</span>
              </div>
            </div>
          </div>
        </div>

        {/* 环保数据 */}
        <div className="px-4 pb-4">
          <div className="bg-green-50 rounded-lg p-4 border border-green-200">
            <div className="flex items-center mb-3">
              <div className="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center mr-3">
                <span className="text-white text-xs">🌱</span>
              </div>
              <div>
                <h3 className="font-medium text-green-800">环保出行</h3>
                <p className="text-xs text-green-600">与他人拼车，减少碳排放</p>
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4 text-center">
              <div>
                <div className="text-lg font-bold text-green-700">15.6kg</div>
                <div className="text-xs text-green-600">本月减排CO₂</div>
              </div>
              <div>
                <div className="text-lg font-bold text-green-700">¥286</div>
                <div className="text-xs text-green-600">本月节省费用</div>
              </div>
            </div>
          </div>
        </div>

        {/* 发布拼车请求按钮 */}
        <div className="p-4">
          <button
            onClick={() => setCurrentPage('publishRequest')}
            className="w-full bg-green-500 text-white py-4 rounded-lg font-medium flex items-center justify-center text-lg shadow-lg"
          >
            <Plus className="w-5 h-5 mr-2" />
            发布拼车请求
          </button>
        </div>

        {/* 附近拼车标题 */}
        <div className="px-4 pb-2">
          <h2 className="text-lg font-medium text-gray-800">附近拼车</h2>
        </div>

        {/* 可用行程 */}
        <div className="p-4">
          <div className="space-y-4">
            {trips.filter(trip => trip.status !== 'completed').map((trip, index) => (
              <div key={index} className="bg-white rounded-lg border border-gray-200 p-4">
                <div className="flex justify-between items-start mb-3">
                  <div className="flex-1">
                    <div className="flex items-center text-sm text-gray-600 mb-1">
                      <div className="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
                      {trip.startPoint}
                    </div>
                    <div className="flex items-center text-sm text-gray-600">
                      <div className="w-2 h-2 bg-red-500 rounded-full mr-2"></div>
                      {trip.endPoint}
                    </div>
                  </div>
                  <span className="text-lg font-bold text-blue-600">¥{trip.price}</span>
                </div>

                <div className="grid grid-cols-2 gap-4 text-sm text-gray-600 mb-3">
                  <div className="flex items-center">
                    <Clock className="w-4 h-4 mr-1" />
                    {trip.departureTime.split(' ')[1]}
                  </div>
                  <div className="flex items-center">
                    <Users className="w-4 h-4 mr-1" />
                    {trip.availableSeats}座
                  </div>
                </div>

                <div className="flex items-center justify-between text-sm">
                  <div className="flex items-center text-gray-600">
                    <Car className="w-4 h-4 mr-1" />
                    {trip.carModel} · {trip.plateNumber}
                  </div>
                  <button className="bg-blue-500 text-white px-4 py-2 rounded-full text-sm min-h-8">
                    立即预订
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* 附近更多行程 */}
        <div className="p-4">
          <div className="space-y-4">
            <div className="bg-white rounded-lg border border-gray-200 p-4">
              <div className="flex justify-between items-start mb-3">
                <div className="flex-1">
                  <div className="flex items-center text-sm text-gray-600 mb-1">
                    <div className="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
                    嘉定北站
                  </div>
                  <div className="flex items-center text-sm text-gray-600">
                    <div className="w-2 h-2 bg-red-500 rounded-full mr-2"></div>
                    人民广场
                  </div>
                </div>
                <span className="text-lg font-bold text-blue-600">¥28</span>
              </div>

              <div className="grid grid-cols-2 gap-4 text-sm text-gray-600 mb-3">
                <div className="flex items-center">
                  <Clock className="w-4 h-4 mr-1" />
                  15:30 出发
                </div>
                <div className="flex items-center">
                  <Users className="w-4 h-4 mr-1" />
                  还剩2座
                </div>
              </div>

              <div className="flex items-center justify-between text-sm">
                <div className="flex items-center text-gray-600">
                  <Car className="w-4 h-4 mr-1" />
                  丰田凯美瑞 · 沪C88888
                </div>
                <button className="bg-blue-500 text-white px-4 py-1 rounded-full text-xs">
                  立即预订
                </button>
              </div>
            </div>

            <div className="bg-white rounded-lg border border-gray-200 p-4">
              <div className="flex justify-between items-start mb-3">
                <div className="flex-1">
                  <div className="flex items-center text-sm text-gray-600 mb-1">
                    <div className="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
                    同济大学嘉定校区
                  </div>
                  <div className="flex items-center text-sm text-gray-600">
                    <div className="w-2 h-2 bg-red-500 rounded-full mr-2"></div>
                    静安寺
                  </div>
                </div>
                <span className="text-lg font-bold text-blue-600">¥32</span>
              </div>

              <div className="grid grid-cols-2 gap-4 text-sm text-gray-600 mb-3">
                <div className="flex items-center">
                  <Clock className="w-4 h-4 mr-1" />
                  16:00 出发
                </div>
                <div className="flex items-center">
                  <Users className="w-4 h-4 mr-1" />
                  还剩1座
                </div>
              </div>

              <div className="flex items-center justify-between text-sm">
                <div className="flex items-center text-gray-600">
                  <Car className="w-4 h-4 mr-1" />
                  别克君威 · 沪A66666
                </div>
                <button className="bg-blue-500 text-white px-4 py-1 rounded-full text-xs">
                  立即预订
                </button>
              </div>
            </div>

            <div className="bg-white rounded-lg border border-gray-200 p-4">
              <div className="flex justify-between items-start mb-3">
                <div className="flex-1">
                  <div className="flex items-center text-sm text-gray-600 mb-1">
                    <div className="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
                    安亭地铁站
                  </div>
                  <div className="flex items-center text-sm text-gray-600">
                    <div className="w-2 h-2 bg-red-500 rounded-full mr-2"></div>
                    徐家汇
                  </div>
                </div>
                <span className="text-lg font-bold text-blue-600">¥35</span>
              </div>

              <div className="grid grid-cols-2 gap-4 text-sm text-gray-600 mb-3">
                <div className="flex items-center">
                  <Clock className="w-4 h-4 mr-1" />
                  17:15 出发
                </div>
                <div className="flex items-center">
                  <Users className="w-4 h-4 mr-1" />
                  还剩3座
                </div>
              </div>

              <div className="flex items-center justify-between text-sm">
                <div className="flex items-center text-gray-600">
                  <Car className="w-4 h-4 mr-1" />
                  奥迪A4L · 沪B99999
                </div>
                <button className="bg-blue-500 text-white px-4 py-1 rounded-full text-xs">
                  立即预订
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  };

  // 发布拼车请求页面
  const PublishRequestPage = () => {
    const [requestData, setRequestData] = useState({
      startPoint: '',
      endPoint: '',
      departureTime: '',
      seats: 1,
      note: ''
    });

    const handlePublish = () => {
      setCurrentPage('main');
      setActiveTab('trips');
    };

    return (
      <div className="min-h-screen bg-gray-50">
        <div className="bg-blue-500 text-white p-4 flex items-center">
          <button onClick={() => setCurrentPage('main')} className="mr-3">
            <X className="w-6 h-6" />
          </button>
          <h1 className="text-lg font-medium">发布拼车请求</h1>
        </div>

        <div className="p-4 space-y-4">
          <div className="bg-white rounded-lg p-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">起点</label>
            <input
              type="text"
              value={requestData.startPoint}
              onChange={(e) => setRequestData({...requestData, startPoint: e.target.value})}
              placeholder="请输入起点"
              className="w-full px-3 py-3 border border-gray-200 rounded-lg"
            />
          </div>

          <div className="bg-white rounded-lg p-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">终点</label>
            <input
              type="text"
              value={requestData.endPoint}
              onChange={(e) => setRequestData({...requestData, endPoint: e.target.value})}
              placeholder="请输入终点"
              className="w-full px-3 py-3 border border-gray-200 rounded-lg"
            />
          </div>

          <div className="bg-white rounded-lg p-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">期望出发时间</label>
            <input
              type="datetime-local"
              value={requestData.departureTime}
              onChange={(e) => setRequestData({...requestData, departureTime: e.target.value})}
              className="w-full px-3 py-3 border border-gray-200 rounded-lg"
            />
          </div>

          <div className="bg-white rounded-lg p-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">需要座位数</label>
            <div className="flex items-center justify-center space-x-4">
              <button
                onClick={() => setSeatCount(Math.max(1, seatCount - 1))}
                className="w-10 h-10 bg-gray-200 rounded-full flex items-center justify-center"
              >
                <Minus className="w-5 h-5" />
              </button>
              <span className="text-2xl font-bold w-8 text-center">{seatCount}</span>
              <button
                onClick={() => setSeatCount(Math.min(4, seatCount + 1))}
                className="w-10 h-10 bg-gray-200 rounded-full flex items-center justify-center"
              >
                <Plus className="w-5 h-5" />
              </button>
            </div>
          </div>

          <div className="bg-white rounded-lg p-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">备注消息</label>
            <textarea
              value={requestData.note}
              onChange={(e) => setRequestData({...requestData, note: e.target.value})}
              placeholder="请输入备注信息（可选）"
              rows="3"
              className="w-full px-3 py-3 border border-gray-200 rounded-lg"
            />
          </div>

          <button
            onClick={handlePublish}
            className="w-full bg-blue-500 text-white py-3 rounded-lg font-medium"
          >
            发布拼车请求
          </button>
        </div>
      </div>
    );
  };

  // 乘客行程页面
  const PassengerTrips = () => {
    const [activePassengerTab, setActivePassengerTab] = useState('ongoing');

    const ongoingTrips = [
      {
        id: 3,
        startPoint: '同济大学（嘉定校区）',
        endPoint: '人民广场',
        departureTime: '2025-06-23 18:30',
        status: 'ongoing',
        driver: '张师傅',
        carModel: '大众帕萨特',
        plateNumber: '沪A55555',
        seats: 2,
        price: 30
      }
    ];

    return (
      <div className="pb-20">
        <div className="bg-blue-500 text-white p-4">
          <h1 className="text-lg font-medium">我的行程</h1>
        </div>

        <div className="bg-white border-b border-gray-200">
          <div className="flex">
            <button
              className={`flex-1 py-3 px-4 text-center ${
                activePassengerTab === 'ongoing' ? 'border-b-2 border-blue-500 text-blue-600' : 'text-gray-600'
              }`}
              onClick={() => setActivePassengerTab('ongoing')}
            >
              进行中
            </button>
            <button
              className={`flex-1 py-3 px-4 text-center ${
                activePassengerTab === 'completed' ? 'border-b-2 border-blue-500 text-blue-600' : 'text-gray-600'
              }`}
              onClick={() => setActivePassengerTab('completed')}
            >
              已完成
            </button>
          </div>
        </div>

        <div className="p-4">
          {activePassengerTab === 'ongoing' ? (
            <div className="space-y-4">
              {ongoingTrips.map((trip) => (
                <div key={trip.id} className="bg-white border border-blue-200 rounded-lg p-4">
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center">
                      <div className="w-3 h-3 bg-green-500 rounded-full mr-2 animate-pulse"></div>
                      <span className="text-sm font-medium text-green-600">进行中</span>
                    </div>
                    <span className="text-xs bg-blue-100 text-blue-600 px-2 py-1 rounded-full">
                      {trip.departureTime.split(' ')[1]} 出发
                    </span>
                  </div>

                  <div className="mb-3">
                    <div className="flex items-center text-sm text-gray-600 mb-1">
                      <div className="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
                      {trip.startPoint}
                    </div>
                    <div className="flex items-center text-sm text-gray-600">
                      <div className="w-2 h-2 bg-red-500 rounded-full mr-2"></div>
                      {trip.endPoint}
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-4 text-sm text-gray-600 mb-3">
                    <div className="flex items-center">
                      <Users className="w-4 h-4 mr-1" />
                      {trip.seats}人
                    </div>
                    <div className="flex items-center">
                      <DollarSign className="w-4 h-4 mr-1" />
                      ¥{trip.price}
                    </div>
                  </div>

                  <div className="flex items-center justify-between text-sm border-t border-gray-100 pt-3">
                    <div className="flex items-center text-gray-600">
                      <Car className="w-4 h-4 mr-1" />
                      {trip.carModel} · {trip.plateNumber}
                    </div>
                    <div className="flex space-x-2">
                      <button className="bg-green-500 text-white px-3 py-1 rounded-full text-xs flex items-center">
                        <Phone className="w-3 h-3 mr-1" />
                        联系司机
                      </button>
                    </div>
                  </div>
                </div>
              ))}

              {ongoingTrips.length === 0 && (
                <div className="text-center py-8 text-gray-500">
                  <Route className="w-12 h-12 mx-auto mb-2 opacity-50" />
                  <p>暂无进行中的行程</p>
                </div>
              )}
            </div>
          ) : (
            <div className="space-y-4">
              {trips.map((trip) => (
                <div key={trip.id} className="border border-gray-100 rounded-lg p-4">
                  <div className="flex justify-between items-start mb-3">
                    <div>
                      <div className="text-sm text-gray-500 mb-1">
                        {trip.departureTime}
                      </div>
                      <div className="font-medium">{trip.startPoint}</div>
                      <div className="text-gray-600">→ {trip.endPoint}</div>
                    </div>
                    <div className="text-right">
                      <div className="text-lg font-bold">¥{trip.amount}</div>
                      <div className={`text-xs px-2 py-1 rounded-full ${
                        trip.paid ? 'bg-green-100 text-green-600' : 'bg-red-100 text-red-600'
                      }`}>
                        {trip.paid ? '已支付' : '未支付'}
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center justify-between text-sm text-gray-600">
                    <div className="flex items-center">
                      <Users className="w-4 h-4 mr-1" />
                      {trip.availableSeats}座
                    </div>
                    <div className="flex items-center">
                      <Car className="w-4 h-4 mr-1" />
                      {trip.carModel}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    );
  };

  // 司机首页
  const DriverHome = () => {
    return (
      <div className="pb-20">
        <div className="bg-blue-500 text-white p-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-lg font-medium">你好，{user.name}</h1>
              <p className="text-blue-100 text-sm flex items-center">
                <Car className="w-4 h-4 mr-1" />
                司机
              </p>
            </div>
            <User className="w-8 h-8" />
          </div>
        </div>

        <div className="p-4">
          <h2 className="text-lg font-medium mb-4">附近拼车需求</h2>
          <div className="space-y-4">
            {rideRequests.map((request) => (
              <div key={request.id} className="bg-white rounded-lg border border-gray-200 p-4">
                <div className="flex justify-between items-start mb-3">
                  <div className="flex-1">
                    <div className="font-medium text-blue-600 mb-1">{request.passengerName}</div>
                    <div className="text-sm text-gray-600 mb-1">
                      <div className="flex items-center">
                        <div className="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
                        {request.startPoint}
                      </div>
                    </div>
                    <div className="text-sm text-gray-600">
                      <div className="flex items-center">
                        <div className="w-2 h-2 bg-red-500 rounded-full mr-2"></div>
                        {request.endPoint}
                      </div>
                    </div>
                  </div>
                  <span className="text-lg font-bold text-green-600">¥{request.price}</span>
                </div>

                <div className="grid grid-cols-3 gap-4 text-sm text-gray-600 mb-3">
                  <div className="flex items-center">
                    <Clock className="w-4 h-4 mr-1" />
                    {request.departureTime.split(' ')[1]}
                  </div>
                  <div className="flex items-center">
                    <Users className="w-4 h-4 mr-1" />
                    {request.seats}人
                  </div>
                  <div className="flex items-center">
                    <Navigation className="w-4 h-4 mr-1" />
                    {request.distance}
                  </div>
                </div>

                <button className="w-full bg-green-500 text-white py-2 rounded-lg font-medium">
                  接单
                </button>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  };

  // 司机行程页面
  const DriverTrips = () => {
    const [activeDriverTab, setActiveDriverTab] = useState('current');

    return (
      <div className="pb-20">
        <div className="bg-blue-500 text-white p-4">
          <h1 className="text-lg font-medium">行程管理</h1>
        </div>

        <div className="bg-white border-b border-gray-200">
          <div className="flex">
            <button
              className={`flex-1 py-3 px-4 text-center ${
                activeDriverTab === 'current' ? 'border-b-2 border-blue-500 text-blue-600' : 'text-gray-600'
              }`}
              onClick={() => setActiveDriverTab('current')}
            >
              当前行程
            </button>
            <button
              className={`flex-1 py-3 px-4 text-center ${
                activeDriverTab === 'completed' ? 'border-b-2 border-blue-500 text-blue-600' : 'text-gray-600'
              }`}
              onClick={() => setActiveDriverTab('completed')}
            >
              已完成
            </button>
          </div>
        </div>

        <div className="p-4">
          {activeDriverTab === 'current' ? (
            <div className="space-y-4">
              <div className="bg-white border border-gray-200 rounded-lg p-4">
                <div className="flex justify-between items-start mb-3">
                  <div>
                    <div className="font-medium">虹桥火车站</div>
                    <div className="text-gray-600">→ 浦东机场</div>
                    <div className="text-sm text-gray-500 mt-1">今天 14:30 出发</div>
                  </div>
                  <div className="text-right">
                    <div className="text-lg font-bold text-green-600">¥85</div>
                    <div className="text-sm text-gray-500">3/4人</div>
                  </div>
                </div>

                <div className="border-t border-gray-100 pt-3 mt-3">
                  <div className="text-sm text-gray-600 mb-3">乘客：张同学、李同学、王同学</div>
                  <button className="w-full bg-red-500 text-white py-2 rounded-lg font-medium">
                    结束行程
                  </button>
                </div>
              </div>
            </div>
          ) : (
            <div className="space-y-4">
              {trips.map((trip) => (
                <div key={trip.id} className="bg-white border border-gray-200 rounded-lg p-4">
                  <div className="flex justify-between items-start mb-3">
                    <div>
                      <div className="font-medium">{trip.startPoint}</div>
                      <div className="text-gray-600">→ {trip.endPoint}</div>
                      <div className="text-sm text-gray-500 mt-1">{trip.departureTime}</div>
                    </div>
                    <div className="text-right">
                      <div className="text-lg font-bold text-green-600">¥{trip.price}</div>
                      <div className={`text-xs px-2 py-1 rounded-full ${
                        trip.paid ? 'bg-green-100 text-green-600' : 'bg-red-100 text-red-600'
                      }`}>
                        {trip.paid ? '已收款' : '待收款'}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    );
  };

  // 消息页面
  const MessagesPage = () => {
    const messages = [
      {
        id: 1,
        name: userType === 'passenger' ? '司机张师傅' : '乘客李同学',
        avatar: '👨',
        lastMessage: '我已经到楼下了',
        time: '10:30',
        unread: 2
      },
      {
        id: 2,
        name: userType === 'passenger' ? '司机王师傅' : '乘客张同学',
        avatar: '👨‍💼',
        lastMessage: '预计15分钟后到达',
        time: '09:45',
        unread: 0
      }
    ];

    return (
      <div className="pb-20">
        <div className="bg-blue-500 text-white p-4">
          <h1 className="text-lg font-medium">消息</h1>
        </div>

        <div className="divide-y divide-gray-200">
          {messages.map((message) => (
            <div key={message.id} className="bg-white p-4 flex items-center">
              <div className="w-12 h-12 bg-gray-200 rounded-full flex items-center justify-center text-xl mr-3">
                {message.avatar}
              </div>
              <div className="flex-1">
                <div className="flex justify-between items-start">
                  <h3 className="font-medium">{message.name}</h3>
                  <span className="text-sm text-gray-500">{message.time}</span>
                </div>
                <p className="text-gray-600 text-sm mt-1">{message.lastMessage}</p>
              </div>
              {message.unread > 0 && (
                <div className="w-5 h-5 bg-red-500 rounded-full flex items-center justify-center text-white text-xs ml-2">
                  {message.unread}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    );
  };

  // 我的页面
  const ProfilePage = () => {
    const profileItems = [
      { icon: <User className="w-5 h-5" />, label: '个人信息', action: '>' },
      { icon: <Car className="w-5 h-5" />, label: userType === 'driver' ? '车辆信息' : '常用地址', action: '>' },
      { icon: <CreditCard className="w-5 h-5" />, label: '钱包', action: '>' },
      { icon: <Shield className="w-5 h-5" />, label: '安全中心', action: '>' },
      { icon: <Settings className="w-5 h-5" />, label: '设置', action: '>' },
      { icon: <Phone className="w-5 h-5" />, label: '客服', action: '>' }
    ];

    return (
      <div className="pb-20 bg-gray-50">
        <div className="bg-blue-500 text-white p-4">
          <h1 className="text-lg font-medium">我的</h1>
        </div>

        {/* 用户信息卡片 */}
        <div className="bg-white p-4 m-4 rounded-lg shadow-sm">
          <div className="flex items-center">
            <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mr-4">
              <User className="w-8 h-8 text-blue-600" />
            </div>
            <div className="flex-1">
              <h2 className="text-lg font-medium">{user.name}</h2>
              <p className="text-gray-600 flex items-center">
                {userType === 'passenger' ? <Users className="w-4 h-4 mr-1" /> : <Car className="w-4 h-4 mr-1" />}
                {userType === 'passenger' ? '乘客' : '司机'}
              </p>
            </div>
          </div>

          {userType === 'driver' && (
            <div className="grid grid-cols-3 gap-4 mt-4 pt-4 border-t border-gray-100">
              <div className="text-center">
                <div className="text-lg font-bold text-blue-600">4.8</div>
                <div className="text-sm text-gray-600 flex items-center justify-center">
                  <Star className="w-3 h-3 mr-1" />
                  评分
                </div>
              </div>
              <div className="text-center">
                <div className="text-lg font-bold text-green-600">156</div>
                <div className="text-sm text-gray-600">完成订单</div>
              </div>
              <div className="text-center">
                <div className="text-lg font-bold text-orange-600">¥2,580</div>
                <div className="text-sm text-gray-600">本月收入</div>
              </div>
            </div>
          )}
        </div>

        {/* 功能列表 */}
        <div className="bg-white mx-4 rounded-lg shadow-sm divide-y divide-gray-100">
          {profileItems.map((item, index) => (
            <div key={index} className="flex items-center justify-between p-4">
              <div className="flex items-center">
                <div className="text-gray-600 mr-3">{item.icon}</div>
                <span className="font-medium">{item.label}</span>
              </div>
              <span className="text-gray-400">{item.action}</span>
            </div>
          ))}
        </div>

        {/* 退出登录 */}
        <div className="mx-4 mt-4">
          <button
            onClick={() => {
              setUser(null);
              setCurrentPage('login');
            }}
            className="w-full bg-red-500 text-white py-3 rounded-lg font-medium"
          >
            退出登录
          </button>
        </div>
      </div>
    );
  };

  // 底部导航
  const BottomNavigation = () => {
    const navItems = [
      { id: 'home', icon: Home, label: '首页' },
      { id: 'trips', icon: Route, label: '行程' },
      { id: 'messages', icon: MessageCircle, label: '消息' },
      { id: 'profile', icon: User, label: '我的' }
    ];

    return (
      <div className="absolute bottom-0 left-0 right-0 bg-white border-t border-gray-200 pb-safe">
        <div className="flex">
          {navItems.map((item) => {
            const IconComponent = item.icon;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`flex-1 py-3 px-1 flex flex-col items-center min-h-16 ${
                  activeTab === item.id ? 'text-blue-600' : 'text-gray-600'
                }`}
              >
                <IconComponent className="w-6 h-6 mb-1" />
                <span className="text-xs">{item.label}</span>
              </button>
            );
          })}
        </div>
      </div>
    );
  };

  // 主应用
  const MainApp = () => {
    const renderContent = () => {
      switch (activeTab) {
        case 'home':
          return userType === 'passenger' ? <PassengerHome /> : <DriverHome />;
        case 'trips':
          return userType === 'passenger' ? <PassengerTrips /> : <DriverTrips />;
        case 'messages':
          return <MessagesPage />;
        case 'profile':
          return <ProfilePage />;
        default:
          return userType === 'passenger' ? <PassengerHome /> : <DriverHome />;
      }
    };

    return (
      <div className="min-h-screen bg-gray-50 relative">
        {renderContent()}
        <BottomNavigation />
      </div>
    );
  };

  // 主渲染逻辑
  const renderApp = () => {
    if (currentPage === 'login') {
      return <LoginPage />;
    }

    if (currentPage === 'publishRequest') {
      return <PublishRequestPage />;
    }

    return <MainApp />;
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-start justify-center py-1">
      <div className="w-full max-w-sm bg-white shadow-xl rounded-lg overflow-hidden min-h-screen relative">
        {renderApp()}
      </div>
    </div>
  );
};

export default RideShareApp;
