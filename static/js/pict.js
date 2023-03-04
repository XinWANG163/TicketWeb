var index = 1;

function lunbo() {
    index++;
    //判断index是否大于3
    if (index > 5) {
        index = 0;
    }
    //获取img对象
    var img = document.getElementById("lunbo_img");
    img.src = "../static/img/" + index + ".jpg";
}
//2.定义定时器
setInterval(lunbo, 2000);


// function logout() {
//     $.ajax({
//         url: '/login',
//         type: 'GET',
//         success: function(result) {
//             console.log(result)
//         },
//         error: function(result) {
//             console.log(result)
//         }

//     })
// }