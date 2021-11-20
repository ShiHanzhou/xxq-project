
window.onload = function(){
    if (window.sessionStorage) {
        var username = window.sessionStorage.getItem("username");
        var password = window.sessionStorage.getItem("password");
        var email = window.sessionStorage.getItem("email");
        if (username != "" || username != null){
            document.getElementById("username").value = username;
        }
        if (password != "" || password != null){
            document.getElementById("password").value = password;
        }
        if (email != "" || email != null){
            document.getElementById("email").value = email;
        }
    }
 };

function check() {

    document.getElementById("form1").action="/regist";
    var user_name = form1.username.value;//获取表单form1的用户名的值
    var user_pwd = form1.password.value;//获取表单form1密码值
    // document.pay.action = "{:U('/regist')}";
//(user_name == "") || (user_name == null)
    if (user_name.length<5||user_name.length>12) {
        alert("请输入5-12位的用户名！");
        form1.user.focus();//获取焦点，即：鼠标自动定位到用户名输入框，等待用户输入用户名。
        return false;
    } else if (user_pwd.length<5||user_pwd.length>12) {//判断密码是否为空，为空就弹出提示框"请输入密码"，否则正常执行下面的代码。
        alert("请输入5-12位的密码！");
        form1.pwd.focus();//获取焦点。
        return false;
    } else {//如果用户名、密码都正常输入，则提交表单，浏览器经打开新的（主页）窗口。
        form1.submit();
        return true;
    }
}

function checkCode(){

   if (window.sessionStorage) {
        var username = document.getElementById("username").value;
        var password = document.getElementById("password").value;
        var email = document.getElementById("email").value;
        window.sessionStorage.setItem("username", username);
        window.sessionStorage.setItem("password", password);
        window.location.href="register.html";
    }
    document.getElementById("form1").action="/Code";
    document.pay.submit();
    return true;
}

function back() {
    window.location.href="form1.html";
 }
function onload(){
        //刷新后重新获取输入框中填入的值
        var username = localStorage.getItem("username");
        var password = localStorage.getItem("password");
        var email = localStorage.getItem("email");
        //将重新获取的值显示到表单元素中
        $("username").val(username);
        $("#password").val(password);
        $("#email").val(email);
}

function check2() {
    // let error_name = false;
    // let error_password = false;
    // let error_email = false;
    // var pat=
    var user_name = form2.username.value;//获取表单form1的用户名的值
    var user_pwd = form2.password.value;//获取表单form1密码值
//(user_name == "") || (user_name == null)
    if (user_name.length<5||user_name.length>12) {
        alert("请输入5-12位的用户名！");
        form2.user.focus();//获取焦点，即：鼠标自动定位到用户名输入框，等待用户输入用户名。
        return false;
    } else if (user_pwd.length<5||user_pwd.length>12) {//判断密码是否为空，为空就弹出提示框"请输入密码"，否则正常执行下面的代码。
        alert("请输入5-12位的密码！");
        form2.pwd.focus();//获取焦点。
        return false;
    } else {//如果用户名、密码都正常输入，则提交表单，浏览器经打开新的（主页）窗口。
        form2.submit();
        return true;
    }
}
