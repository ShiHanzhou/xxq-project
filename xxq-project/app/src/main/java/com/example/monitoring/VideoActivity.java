package com.example.monitoring;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.os.Looper;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

import java.net.Socket;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class VideoActivity extends AppCompatActivity implements View.OnClickListener{

    private ExecutorService mThreadPool;//线程池管理
    private Socket socket;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_video);

        initView();
    }
    private void initView(){
        Button mBtVideocon = findViewById(R.id.btn_connect);

        // 绑定点击监听器
        mBtVideocon.setOnClickListener(this);
    }
    public void onClick(View view) {

        switch (view.getId()) {
            case R.id.btn_connect: //返回登录页面



                mThreadPool.execute(new Runnable() {
                    @Override
                    public void run() {
                        try {
                            /*
                            建立请求连接
                             */
                            socket = new Socket("127.0.0.1", 1935);
                            System.out.println(socket.isConnected());


                            runOnUiThread(new Runnable() {
                                @Override
                                public void run() {
                                    if (socket.isConnected()) {
                                        Looper.prepare();
                                        Toast.makeText(VideoActivity.this, "建立连接成功", Toast.LENGTH_SHORT).show();
                                        Looper.loop();

                                    } else {
                                        Looper.prepare();
                                        Toast.makeText(VideoActivity.this, "建立连接失败", Toast.LENGTH_SHORT).show();
                                        Looper.loop();

                                    }
                                }
                            });
                        } catch (Exception e) {
                            e.printStackTrace();
                        }
                    }
                });
                break;
        }
    }


}
