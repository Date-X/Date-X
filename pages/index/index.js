//index.js
//获取应用实例
const app = getApp()
Page({
  data: {
    indexmenu:[],
    imgUrls:[]
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
          'icon': './../../images/LOL.jpg',
          'text': '英雄联盟',
          'url': '../roomlist/roomlist?id=3'
        },
        {
          'icon': './../../images/PUBG.jpg',
          'text': '绝地求生',
          'url': '../roomlist/roomlist?id=2'
        },
        {
          'icon': './../../images/wolf.jpg',
          'text': '狼人杀',
          'url': '../roomlist/roomlist?id=4'
        }
      ],
      imgUrls:[
        '../../images/swiper_pic1.png',
        '../../images/swiper_pic1.png',
        '../../images/swiper_pic1.png',
        '../../images/swiper_pic1.png'
      ]
    })
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
  }
})