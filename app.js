//app.js
App({
  onLaunch: function () {
    // 展示本地存储能力
    var logs = wx.getStorageSync('logs') || []
    logs.unshift(Date.now())
    wx.setStorageSync('logs', logs)

    // 登录
    wx.login({
      success: res => {
        // 发送 res.code 到后台换取 openId, sessionKey, unionId
        if (res.code) {
          console.log(res.code)
          //发起网络请求
          wx.request({
            url: 'http://www.eximple.me:5000/login',
            data: {
              code: res.code
            },
            method: 'POST',
            header: {
              'content-type': 'application/json' // 默认值
            },
            success: function (res) {
              console.log(res.data)
              const app = getApp()
              app.globalData.openid = res.data.openid
              var openid = app.globalData.openid
              console.log(openid)
              var exist = res.data.exist
              console.log(exist)
              if (exist != 1) {
                wx.showModal({
                  title: '提示',
                  content: '您还没有加入Date-X 是否加入？',
                  success: function (res) {
                    if (res.confirm) {
                      console.log('用户点击确定')
                      wx.navigateTo({
                        url: '../complete/complete',
                      })
                    } else if (res.cancel) {
                      console.log('用户点击取消')
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
    // 获取用户信息
    wx.getSetting({
      success: res => {
        if (res.authSetting['scope.userInfo']) {
          // 已经授权，可以直接调用 getUserInfo 获取头像昵称，不会弹框
          wx.getUserInfo({
            success: res => {
              // 可以将 res 发送给后台解码出 unionId
              this.globalData.userInfo = res.userInfo

              // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
              // 所以此处加入 callback 以防止这种情况
              if (this.userInfoReadyCallback) {
                this.userInfoReadyCallback(res)
              }
            }
          })
        }
      }
    })
  },
  globalData: {
    userInfo: null,
    openid: null
  }
})