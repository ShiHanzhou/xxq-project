package com.example.monitoring;


import android.content.Intent;
import android.os.Bundle;
import android.os.Looper;
import android.text.TextUtils;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.RelativeLayout;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
/**
 * Created by littlecurl 2018/6/24
 */

/**
 * 此类 implements View.OnClickListener 之后，
 * 就可以把onClick事件写到onCreate()方法之外
 * 这样，onCreate()方法中的代码就不会显得很冗余
 */
public class LoginActivity extends AppCompatActivity implements View.OnClickListener {
    /**
     * 声明自己写的 DBOpenHelper 对象
     * DBOpenHelper(extends SQLiteOpenHelper) 主要用来
     * 创建数据表
     * 然后再进行数据表的增、删、改、查操作
     */

    private TextView mTvLoginactivityRegister;
    private RelativeLayout mRlLoginactivityTop;
    private EditText mEtLoginactivityUsername;
    private EditText mEtLoginactivityPassword;
    private LinearLayout mLlLoginactivityTwo;
    private Button mBtLoginactivityLogin;
    private Connection connection;
    /**
     * 创建 Activity 时先来重写 onCreate() 方法
     * 保存实例状态
     * super.onCreate(savedInstanceState);
     * 设置视图内容的配置文件
     * setContentView(R.layout.activity_login);
     * 上面这行代码真正实现了把视图层 View 也就是 layout 的内容放到 Activity 中进行显示
     * 初始化视图中的控件对象 initView()
     * 实例化 DBOpenHelper，待会进行登录验证的时候要用来进行数据查询
     * mDBOpenHelper = new DBOpenHelper(this);
     */
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        initView();


    }

    /**
     * onCreae()中大的布局已经摆放好了，接下来就该把layout里的东西
     * 声明、实例化对象然后有行为的赋予其行为
     * 这样就可以把视图层View也就是layout 与 控制层 Java 结合起来了
     */
    private void initView() {
        // 初始化控件
        mBtLoginactivityLogin = findViewById(R.id.bt_loginactivity_login);
        mTvLoginactivityRegister = findViewById(R.id.tv_loginactivity_register);
        mRlLoginactivityTop = findViewById(R.id.rl_loginactivity_top);
        mEtLoginactivityUsername = findViewById(R.id.et_loginactivity_username);
        mEtLoginactivityPassword = findViewById(R.id.et_loginactivity_password);
        mLlLoginactivityTwo = findViewById(R.id.ll_loginactivity_two);

        // 设置点击事件监听器
        mBtLoginactivityLogin.setOnClickListener(this);
        mTvLoginactivityRegister.setOnClickListener(this);

    }

    public void onClick(View view) {
        switch (view.getId()) {
            // 跳转到注册界面
            case R.id.tv_loginactivity_register:
                startActivity(new Intent(this, RegisterActivity.class));
                finish();
                break;
            /**
             * 登录验证：
             *
             * 从EditText的对象上获取文本编辑框输入的数据，并把左右两边的空格去掉
             *  String name = mEtLoginactivityUsername.getText().toString().trim();
             *  String password = mEtLoginactivityPassword.getText().toString().trim();
             *  进行匹配验证,先判断一下用户名密码是否为空，
             *  if (!TextUtils.isEmpty(name) && !TextUtils.isEmpty(password))
             *  再进而for循环判断是否与数据库中的数据相匹配
             *  if (name.equals(user.getName()) && password.equals(user.getPassword()))
             *  一旦匹配，立即将match = true；break；
             *  否则 一直匹配到结束 match = false；
             *
             *  登录成功之后，进行页面跳转：
             *
             *  Intent intent = new Intent(this, MainActivity.class);
             *  startActivity(intent);
             *  finish();//销毁此Activity
             */
            case R.id.bt_loginactivity_login:

                new Thread(new Runnable() {
                    @Override
                    public void run() {
                        String name1 = mEtLoginactivityUsername.getText().toString().trim();
                        String password = mEtLoginactivityPassword.getText().toString().trim();
                        try {
                            Class.forName("com.mysql.jdbc.Driver");
                            System.out.println("驱动加载成功！！！");
                            String url = "jdbc:mysql://rm-bp12m3039u29b56w32o.mysql.rds.aliyuncs.com:3306/shi_pin_xxq?useSSL=false&serverTimezone=UTC&allowPublicKeyRetrieval=true";
                            //连接数据库使用的用户名
                            String name = "root";
                            String passwd = "POiu0987";

                            try {
                                connection = DriverManager.getConnection(url, name, passwd);
                                System.out.println("连接数据库成功！！！");

                            } catch (SQLException e) {
                                System.out.println("连接数据库shibai！！！");
                            }

                            String sql = "SELECT * FROM user";
                            //获取输入框的数据
                            // 创建用来执行sql语句的对象
                            java.sql.Statement statement = connection.createStatement();
                            // 执行sql查询语句并获取查询信息
                            ResultSet rs = statement.executeQuery(sql);
                            if (name1.equals("") || password.equals("")) {
                                Looper.prepare();
                                Toast.makeText(LoginActivity.this, "账号或密码不能为空", Toast.LENGTH_SHORT).show();
                                Looper.loop();
                            }
                            String user[] = new String[100];
                            String checkpasswd[] = new String[100];
                            int i = 0, j = 0;
                            while (rs.next()) {//循环数据库数据，每条数据都保存到数组user里面
                                String UserName = rs.getString("username");
                                String UserPasswd = rs.getString("password")
                                        .replace((char) 12288, ' ').trim();
                                user[i++] = UserName;
                                checkpasswd[j++] = UserPasswd;
                            }
                            int userlength = user.length - 1;
                            Log.e("数组长度: ", String.valueOf(userlength));
                            for (i = 0, j = 0; i < user.length; i++, j++) {
                                //输入的数据和数组挨个比对，一条输入的数据和数组全部数据进行比对，判断是否注册
                                if (!name1.equals(user[i])) {
                                    if (name1.equals("")) {
                                        Looper.prepare();
                                        Toast.makeText(getApplicationContext(), "账号不能为空", Toast.LENGTH_SHORT).show();
                                        Looper.loop();
                                    } else if (password.equals("")) {
                                        Looper.prepare();
                                        Toast.makeText(getApplicationContext(), "密码不能为空", Toast.LENGTH_SHORT).show();
                                        Looper.loop();
                                    } else if (i == userlength) {
                                        Looper.prepare();
                                        Toast.makeText(getApplicationContext(), "账号不存在", Toast.LENGTH_SHORT).show();
                                        Looper.loop();
                                    }
                                    continue;
                                } else if (name1.equals(user[i])) {
                                    if (!password.equals(checkpasswd[j])) {
                                        Looper.prepare();
                                        Toast.makeText(getApplicationContext(), "密码不正确，请重试", Toast.LENGTH_SHORT).show();
                                        Looper.loop();
                                    }

                                }
                                Intent intent = new Intent(LoginActivity.this, ImagelayoutActivity.class);
                                startActivity(intent);
                                Looper.prepare();
                                Toast.makeText(LoginActivity.this, "登录成功", Toast.LENGTH_SHORT).show();
                                Looper.loop();
                            }
                        } catch (ClassNotFoundException e) {
                            e.printStackTrace();
                        } catch (SQLException e) {
                            e.printStackTrace();
                        }
                    }
                }).start();

        }
    }
}


