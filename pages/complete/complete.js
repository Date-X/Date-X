var sex = '0'
var section = []
var openid = ''

wx.getStorage({
  key: 'openid',
  success: function (res) {
    console.log(res.data)
    openid = res.data
  }
})

Page({
  data: {
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
    wx.request({
      url: 'http://www.eximple.me:5000/usr/complete',
      data: {
        open_id: null,
        sex : sex,
        preference: section,
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
            icon:'success',
            duration: 2000,
          });
          setTimeout(wx.navigateBack({
            delta: 1
          }), 3000)
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