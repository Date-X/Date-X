//获取应用实例
const app = getApp();

Page({
  data: {
    open_id:'',
    userInfo:{},
    user:{},
    indexmenu: [
      {
        'icon': './../../images/KoG.jpg',
        'text': '王者荣耀',
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
  },
  onLoad: function (options) {
    var that = this;
    console.log(options.open_id);
    if(options.open_id){
      that.data.open_id = options.open_id;
    }
    else{
      that.data.open_id = app.globalData.openid;
    }
    console.log(that.data.open_id)
    that.fetchData();    
  },

  onShow: function(){
    var that = this;
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
      url: 'http://www.eximple.me:5000/usr/info',
      data: {
        open_id: that.data.open_id
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
            user:res.data[1]
          });
        }
        
      },
      fail: function () {
        console.log('fail');
      }
    })
  }
})
