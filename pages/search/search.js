// pages/search/search.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    showsearch: false,   //显示搜索按钮
    roomlist: [],
    searchtext: '',
    hidden:true,
  },

  inputSearch: function (e) {  //输入搜索文字
    this.setData({
      showsearch: e.detail.cursor > 0,
      searchtext: e.detail.value
    })
  },

  submitSearch: function(){
    this.fetchData();
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
  
  },

  fetchData: function(){
    var that = this;
    console.log(that.data.searchtext);
    that.setData({
      hidden:false
    });
    wx.request({
      url: 'http://www.eximple.me:5000/search',
      data: {
        description: that.data.searchtext
      },
      method: 'POST',
      dataType: 'json',
      header: {
        'Content-Type': 'application/json'
      },
      success: function (res) {
        console.log('success')
        console.log(res.data);
        if(res.data.response_code != 0)
        {
          that.setData({
            roomlist: res.data[1],
            hidden:true,
          });
        }
        console.log('success')
      },
      fail: function () {
        console.log('fail');
      }
    });
  },

  enter_room: function (event) {
    console.log(event);
    console.log(event.currentTarget.dataset.room_id)

    wx.navigateTo({
      url: '../roomchat/roomchat?room_id=' + event.currentTarget.dataset.room_id,
    });
  },
})