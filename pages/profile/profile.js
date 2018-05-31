//获取应用实例
const app = getApp()

Page({
  data: {
    userInfo:{},
    user:{},
    open_id:'',
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
        },
        fail: function(){
          console.log('fail')
        },
      })
    } catch (e) {
      console.log('exception.');
     }
  },
  click: function() {
    wx.navigateTo({
      url: '/pages/complete/complete',
    })
  },

  fetchData: function(){
    var that = this;
    
  },
})
