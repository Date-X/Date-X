//app.js
App({
  onLaunch: function () {
    // 登录
    var that = this;
    wx.login({
      success: res => {
        // 发送 res.code 到后台换取 openId, sessionKey, unionId
        if (res.code) {
          //console.log(res.code)
          //发起网络请求
          wx.request({
            url: that.globalData.serverurl + '/login',
            data: {
              code: res.code
            },
            method: 'POST',
            header: {
              'content-type': 'application/json' // 默认值
            },
            success: res=> {
              console.log(res.data)
              wx.setStorage({
                key: 'openid',
                data: res.data.openid,
              })
              that.globalData.openid = res.data.openid
              //console.log(this.globalData.openid)
              var openid = that.globalData.openid
              //console.log(openid)
              var exist = res.data.exist
              //console.log(exist)
              if (exist != 1) {
                wx.showModal({
                  title: '提示',
                  content: '您还没有加入Date-X 是否加入？',
                  success: function (res) {
                    if (res.confirm) {
                      //console.log('用户点击确定')
                      wx.navigateTo({
                        url: '../complete/complete',
                      })
                    } else if (res.cancel) {
                      //console.log('用户点击取消')
                    }
                  },
                  cancelText: '告辞',
                  confirmText: '加入'

                })
              }
            }
          })
        } else {
          console.log('登录失败！' + res.errMsg)
        }
      }
    })
  },
  globalData: {
    userInfo: null,
    openid: "o9Qsr5De5nW3C2XK_tdoMZKsw-kc",
    serverurl: 'https://www.eximple.me'
  }
})