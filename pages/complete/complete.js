var sex = '0'
var section = []
var openid = ''
var avatarurl = ''
var name = ''

const app = getApp()

wx.getStorage({
  key: 'openid',
  success: function (res) {
    //console.log(res.data)
    openid = res.data
  }
})

try{
  wx.getStorage({
    key:'usrinfo',
    success: function(res) {
      //console.log(res.data)
      avatarurl = res.data.avatarUrl
      name = res.data.nickName
    }
  })
}catch(e){}

Page({
  data: {
    canIUse: wx.canIUse('button.open-type.getUserInfo'),
    sex: [
      { name: '0', value: '女', imgurl:'../../images/female.png', checked: 'true' },
      { name: '1', value: '男', imgurl: '../../images/male.png' }
    ],
    sectionicons: [
      {
        'icon': '../../images/KoG.jpg',
        'text': '王者荣耀',
        'value': '1',
      },
      {
        'icon': '../../images/PUBG.jpg',
        'text': '吃鸡',
        'value': '2',
      },
      {
        'icon': '../../images/LOL.jpg',
        'text': '英雄联盟',
        'value': '3',
      },
      {
        'icon': '../../images/wolf.jpg',
        'text': '狼人杀',
        'value': '4',
      }
    ]
  },

  onShow: function(){
    sex = '0'
    section = []
    try {
      wx.getStorage({
        key: 'usrinfo',
        success: function (res) {
          //console.log(res.data)
          avatarurl = res.data.avatarUrl
          name = res.data.nickName
        }
      })
    } catch (e) { }
  },

  bindGetUserInfo: function (e) {
    console.log(e.detail.userInfo)
    wx.setStorage({
      key: 'usrinfo',
      data: e.detail.userInfo,
    })
    avatarurl = e.detail.userInfo.avatarUrl
  },
   
  radioChange: function (e) {
    //console.log('radio发生change事件，携带value值为：', e.detail.value)
    sex = e.detail.value
  },
  checkboxChange: function (e) {
    //console.log('checkbox发生change事件，携带value值为：', e.detail.value)
    section = e.detail.value
  },

  formSubmit: function (e) {
    //console.log(sex)
    //console.log(section)
    if (avatarurl == '') {
      wx.showToast({
        title: '请先授权',
        icon:'none',
        duration: 1000,
      })
    }
    else {
      wx.request({
        url: app.globalData.serverurl + '/usr/complete',
        data: {
          open_id: openid,
          sex: sex,
          preference: section,
          avatar: avatarurl,
          name: name
        },
        method: 'POST',
        header: {
          'content-type': 'application/json' // 默认值
        },
        success: function (res) {
          console.log(res.data)
          if (res.data.response_code == 1) {
            wx.showToast({
              title: '成功',
              icon: 'success',
              duration: 1500,
            });
            setTimeout(function () {
              wx.navigateBack({
                delta: 1
              })
            }, 1500);
          }
          else {
            wx.showToast({
              title: '设置失败',
              icon: 'none'
            })
          }
        }
      }
      )
    }
  },

  check:function(e) {
    console.log('check_function')
    //console.log(openid)
    wx.request({
      url: app.globalData.serverurl+'/usr/info',
      data: {
        open_id: openid,
      },
      method: 'POST',
      header: {
        'content-type': 'application/json' // 默认值
      },
      success: function (res) {
        //console.log(openid)
        console.log(res.data)
      }
    }
    )
  }
})