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
    hidden:false,
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    
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
    var that = this;
    var openid = ''
    console.log(app.globalData.openid)
    // wx.getStorage({
    //   key: 'openid',
    //   success: function (res) {
    //     console.log(res.data)
    //     openid = res.data
    //   },
    //   fail: function(){
    //     console.log('Storage fail!');
    //   }
    // });

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
  
  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {
  
  },

  enter_room: function (event) {
    console.log(event);
    console.log(event.currentTarget.dataset.room_id)

    wx.navigateTo({
      url: '../room/room?room_id=' + event.currentTarget.dataset.room_id,
    });
  },

  
  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {
  
  },

  fetchData: function () {
    var that = this;
    wx.request({
      url: 'http://www.eximple.me:5000/usr/roomlist1',
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
            roomlist: res.data[1]
          });
        }
        setTimeout(function () {
          that.setData({
            hidden: true
          })
        }, 1000);
      },
      fail: function () {
        console.log('fail');
      }
    })

    wx.request({
      url: 'http://www.eximple.me:5000/usr/roomlist2',
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
            roomlist: res.data[1]
          });
        }
        setTimeout(function () {
          that.setData({
            hidden: true
          })
        }, 1000);
      },
      fail: function () {
        console.log('fail');
      }
    })
  }
})