// pages/rooms/rooms.js
var app = getApp();
var Util = require('../../utils/util.js');

Page({

  /**
   * 页面的初始数据
   */
  data: {
    imgUrls: [
      '../../images/roomlist.png',
      '../../images/roomlist.png',
      '../../images/roomlist.png',
      '../../images/roomlist.png',
      '../../images/roomlist.png',
      '../../images/roomlist.png',
      '../../images/roomlist.png'
    ],
    roomlist: [],
    section: -1,
    hidden:true
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    console.log(options.id)
    console.log(app.globalData.openid);
    var that = this;
    this.data.section = options.id;
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
      hidden: false,
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
      hidden:false,
    })
    this.fetchData();
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

  fetchData: function(){
    var that = this;
    wx.request({
      url: app.globalData.serverurl+'/search',
      data: {
        section: that.data.section
      },
      method: 'POST',
      dataType: 'json',
      header: {
        'Content-Type': 'application/json'
      },
      success: function (res) {
        //console.log('success')
        //console.log(res.data);
        if(res.data.response_code != 0)
        {
          that.setData({
            roomlist: res.data[1]
          });
        }
        setTimeout(function () {
          that.setData({
            hidden: true
          })
        }, 1000);
        //console.log('success')
        wx.stopPullDownRefresh();
      },
      fail: function () {
        console.log('fail');
      }
    })
  }
})