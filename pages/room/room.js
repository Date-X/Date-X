var timer;
const app = getApp();

Page({

  /**
   * 页面的初始数据
   */
  data: {
    str: '123',
    room_id: -1,
    name: '',
    section: -1,
    description: '',
    room_owner: {},
    users: [],
    msg:[],
    open_id:'',
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    console.log(options.room_id);
    this.setData({
      room_id:options.room_id,
      openid:app.globalData.openid,
    })
    //this.Countdown();
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {
  
  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {
    this.Countdown();
  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {
    clearTimeout(timer);
  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {
    clearTimeout(timer);
  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {
  
  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {
  
  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {
  },

  //按钮测试
  tap_it: function(event){
    var that = this
    wx.request({
      url: 'http://www.eximple.me:5000/room/send_message',
      data: {
        room_id:2,
        open_id:app.globalData.openid,
        message:'test',
      },
      dataType: 'form',
      method: 'POST',
      success: function(res){
        that.setData({
          'str': res.data
        })
      },
      fail: function(){
        that.setData({
          'str':'fail'
        })
      }
    })
  },

  //启动定时器
  f: function(){
    Countdown();
  },

  //定时刷新
  Countdown: function() {
    var that = this;
    timer = setTimeout(function () {
      console.log("----Countdown----");
      console.log(that.data.room_id);
      that.fetchData();
      that.Countdown();
    }, 1000);
  },

  //测试发送信息
  tap_it: function (event) {
    var that = this
    wx.request({
      url: 'http://www.eximple.me:5000/room/send_message',
      data: {
        room_id: parseInt(that.data.room_id),
        open_id: app.globalData.openid,
        message: 'test',
      },
      dataType: 'json',
      method: 'POST',
      success: function (res) {
        console.log("send successfully");
        console.log(res.data)
        that.setData({
          'str': res.data
        })
      },
      fail: function () {
        that.setData({
          'str': 'fail'
        })
      }
    })
  },

  clear_message: function (event) {
    var that = this
    wx.request({
      url: 'http://www.eximple.me:5000/room/clear_message',
      data: {
        room_id: parseInt(that.data.room_id),
      },
      dataType: 'json',
      method: 'POST',
      success: function (res) {
        console.log("clear successfully");
        console.log(res.data)
        that.setData({
          'str': res.data
        })
      },
      fail: function () {
        that.setData({
          'str': 'fail'
        })
      }
    })
  },

  join: function () {
    var that = this
    wx.request({
      url: 'http://www.eximple.me:5000/usr/join',
      data: {
        room_id: parseInt(that.data.room_id),
        open_id: app.globalData.openid,
      },
      dataType: 'json',
      method: 'POST',
      success: function (res) {
        console.log('join success');
        that.setData({
          'str': res.data
        })
      },
      fail: function () {
        that.setData({
          'str': 'fail'
        })
      }
    })
  },

  tap_it: function (event) {
    var that = this
    wx.request({
      url: 'http://www.eximple.me:5000/room/send_message',
      data: {
        room_id: parseInt(that.data.room_id),
        open_id: app.globalData.openid,
        message: 'test',
      },
      dataType: 'json',
      method: 'POST',
      success: function (res) {
        console.log("send successfully");
        console.log(res.data)
        that.setData({
          'str': res.data
        })
      },
      fail: function () {
        that.setData({
          'str': 'fail'
        })
      }
    })
  },

  clear_message: function (event) {
    var that = this
    wx.request({
      url: 'http://www.eximple.me:5000/room/clear_message',
      data: {
        room_id: parseInt(that.data.room_id),
      },
      dataType: 'json',
      method: 'POST',
      success: function (res) {
        console.log("clear successfully");
        console.log(res.data)
        that.setData({
          'str': res.data
        })
      },
      fail: function () {
        that.setData({
          'str': 'fail'
        })
      }
    })
  },

  delete_room: function () {
    var that = this
    wx.request({
      url: 'http://www.eximple.me:5000/usr/join',
      data: {
        room_id: parseInt(that.data.room_id),
        open_id: app.globalData.openid,
      },
      dataType: 'json',
      method: 'POST',
      success: function (res) {
        console.log('join success');
        that.setData({
          'str': res.data
        })
      },
      fail: function () {
        that.setData({
          'str': 'fail'
        })
      }
    })
  },

  kick: function (event) {
    var that = this;
    var openid = event.currentTarget.dataset.uid
    wx.request({
      url: 'http://www.eximple.me:5000/room/kick',
      data: {
        room_id: parseInt(that.data.room_id),
        open_id: openid
      },
      method: 'POST',
      dataType: 'json',
      header: {
        'Content-Type': 'application/json'
      },
      success: function (res) {
        console.log('success')
        console.log(res.data);
        if (res.data.response_code != 0) {
          console.log(res.data.response_code);
        }
        console.log('success')
      },
      fail: function () {
        console.log('fail');
      }
    });
  },

  quit: function () {
    var that = this;
    wx.request({
      url: 'http://www.eximple.me:5000/room/kick',
      data: {
        room_id: parseInt(that.data.room_id),
        open_id: app.globalData.openid,
      },
      method: 'POST',
      dataType: 'json',
      header: {
        'Content-Type': 'application/json'
      },
      success: function (res) {
        console.log('quit success')
        console.log(res.data);
        if (res.data.response_code != 0) {
          console.log(res.data.response_code);
        }
        console.log('success')
      },
      fail: function () {
        console.log('fail');
      }
    });
  },

  //获取数据
  fetchData: function(){
    var that = this;
    wx.request({
      url: 'http://www.eximple.me:5000/search',
      data: {
        room_id: parseInt(that.data.room_id)
      },
      method: 'POST',
      dataType: 'json',
      header: {
        'Content-Type': 'application/json'
      },
      success: function (res) {
        console.log('success')
        console.log(res.data);
        if (res.data.response_code != 0) {
          that.setData({
            room_id: res.data[1].room_id,
            name: res.data[1].name,
            section: res.data[1].area,
            description: res.data[1].description,
            room_owner: res.data[1].owner,
            users: res.data[1].users,
            msg: res.data[1].messages,
          });
        }
        console.log('success')
      },
      fail: function () {
        console.log('fail');
      }
    });
  },
})

