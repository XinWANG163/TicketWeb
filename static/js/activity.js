function create() {
    var pop = document.querySelector('.popWindow');
    pop.style.display = 'block'

    var list = document.querySelector('.activitesList');
    list.style.display = 'none'

    $('#endTime').blur(function() {
        var bgtime = document.querySelector('input[type="datetime-local"][id="bgTime"]').value
        var endtime = document.querySelector('input[type="datetime-local"][id="endTime"]').value
        var end = new Date(Date.parse(endtime))
        var bg = new Date(Date.parse(bgtime))
        var now = new Date()
        if (end < bg) {
            alert("Endtime should after Begintime")
        }
        if (end < now) {
            alert("Endtime should after Today")
        }
    })

    $('#bgTime').blur(function() {
        var bgtime = document.querySelector('input[type="datetime-local"][id="bgTime"]').value
        var endtime = document.querySelector('input[type="datetime-local"][id="endTime"]').value
        var end = new Date(Date.parse(endtime))
        var bg = new Date(Date.parse(bgtime))
        var now = new Date()
        if (end < bg) {
            alert("Endtime should after Begintime")
        }
        if (end < now) {
            alert("Endtime should after Today")
        }
    })
}

function Toast(msg, duration) {
    duration = isNaN(duration) ? 3000 : duration;
    var m = document.createElement('div');
    m.innerHTML = msg;
    m.style.cssText = "max-width:60%;min-width: 150px;padding:0 14px;height: 40px;color: rgb(255, 255, 255);line-height: 40px;text-align: center;border-radius: 4px;position: fixed;top: 50%;left: 50%;transform: translate(-50%, -50%);z-index: 999999;background: rgba(0, 0, 0,.7);font-size: 16px;";
    document.body.appendChild(m);
    setTimeout(function() {
        var d = 0.5;
        m.style.webkitTransition = '-webkit-transform ' + d + 's ease-in, opacity ' + d + 's ease-in';
        m.style.opacity = '0';
        setTimeout(function() { document.body.removeChild(m) }, d * 1000);
    }, duration);
}

function newActivity() {
    var title = actiInfo.title.value
    var status = $('#status option:selected').val()
    var bgtime = document.querySelector('input[type="datetime-local"][id="bgTime"]').value
    var endtime = document.querySelector('input[type="datetime-local"][id="endTime"]').value
    var des = document.querySelector('#description').value
    var number = actiInfo.number.value
    var data = {
            data: JSON.stringify({
                'title': title,
                'number': number,
                'status': status,
                'bgtime': bgtime,
                'endtime': endtime,
                'des': des
            })
        }
        // 将前端新活动数据发送到后端
    $.ajax({
        type: "POST",
        dataType: "json",
        url: "/activity", //后端请求
        data: data,
        success: function(result) {
            console.log(result)
        },
        error: function(result) {
            console.log(result)
        }
    })

    window.location.reload();
    // 关闭pop窗口
    var pop = document.querySelector('.popWindow');
    pop.style.display = 'none'
    var list = document.querySelector('.activitesList');
    list.style.display = 'block'
        // 成功创建提示
    Toast("New Activity '" + title + "' created!", 5000)
}

function buyTicket() {
    $.ajax({
        url: '/buyTicket',
        type: 'POST',
        dataType: "json",
        data: {},
        success: function(result) {
            Toast("Your Ticket Number is '" + result['code'] + "'", 8000)
        }
    })

    window.location.reload();
}

function calcel(id) {
    var data = {
        data: JSON.stringify({
            'activityId': id
        })
    }
    $.ajax({
        url: '/calcel',
        type: 'POST',
        dataType: "json",
        data: data,
        success: function(result) {
            Tconsole.log(result)
        },
        error: function(result) {
            console.log(result)
        }
    })
    window.location.reload();
    // 关闭pop窗口
    // 成功取消提示
    Toast("The Activity '" + title + "' canceled!", 8000)
}

function refund(target) {
    code = target.className
    var data = {
        data: JSON.stringify({
            'code': code
        })
    }
    $.ajax({
        url: '/refund',
        type: 'POST',
        dataType: "json",
        data: data,
        success: function(result) {
            Tconsole.log(result)
        },
        error: function(result) {
            console.log(result)
        }
    })
    window.location.reload();
    // 关闭pop窗口
    // 成功取消提示
    Toast("The ticket: '" + code + "' annuled!", 8000)
}

// function getUser() {
//     messages = ""
//     $.ajax({
//         url: '/getSession',
//         type: 'POST',
//         data: {},
//         success: function(data) {
//             user = JSON.parse(data)
//             var btn = document.querySelector('#createActivityBtn')
//             console.log(user)
//             if (user['role'] != 'organiser') {
//                 btn.style.display = "none"
//             } else {
//                 btn.style.display = "block"
//             }
//             if (user['username']) {
//                 $('.welcome').innerHTML = "Welcome," + user['username']
//             }
//         }
//     })
// }