// pages/roomcomplete/roomcomplete.js
var app=getApp();

Page({

  /**
   * 页面的初始数据
   */
  data: {
    room_id: -1,
    open_id: '',
    name:'',
    room_number:-1,
    section_array: ['选择分区', '王者荣耀', '吃鸡', '英雄联盟', '狼人杀', '其他'],
    section_index: 0,
    description:''
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    console.log(options.room_id);
    this.setData({
      room_id: options.room_id,
      open_id: app.globalData.openid,
    })
    this.fetchData();
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
  fetchData: function () {
    var that = this;
    wx.request({
      url: app.globalData.serverurl + '/search',
      data: {
        room_id: parseInt(that.data.room_id)
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
          //console.log(in_room);
          that.setData({
            room_id: res.data[1].room_id,
            name: res.data[1].name,
            section_index: res.data[1].area,
            description: res.data[1].description,
            room_number: res.data[1].users.length
          });
        }
        console.log('success')
      },
      fail: function () {
        console.log('fail');
      }
    });
  },
  bindPickerChange: function (e) {
    this.setData({
      section_index: e.detail.value
    })
  },
  formSubmit: function (e) {
    if (e.detail.value["name"] != ''){
      this.setData({
        name: e.detail.value["name"]
      })
    }
    if (e.detail.value["section"] != '') {
      this.setData({
        section_index: e.detail.value["section"]
      })
    }
    if (e.detail.value["room_number"] != '') {
      this.setData({
        room_number: e.detail.value["room_number"]
      })
    }
    if (e.detail.value["description"] != '') {
      this.setData({
        description: e.detail.value["description"]
      })
    }
    wx.request({
      url: app.globalData.serverurl + '/room/complete', 

      data: {
        room_id: this.data.room_id,
        name: this.data.name,
        section: this.data.section_index,
        room_number: this.data.room_number,
        description: this.data.description,
        room_owner_id: this.data.open_id
      },
      method: 'POST',
      header: {
        'content-type': 'application/json' // 默认值
      },
      success: function (res) {
        wx.showToast({
          title: '修改成功',
          icon: 'success',
          duration: 2000
        })
        console.log(res.data)
        wx.navigateBack({
          
        })
        
      },
      fail: function () {
        wx.showToast({
          title: 'error',
          icon: 'none',
          duration: 2000
        })
      }
    })
  }
})