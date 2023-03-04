// 获取radio里面的选择
$(document).ready(function() {
    $('input[type=radio][name=role]').change(function() {
        var token = document.getElementById("token").value
        var checked = document.getElementsByName("role");
        if (token != "Dc5_G1gz" && checked[0].checked) {
            alert("Code incorrect!Register for attendee!")
            checked[1].checked = true
            checked[0].checked = false
            document.getElementById("token").required = false
        }
    });
    $('input[type=text][name=email]').blur(function() {
        var x = this.value;
        var atpos = x.indexOf("@");
        var dotpos = x.lastIndexOf(".");
        if (atpos < 1 || dotpos < atpos + 2 || dotpos + 2 >= x.length) {
            alert("It's not a valid e-mail.");
        }

    });

    // 如果选择的是组织者角色，那边必须填写code
    $(':radio').click(function() {
        var checkValue = $(this).val();
        if (checkValue == "organiser") {
            document.getElementById("token").required = true
        } else {
            document.getElementById("token").required = false
        }
    });

    $('input[type=text][name=token]').blur(function() {
        var x = this.value;
        var checked = document.getElementsByName("role");
        if (x != "Dc5_G1gz" && checked[0].checked) {
            alert("Code incorrect!Register for attendee!")
            checked[1].checked = true
            checked[0].checked = false
            document.getElementById("token").required = false
        }
    });

});

$.ajax({
    url: '/register',
    type: 'POST',
    dataType: "json",
    succrss: function(data) {
        console.log(data)
    }
})