// pages/myroom/myroom.js
 const app = getApp();

Page({

  /**
   * 页面的初始数据
   */
  data: {
    //我创建的
    roomlist1:[],
    //我加入的
    roomlist2:[],
    hidden1:false,
    hidden2:false
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function () {
    console.log(app.globalData.openid);
    var that = this;
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
    this.setData({
      hidden1: false,
      hidden2: false,
    })
    this.fetchData();
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
    this.setData({
      hidden1: false,
      hidden2: false,
    })
    this.fetchData();
    wx.stopPullDownRefresh();
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

  enter_room: function (event) {
    console.log(event);
    console.log(event.currentTarget.dataset.room_id)

    wx.navigateTo({
      url: '../roomchat/roomchat?room_id=' + event.currentTarget.dataset.room_id,
    });
  },

  fetchData: function () {
    var that = this;
    wx.request({
      url: app.globalData.serverurl+'/usr/roomlist1',
      data: {
        open_id: app.globalData.openid
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
            roomlist1: res.data[1]
          });
        }
        setTimeout(function () {
          that.setData({
            hidden1: true
          })
        }, 1000);
      },
      fail: function () {
        console.log('fail');
      }
    })

    wx.request({
      url: app.globalData.serverurl+'/usr/roomlist2',
      data: {
        open_id: app.globalData.openid
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
            roomlist2: res.data[1]
          });
        }
        setTimeout(function () {
          that.setData({
            hidden2: true
          })
        }, 1000);
      },
      fail: function () {
        console.log('fail');
      }
    })
  },
})