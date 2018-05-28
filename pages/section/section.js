
Page({

  /**
   * 页面的初始数据
   */
  data: {
    sectionmenu:[],
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    this.fetchData();
  },
  fetchData: function () {
    this.setData({
      sectionmenu: [
        {
          'icon': '../images/王者荣耀.jpg',
          'text': '王者荣耀',
          'url': '../roomlist/roomlist?id=1'
        },
        {
          'icon': '../images/吃鸡.jpg',
          'text': '吃鸡',
          'url': '../roomlist/roomlist?id=2'
        },
        {
          'icon': '../images/英雄联盟.jpg',
          'text': '英雄联盟',
          'url': '../roomlist/roomlist?id=3'
        },
        {
          'icon': '../images/狼人杀.jpg',
          'text': '狼人杀',
          'url': '../roomlist/roomlist?id=4'
        }
      ]
    })
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