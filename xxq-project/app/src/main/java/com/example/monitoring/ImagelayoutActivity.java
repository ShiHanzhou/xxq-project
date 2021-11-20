package com.example.monitoring;




import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.drawable.BitmapDrawable;
import android.graphics.drawable.Drawable;
import android.os.Bundle;
import android.os.Looper;
import android.text.TextUtils;
import android.util.Base64;
import android.util.Log;
import android.view.LayoutInflater;
import android.widget.ImageView;
import android.widget.ListView;

import android.view.View;
import android.view.ViewGroup;
import android.widget.Toast;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.TimeUnit;

public class ImagelayoutActivity extends AppCompatActivity {
    private ImageView mIvImageaivityBack;
    private List<ImageListArray> onePieceList = new ArrayList<>();
    private Connection connection;
    private String time[] = new String[100];
    private String photo[] = new String[100];
    private int count;

    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        mIvImageaivityBack = findViewById(R.id.iv_image_back);
        setContentView(R.layout.activity_list_view);
        getByteFromMysql();
        addingData(); //初始化数据
        //创建适配器，在适配器中导入数据 1.当前类 2.list_view一行的布局 3.数据集合
        ImageListAdapter imageListAdapter = new ImageListAdapter(ImagelayoutActivity.this,R.layout.activity_image,onePieceList);
        ListView listView = (ListView)findViewById(R.id.ImageListView1); //将适配器导入Listview
        listView.setAdapter(imageListAdapter);
        //mIvImageaivityBack.setOnClickListener(this);
    }

//    public void onClick(View view) {
//        switch (view.getId()) {
//            // 跳转到注册界面
//            case R.id.iv_image_back:
//                startActivity(new Intent(this, MainActivity.class));
//                finish();
//                break;
//        }
//    }
    public void getByteFromMysql(){
        new Thread(new Runnable() {
            @Override
            public void run() {

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

                    String sql = "SELECT * FROM PHOTO";
                    //获取输入框的数据
                    // 创建用来执行sql语句的对象
                    java.sql.Statement statement = connection.createStatement();
                    // 执行sql查询语句并获取查询信息
                    ResultSet rs = statement.executeQuery(sql);
                    // 创建用来执行sql语句的对象


                    int i = 0, j = 0;
                    while (rs.next()) {//循环数据库数据，每条数据都保存到数组user里面
                        String time_ = rs.getString("datetime");
                        String photo_ = rs.getString("photo")
                                .replace((char) 12288, ' ').trim();
                        time[i++] = time_;
                        photo[j++] = photo_;
                        count++;
                        System.out.println(count);
                    }
                  //  System.out.println(i);
                } catch (ClassNotFoundException e) {
                    e.printStackTrace();
                } catch (SQLException e) {
                    e.printStackTrace();
                }
            }
        }).start();
        try {
            // 等待全部子线程执行完毕
            TimeUnit.SECONDS.sleep(1);
        } catch (InterruptedException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }

        System.out.println(1111111);
    }
    public static Bitmap stringToBitmap(String string) {
        Bitmap bitmap = null;

        try {
            byte[] bitmapArray = Base64.decode(string, Base64.DEFAULT);

            bitmap = BitmapFactory.decodeByteArray(bitmapArray, 0, bitmapArray.length);
        } catch (Exception e) {
            e.printStackTrace();
        }

        return bitmap;
    }
    public Drawable chage_to_drawable(Bitmap bp) {
        Bitmap bm=bp;
        BitmapDrawable bd= new BitmapDrawable(bm);
        return bd;
    }
    public void addingData(){
        // getByteFromMysql();
        for(int i=0;i<count;i++){
            Bitmap b = stringToBitmap(photo[i]);
            Drawable drawable = new BitmapDrawable(b);
            String s = time[i];
            ImageListArray barbe_blanche =new ImageListArray(s,drawable);
            onePieceList.add(barbe_blanche);
        }
    }


//
//    public void onClick(View view) {
//        if(view.getId() == R.id.iv_image_back){
//            Intent intent1 = new Intent(this, MainActivity.class);
//            startActivity(intent1);
//            finish();
//        }
//
//    }
}

//        String s = "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";
//        Bitmap b = stringToBitmap(s);
//        Drawable d;
//        Drawable d1=chage_to_drawable(b);
//        System.out.println(d1);
//        ImageView i1;
//        i1=findViewById(R.id.imageView);
//        i1.setImageDrawable(d1);

//    public static Bitmap stringToBitmap(String string) {
//        Bitmap bitmap = null;
//
//        try {
//            byte[] bitmapArray = Base64.decode(string, Base64.DEFAULT);
//
//            bitmap = BitmapFactory.decodeByteArray(bitmapArray, 0, bitmapArray.length);
//        } catch (Exception e) {
//            e.printStackTrace();
//        }
//
//        return bitmap;
//    }
//
//        public Drawable chage_to_drawable(Bitmap bp) {
//            Bitmap bm=bp;
//            BitmapDrawable bd= new BitmapDrawable(bm);
//            return bd;
//        }
//


//    public Bitmap stringToBitmap(byte[] string) {
//        Bitmap bitmap = null;
//        try {
////base64转字节数组
//            byte[] bitmapArray = Base64.decode(string, Base64.DEFAULT);
//            bitmap = BitmapFactory.decodeByteArray(bitmapArray, 0, bitmapArray.length);
//        } catch (Exception e) {
//            e.printStackTrace();
//        }
//        return bitmap;
//
//    }

//    private List<Map<String,Object>> getData() {
//        String s = "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";
//        Bitmap b = stringToBitmap(s);
//        System.out.println(b);
//
//        String[] title = {
//                "企业会话",
//                "办公邮件",
//                "财务信息查询",
//        };
//        String[] info = {
//                "嘿,你好",
//                "写信",
//                "发补贴了",
//        };
//        int[] imageId = {
//                R.drawable.xj,
//                R.drawable.lock,
//                R.drawable.cw
//
//        };
//        List<Map<String,Object>>listItems = new ArrayList<Map<String,Object>>();
//        //通过循环将图片放到集合里
//        for(int i=0;i<title.length;i++) {
//            Map<String,Object> map = new HashMap<String,Object>();
//            map.put("title",title[i]);
//            map.put("info",info[i]);
//            map.put("img",imageId[i]);
//            listItems.add(map);
//        }
//
//        return listItems;
//    }


