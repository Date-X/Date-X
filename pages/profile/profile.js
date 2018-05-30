//获取应用实例
const app = getApp()

Page({
  data: {
    userInfo:{}
  },
  onLoad: function () {
    var that=this
    try {
      wx.getStorage({
        key: 'usrinfo',
        success: function (res) {
          //console.log(res.data)
          that.setData({
            userInfo:res.data
          })
        }
      })
    } catch (e) { }
  },
  click: function() {
    wx.navigateTo({
      url: '/pages/complete/complete',
    })
  }
})
