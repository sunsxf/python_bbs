$(function () {
    // 整個頁面加載完畢後才運行這個函數
    $("#submit").click(function (event) {
        // 必須在點擊事件發生後才能獲取到表單值
        event.preventDefault();
        // event.preventDefault阻止按鈕默認提交表單的事件
        var oldpwdElement = $("input[name=oldpwd]");
        var newpwdElement = $("input[name=newpwd]");
        var newpwd2Element = $("input[name=newpwd2]");

        var oldpwd = oldpwdElement.val();
        var newpwd = newpwdElement.val();
        var newpwd2 = newpwd2Element.val();

        // 要在模板的meta標籤中渲染一個csrf-token
        // 在ajax請求的頭部中設置X-CSRFtoken
        jQuery.post({
            'url': '/cms/resetpwd/',
            // 傳給表單所在的html路徑
            'data': {
                'oldpwd': oldpwd,
                'newpwd': newpwd,
                'newpwd2': newpwd2
            },
            'success': function (data) {
                if (data['code'] == 200) {
                    xalert.alertSuccessToast('修改成功');
                    oldpwdElement = oldpwdElement.val('');
                    newpwdElement = newpwdElement.val('');
                    newpwd2Element = newpwd2Element.val('');
                }else {
                    message = data['message'];
                    xalert.alertInfo(message);
                }
            },
            // 此data與上面的data不同,是服務器返回的數據
            'fail': function (error) {
                // console.log(error);
                // 服務器換回的錯誤信息
                xalert.alertNetworkError()
            }
            // 設置回調函數，成功和失敗後分別進行什麼操作
        });
    });
});