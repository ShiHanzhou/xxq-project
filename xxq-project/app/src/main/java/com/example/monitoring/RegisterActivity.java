package com.example.monitoring;

import android.content.Intent;
import android.os.Bundle;
import android.os.Looper;
import android.text.TextUtils;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.RelativeLayout;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
/**
 * Created by littlecurl 2018/6/24
 */
/**
 * 此类 implements View.OnClickListener 之后，
 * 就可以把onClick事件写到onCreate()方法之外
 * 这样，onCreate()方法中的代码就不会显得很冗余
 */
public class RegisterActivity extends AppCompatActivity implements View.OnClickListener {

    private String realCode;

    private Button mBtRegisteractivityRegister;
    private RelativeLayout mRlRegisteractivityTop;
    private ImageView mIvRegisteractivityBack;
    private LinearLayout mLlRegisteractivityBody;
    private EditText mEtRegisteractivityUsername;
    private EditText mEtRegisteractivityPassword1;
    private EditText mEtRegisteractivityPassword2;
    private EditText mEtRegisteractivityPhonecodes;
    private ImageView mIvRegisteractivityShowcode;
    private RelativeLayout mRlRegisteractivityBottom;
    private EditText mEtRegisteractivityEmail;
    private Connection connection =null;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_register);

        initView();

        //将验证码用图片的形式显示出来
        mIvRegisteractivityShowcode.setImageBitmap(Code.getInstance().createBitmap());
        realCode = Code.getInstance().getCode().toLowerCase();
    }

    private void initView(){
        mBtRegisteractivityRegister = findViewById(R.id.bt_registeractivity_register);
        mRlRegisteractivityTop = findViewById(R.id.rl_registeractivity_top);
        mIvRegisteractivityBack = findViewById(R.id.iv_registeractivity_back);
        mLlRegisteractivityBody = findViewById(R.id.ll_registeractivity_body);
        mEtRegisteractivityUsername = findViewById(R.id.et_registeractivity_username);
        mEtRegisteractivityPassword1 = findViewById(R.id.et_registeractivity_password1);
        mEtRegisteractivityPassword2 = findViewById(R.id.et_registeractivity_password2);
        mEtRegisteractivityPhonecodes = findViewById(R.id.et_registeractivity_phoneCodes);
        mIvRegisteractivityShowcode = findViewById(R.id.iv_registeractivity_showCode);
        mRlRegisteractivityBottom = findViewById(R.id.rl_registeractivity_bottom);
        mEtRegisteractivityEmail = findViewById(R.id.et_registeractivity_email);

        /**
         * 注册页面能点击的就三个地方
         * top处返回箭头、刷新验证码图片、注册按钮
         */
        mIvRegisteractivityBack.setOnClickListener(this);
        mIvRegisteractivityShowcode.setOnClickListener(this);
        mBtRegisteractivityRegister.setOnClickListener(this);
    }

    public void onClick(View view) {

        switch (view.getId()) {
            case R.id.iv_registeractivity_back: //返回登录页面
                Intent intent1 = new Intent(this, LoginActivity.class);
                startActivity(intent1);
                finish();
                break;
            case R.id.iv_registeractivity_showCode:    //改变随机验证码的生成
                mIvRegisteractivityShowcode.setImageBitmap(Code.getInstance().createBitmap());
                realCode = Code.getInstance().getCode().toLowerCase();
                break;
            case R.id.bt_registeractivity_register:    //注册按钮
                //获取用户输入的用户名、密码、验证码

                new Thread(new Runnable() {
                    @Override
                    public void run() {
                        String username = mEtRegisteractivityUsername.getText().toString();
                        String password = mEtRegisteractivityPassword2.getText().toString();
                        String phoneCode = mEtRegisteractivityPhonecodes.getText().toString().toLowerCase();
                        String email = mEtRegisteractivityEmail.getText().toString();

                        Looper.prepare();
                        try {
                            Class.forName("com.mysql.jdbc.Driver");
                            System.out.println("驱动加载成功！！！");
                            String url ="jdbc:mysql://rm-bp12m3039u29b56w32o.mysql.rds.aliyuncs.com:3306/shi_pin_xxq?useSSL=false&serverTimezone=UTC&allowPublicKeyRetrieval=true";
                            //连接数据库使用的用户名
                            String name = "root";
                            String passwd = "POiu0987";
                            try {
                                connection = DriverManager.getConnection(url, name, passwd);
                                System.out.println("连接数据库成功！！！");

                            } catch (SQLException e) {
                                System.out.println("连接数据库shibai！！！");
                            }
                            String sql = "INSERT INTO test (name,password,email) VALUES (?,?,?)";

                            //Toast.makeText(RegisterActivity.this,"注册成功",Toast.LENGTH_SHORT).show();
//                            System.out.println(username);
//                            System.out.println(password);
//                            System.out.println(email);
//                            System.out.println(phoneCode);
                            //注册验证
                            if (!TextUtils.isEmpty(password)&& !TextUtils.isEmpty(password) && !TextUtils.isEmpty(phoneCode)&&!TextUtils.isEmpty(email) ) {
                                if (phoneCode.equals(realCode)) {


                                    String checksql = "SELECT * FROM TEST";
                                    // 创建用来执行sql语句的对象
                                    java.sql.Statement statement = connection.createStatement();

                                    // 执行sql查询语句并获取查询信息
                                    ResultSet rs = statement.executeQuery(checksql);

                                    String user[] = new String[100];
                                    String checkpassword[] = new String[100];
                                    int i = 0, j = 0,k=0;
                                    while (rs.next()) {//循环数据库数据，每条数据都保存到数组user里面
                                        String UserName = rs.getString("name");
                                        String UserPasswd = rs.getString("password")
                                                .replace((char) 12288, ' ').trim();
                                        user[i++] = UserName;
                                        checkpassword[j++] = UserPasswd;
                                       // System.out.println(user[i]);
                                    }
                                    int userlength = user.length - 1;
                                    Log.e("数组长度: ", String.valueOf(userlength));

                                    for (i = 0; i < user.length; i++){
                                        //输入的数据和数组挨个比对，一条输入的数据和数组全部数据进行比对，判断是否注册
                                        if (username.equals(user[i])) {
                                            // Toast.makeText(getApplicationContext(), "该账户已经被注册过！", Toast.LENGTH_SHORT).show();
                                            k++;
                                        }
                                    }

                                    if(k==0){
                                        //将用户名和密码加入到数据库中
                                        PreparedStatement ps=connection.prepareStatement(sql);
                                        //获取输入框的数据 添加到mysql数据库
                                        ps.setString(1, username);
                                        ps.setString(2, password);
                                        ps.setString(3, email);
                                        ps.executeUpdate();//更新数据库

                                        Toast.makeText(RegisterActivity.this,"注册成功",Toast.LENGTH_SHORT).show();
                                        Intent intent = new Intent(RegisterActivity.this, MainActivity.class);
                                        startActivity(intent);
                                        connection.close();
                                        finish();
                                    }else{
                                        Toast.makeText(RegisterActivity.this,"该账号已有人注册！",Toast.LENGTH_SHORT).show();
                                    }




                                }
                                else {
                                    Toast.makeText(RegisterActivity.this,"注册失败",Toast.LENGTH_SHORT).show();
                                }
                            }else {
                                Toast.makeText(RegisterActivity.this,"未完善信息，注册失败",Toast.LENGTH_SHORT).show();
                            }



                        } catch (SQLException e) {
                            e.printStackTrace();
                        } catch (ClassNotFoundException e) {
                            e.printStackTrace();
                        } finally {
                            if(connection == null){
                                try{
                                    connection.close();
                                }catch (Exception e){
                                    e.printStackTrace();
                                }
                            }
                        }
                        Looper.loop();
                    }
                }).start();

        }
    }
}

