var sex = '0'
var section = []
var openid = ''
var avatarurl = ''

wx.getStorage({
  key: 'openid',
  success: function (res) {
    console.log(res.data)
    openid = res.data
  }
})

Page({
  data: {
    canIUse: wx.canIUse('button.open-type.getUserInfo'),
    sex: [
      { name: '0', value: '女', checked: 'true' },
      { name: '1', value: '男' }
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

  onLoad: function () {
    // 查看是否授权
    wx.getSetting({
      success: function (res) {
        if (res.authSetting['scope.userInfo']) {
          // 已经授权，可以直接调用 getUserInfo 获取头像昵称
          wx.getUserInfo({
            success: function (res) {
              console(res.userInfo)
              avatarurl = res.userInfo.avatarUrl
            }
          })
        }
      }
    })
  },
  bindGetUserInfo: function (e) {
    console.log(e.detail.userInfo)
    avatarurl = e.detail.userInfo.avatarUrl
  },
   
  radioChange: function (e) {
    console.log('radio发生change事件，携带value值为：', e.detail.value)
    sex = e.detail.value
  },
  checkboxChange: function (e) {
    console.log('checkbox发生change事件，携带value值为：', e.detail.value)
    section = e.detail.value
  },

  formSubmit: function (e) {
    console.log(sex)
    console.log(section)
    if (avatarurl == '') {
      wx.showToast({
        title: '请先授权',
        icon:'none',
        duration: 1000,
      })
    }
    else {
      wx.request({
        url: 'http://www.eximple.me:5000/usr/complete',
        data: {
          open_id: openid,
          sex: sex,
          preference: section,
          avatar: avatarurl,
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
    console.log(openid)
    wx.request({
      url: 'http://www.eximple.me:5000/usr/info',
      data: {
        open_id: openid,
      },
      method: 'POST',
      header: {
        'content-type': 'application/json' // 默认值
      },
      success: function (res) {
        console.log(openid)
        console.log(res.data)
      }
    }
    )
  }
})