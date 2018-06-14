//获取应用实例
const app = getApp();

Page({
  data: {
    userInfo:{},
    user:{},
    open_id:'',
  },
  onLoad: function (options) {
    var that = this;
    if(options.open_id)
    {
      that.setData({
        open_id: options.open_id,
      })
    }
    else{
      that.setData({
        open_id: app.globalData.openid,
      })
    }
    that.auth();
  },

  onShow(){
    this.fetchData();
  },

  click: function() {
    wx.navigateTo({
      url: '/pages/complete/complete',
    })
  },

  fetchData: function(){
    var that = this;
    try {
      wx.getStorage({
        key: 'usrinfo',
        success: function (res) {
          console.log(res.data)
          that.setData({
            userInfo: res.data
          })
          //console.log(that.data.userInfo)
        },
        fail: function () {
          console.log('fail')
        },
      })
    } 
    catch (e) {
      console.log('exception.');
    }
    wx.request({
      url: app.globalData.serverurl+'/usr/info',
      data: {
        open_id: that.data.open_id,
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
            user: res.data[1]
          });
        }
        console.log('success')
      },
      fail: function () {
        console.log('fail');
      }
    })
  },

  auth: function(){
    var that = this;
    wx.request({
      url: app.globalData.serverurl + '/auth',
      data: {
        student_id:'1500012846',
        password: '12345678',
      },
      method: 'POST',
      dataType: 'json',
      success: function (res) {
        console.log('success')
        console.log(res.data);
      },
    })
  },
})
