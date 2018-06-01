// pages/add/add.js
const app = getApp()
var open_id = ''
//get openid
wx.getStorage({
  key: 'openid',
  success: function (res) {
    //console.log(res.data)
    open_id = res.data
  }
})

Page({
  /**
   * 页面的初始数据
   */
  data: {
    section_array: ['选择分区','王者荣耀', '吃鸡', '英雄联盟', '狼人杀','其他'],
    section_index: 0
  },
  bindPickerChange: function (e) {
    this.setData({
      section_index: e.detail.value
    })
  },
  formSubmit: function (e) {
    wx.request({
      url: 'http://www.eximple.me:5000/room/add', //仅为示例，并非真实的接口地址
      
      data: {
        name: e.detail.value["name"],
        section: e.detail.value["section"],
        room_number: e.detail.value["room_number"],
        description: e.detail.value["description"],
        //room_owner_id: 0
        room_owner_id: open_id
      },
      method:'POST',
      header: {
        'content-type': 'application/json' // 默认值
      },
      success: function (res) {
        wx.showToast({
          title: '创建成功',
          icon: 'success',
          duration: 2000
        })
        console.log(res.data)
        var room_url='../room/room?room_id='+res.data['room_id']
        console.log(room_url)
        wx.switchTab({
          url: '../myroom/myroom'
        })
        //跳转到房间内页面
      },
      fail: function(){
        wx.showToast({
          title: 'error',
          icon: 'none',
          duration: 2000
        })
      }
    })
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
  
  }
})