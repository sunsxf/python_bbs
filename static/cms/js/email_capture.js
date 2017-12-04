$(function () {
    $("#email").click(function (event) {
        event.preventDefault();
        var emailElement = $("input[name='email']");
        var email = emailElement.val();
        if (!email) {
            xalert.alertInfoToast('..請輸入郵箱..');
            return;
        }

        jQuery.get({
            'url': '/cms/email_capture/',
            'data': {'email': email},
            'success': function (data) {
                if (data['code'] == 200) {
                    xalert.alertSuccessToast('郵件發送成功，請注意查收');
                } else {
                    xalert.alertInfo(data['message']);
                }
            },
            'fail': function (error) {
                xalert.alertNetworkError();
            }
        })
    });
});