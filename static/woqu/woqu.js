/**
 * Created by hjd on 17-2-9.
 */
var G_WIDTH = 90;
var G_HEIGHT = 30;
var G_LENGTH = 4;
window.code;

/*
 * get random float value amount [start, end)
 */
var randFloat = function (start, end) {
    return start + Math.random() * (end - start);
};

/*
 * get random integer value amount [start, end)
 */
var randInt = function (start, end) {
    return Math.floor(Math.random() * (end - start)) + start;
};

/*
 * get canvas object
 */
var getCanvas = function (w, h) {
    var canvas = document.createElement('canvas');
    canvas.setAttribute('width', w);
    canvas.setAttribute('height', h);

    return canvas;
};

var Captcha = function Captcha(w, h) {
    var W = w ? w : G_WIDTH;
    var H = w ? h : G_HEIGHT;

    var canvas = getCanvas(W, H);
    var ctx = canvas.getContext('2d');
    var items = 'abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPRSTUVWXYZ23456789'.split('');
    var vcode = '';

    // 背景
    ctx.fillStyle = '#f3fbfe';
    ctx.fillRect(0, 0, W, H);
    ctx.globalAlpha = .8;
    ctx.font = '15px sans-serif';
    for (var i = 0; i < 10; i++) {
        ctx.fillStyle = 'rgb(' + randInt(150, 225) + ',' + randInt(150, 225) + ',' + randInt(150, 225) + ')';
        for (var j = 0; j < 5; j++) {
            ctx.fillText(items[randInt(0, items.length)], randFloat(-10, W + 10), randFloat(-10, H + 10));
        }
    }

    // 验证码
    var textOffsetX = 2;
    var textWidth = W / G_LENGTH;
    var textMaxWidth = textWidth - textOffsetX * 2;
    var textY = H - 4 / 2;
    var color = 'rgb(' + randInt(1, 120) + ',' + randInt(1, 120) + ',' + randInt(1, 120) + ')';
    ctx.font = 'bold 30px sans-serif';
    for (var i = 0; i < G_LENGTH; i++) {
        var j = randInt(0, items.length);
        ctx.fillStyle = color;
        ctx.fillText(items[j], textOffsetX + textWidth * i, textY, textMaxWidth);
        var a = randFloat(1.0, 1.0); // 水平缩放
        var b = randFloat(-0.03, 0.03); // 水平倾斜
        var c = randFloat(-0.03, 0.03); // 垂直倾斜
        var d = randFloat(0.85, 1.0); // 垂直缩放
        var e = 0; // 水平移动
        var f = 0; // 垂直移动
        ctx.transform(a, b, c, d, e, f);
        vcode += items[j];
    }

    // 干扰线
    ctx.beginPath();
    ctx.strokeStyle = color;
    var A = randFloat(10, H / 2);
    var b = randFloat(H / 4, 3 * H / 4);
    var f = randFloat(H / 4, 3 * H / 4);
    var T = randFloat(H * 1.5, W);
    var w = 2 * Math.PI / T;
    var S = function (x) {
        return A * Math.sin(w * x + f) + b;
    };
    ctx.lineWidth = 3;
    for (var x = -20; x < 200; x += 4) {
        ctx.moveTo(x, S(x));
        ctx.lineTo(x + 3, S(x + 3));
    }
    ctx.closePath();
    ctx.stroke();
    // 生成的验证码
    window.code = vcode.toLowerCase();
    console.log("验证码：" + vcode.toLowerCase());
    return {
        dataURL: canvas.toDataURL()
    };
};

/**
 * 设置验证码
 * @constructor
 */

function Set_Code() {
    document.getElementById("form__captcha").src = window.Captcha().dataURL;
}

function AddClassName(id, class_name) {
    var old_name = document.getElementById(id).className;
    var new_name;
    var index = old_name.indexOf(class_name);
    if (index > 0) {
        new_name = old_name;
    }
    else {
        new_name = old_name + " " + class_name;
    }
    document.getElementById(id).className = new_name;
}
function DelClassName(id, class_name) {
    var old_name = document.getElementById(id).className;
    var new_name;
    var index = old_name.indexOf(class_name);
    if (index > 0) {
        var length = class_name.length;
        var before = old_name.slice(0, index);
        var after = old_name.slice(index + length);
        new_name = before + after;
    }
    else {
        new_name = old_name;
    }
    document.getElementById(id).className = new_name;
}

function Show_Error(id, msg) {
    AddClassName("message", "show");
    /**
     不需要参数， 5 秒后循环删除
     window.setInterval(DelClassName("message", "show"), 5000);
     * */
    /**
     需要参数
     window.setInterval(function(){
                DelClassName("message", "show");
            }, 5000);
     **/
    // 5 秒后删除一次
    window.setTimeout(function () {
        DelClassName("message", "show");
    }, 5000);
    AddClassName(id, "login-alert-danger");
    document.getElementById(id).innerHTML = '<i class="fa fa-info-circle"></i> ' + msg;
}

function Show_Ok(id, msg) {
    AddClassName("message", "show");
    // 5 秒后删除一次
    window.setTimeout(function () {
        DelClassName("message", "show");
    }, 5000);
    DelClassName(id, "login-alert-danger");
    document.getElementById(id).innerHTML = '<i class="fa fa-info-circle"></i> ' + msg;
}

function Check_Code() {
    var input_code = document.getElementById("form__code").value;
    if (input_code.toLowerCase() == window.code) {
        Show_Ok("code_message", "验证码正确");
        return true;
    }
    else {
        Show_Error("code_message", "验证码错误");
        return false;
    }
}