// pages/roomchat/roomchat.js
const app = getApp();

Page({

  /**
   * 页面的初始数据
   */
  data: {
    openid:'',
    str: '123',
    room_id: -1,
    name: '',
    section: -1,
    description: '',
    room_owner_id: -1,
    users_id: [],
    msg: [],
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    console.log(options.room_id);

    this.setData({
      room_id: options.room_id,
      openid: app.globalData.openid,
    });
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
    //this.fetchData();
  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {
  
  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {
  
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

  tap_it: function (event) {
    var that = this
    wx.request({
      url: 'http://www.eximple.me:5000/room/send_message',
      data: {
        room_id: 2,
        openid: app.globalData.openid,
        message: 'test',
      },
      dataType: 'json',
      method: 'POST',
      success: function (res) {
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

  join: function(){
    var that = this
    wx.request({
      url: 'http://www.eximple.me:5000/usr/join',
      data: {
        room_id: 2,
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

  fetchData: function () {
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
            room_owner_id: res.data[1].owner,
            users_id: res.data[1].users,
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