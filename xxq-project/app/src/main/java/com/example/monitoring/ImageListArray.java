package com.example.monitoring;

/**
 * Created by prize on 2018/4/11.
 */


import android.graphics.drawable.Drawable;

/**
 * Created by prize on 2018/4/11.
 */

public class ImageListArray {
    private String name;
    private int imageId;
    private Drawable drawable;
    public ImageListArray(String name, Drawable drawable){
        this.name = name;
        this.drawable = drawable;
    }
    public Drawable getDrawable() {
        return drawable;
    }
    public void setDrawable(Drawable drawable) {
        this.drawable = drawable;
    }

    public String getName() {
        return name;
    }
    public int getImageId() {
        return imageId;
    }
}