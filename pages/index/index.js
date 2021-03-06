//index.js
//获取应用实例
const app = getApp()
Page({
  data: {
    indexmenu:[],
    imgUrls:[],
    roomlist:[]
  },
  onLoad: function () {
    //生命周期函数--监听页面加载
    this.setData({
      indexmenu:[
        {
          'icon':'./../../images/KoG.jpg',
          'text':'王者荣耀',
          'url': '../roomlist/roomlist?id=1'
        },
        {
          'icon': './../../images/PUBG.jpg',
          'text': '绝地求生',
          'url': '../roomlist/roomlist?id=2'
        },
        {
          'icon': './../../images/LOL.jpg',
          'text': '英雄联盟',
          'url': '../roomlist/roomlist?id=3'
        },
        {
          'icon': './../../images/wolf.jpg',
          'text': '狼人杀',
          'url': '../roomlist/roomlist?id=4'
        }
      ],
      imgUrls:[
        
        'http://img06.tooopen.com/images/20160818/tooopen_sy_175866434296.jpg',
        '../../images/banner.jpg',
        '../../images/banner2.jpg',
        '../../images/swiper_pic1.png'
      ]
    })
    this.fetchData()
  },
    changeRoute:function(url){
    wx.navigateTo({
      url: `../${url}/${url}`
    })
  },
  onReady:function(){
    //生命周期函数--监听页面初次渲染完成
    // console.log('onReady');
  },
  onShow :function(){
    //生命周期函数--监听页面显示
    // console.log('onShow');
  },
  onHide :function(){
    //生命周期函数--监听页面隐藏
    // console.log('onHide');
  },
  onUnload :function(){
    //生命周期函数--监听页面卸载
    // console.log('onUnload');
  },
  onPullDownRefresh:function(){
    //页面相关事件处理函数--监听用户下拉动作
    // console.log('onPullDownRefresh');
  },
  onReachBottom:function(){
    //页面上拉触底事件的处理函数
    // console.log('onReachBottom');
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
      url: app.globalData.serverurl + '/recommend',
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
      },
      fail: function () {
        console.log('fail');
      }
    })
  }
})