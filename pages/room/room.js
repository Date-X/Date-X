var timer;

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
    room_owner_id: -1,
    users_id: []
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    console.log(options.room_id);
    this.setData({
      room_id:options.room_id
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

  tap_it: function(event){
    var that = this
    wx.request({
      url: 'http://www.eximple.me:5000/search',
      data: {
         key: that.data.room_id
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

  f: function(){
    Countdown();
  },

  Countdown: function() {
    var that = this;
    timer = setTimeout(function () {
      console.log("----Countdown----");
      console.log(that.data.room_id);
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
          if(res.data.response_code != 0){
            that.setData({
              room_id: res.data[1].room_id,
              name: res.data[1].name,
              section: res.data[1].area,
              description: res.data[1].description,
              room_owner_id: res.data[1].owner,
              users_id: res.data[1].users,
            });
          }
          console.log('success')
        },
        fail: function () {
          console.log('fail');
        }
      });
      that.Countdown();
    }, 1000);
  },

})

