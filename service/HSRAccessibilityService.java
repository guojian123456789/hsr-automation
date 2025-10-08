package com.hsr.automation;

import android.accessibilityservice.AccessibilityService;
import android.accessibilityservice.GestureDescription;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.graphics.Path;
import android.util.Log;
import android.view.accessibility.AccessibilityEvent;

/**
 * HSR Automation 无障碍服务
 * 用于执行屏幕点击和滑动手势
 */
public class HSRAccessibilityService extends AccessibilityService {
    
    private static final String TAG = "HSRAccessibility";
    private static final String ACTION_DISPATCH_GESTURE = "com.hsr.automation.DISPATCH_GESTURE";
    private static final String ACTION_CLICK = "com.hsr.automation.CLICK";
    private static final String ACTION_SWIPE = "com.hsr.automation.SWIPE";
    
    private static HSRAccessibilityService instance;
    private GestureReceiver gestureReceiver;
    
    public static HSRAccessibilityService getInstance() {
        return instance;
    }
    
    @Override
    public void onCreate() {
        super.onCreate();
        instance = this;
        
        // 注册广播接收器
        gestureReceiver = new GestureReceiver();
        IntentFilter filter = new IntentFilter();
        filter.addAction(ACTION_CLICK);
        filter.addAction(ACTION_SWIPE);
        registerReceiver(gestureReceiver, filter);
        
        Log.i(TAG, "HSR Accessibility Service Created");
    }
    
    @Override
    protected void onServiceConnected() {
        super.onServiceConnected();
        Log.i(TAG, "HSR Accessibility Service Connected");
    }
    
    @Override
    public void onAccessibilityEvent(AccessibilityEvent event) {
        // 这里可以监听界面变化事件
    }
    
    @Override
    public void onInterrupt() {
        Log.i(TAG, "HSR Accessibility Service Interrupted");
    }
    
    @Override
    public void onDestroy() {
        super.onDestroy();
        if (gestureReceiver != null) {
            unregisterReceiver(gestureReceiver);
        }
        instance = null;
        Log.i(TAG, "HSR Accessibility Service Destroyed");
    }
    
    /**
     * 执行点击手势
     */
    public void performClick(float x, float y, int duration) {
        Log.i(TAG, String.format("Performing click at (%.0f, %.0f) duration: %dms", x, y, duration));
        
        Path clickPath = new Path();
        clickPath.moveTo(x, y);
        
        GestureDescription.StrokeDescription clickStroke =
                new GestureDescription.StrokeDescription(clickPath, 0, duration);
        
        GestureDescription.Builder builder = new GestureDescription.Builder();
        builder.addStroke(clickStroke);
        
        GestureDescription gesture = builder.build();
        
        dispatchGesture(gesture, new GestureResultCallback() {
            @Override
            public void onCompleted(GestureDescription gestureDescription) {
                super.onCompleted(gestureDescription);
                Log.i(TAG, "Click gesture completed");
            }
            
            @Override
            public void onCancelled(GestureDescription gestureDescription) {
                super.onCancelled(gestureDescription);
                Log.w(TAG, "Click gesture cancelled");
            }
        }, null);
    }
    
    /**
     * 执行滑动手势
     */
    public void performSwipe(float startX, float startY, float endX, float endY, int duration) {
        Log.i(TAG, String.format("Performing swipe from (%.0f, %.0f) to (%.0f, %.0f)",
                startX, startY, endX, endY));
        
        Path swipePath = new Path();
        swipePath.moveTo(startX, startY);
        swipePath.lineTo(endX, endY);
        
        GestureDescription.StrokeDescription swipeStroke =
                new GestureDescription.StrokeDescription(swipePath, 0, duration);
        
        GestureDescription.Builder builder = new GestureDescription.Builder();
        builder.addStroke(swipeStroke);
        
        GestureDescription gesture = builder.build();
        
        dispatchGesture(gesture, new GestureResultCallback() {
            @Override
            public void onCompleted(GestureDescription gestureDescription) {
                super.onCompleted(gestureDescription);
                Log.i(TAG, "Swipe gesture completed");
            }
            
            @Override
            public void onCancelled(GestureDescription gestureDescription) {
                super.onCancelled(gestureDescription);
                Log.w(TAG, "Swipe gesture cancelled");
            }
        }, null);
    }
    
    /**
     * 广播接收器 - 接收来自Python的手势请求
     */
    private class GestureReceiver extends BroadcastReceiver {
        @Override
        public void onReceive(Context context, Intent intent) {
            String action = intent.getAction();
            
            if (ACTION_CLICK.equals(action)) {
                float x = intent.getFloatExtra("x", 0);
                float y = intent.getFloatExtra("y", 0);
                int duration = intent.getIntExtra("duration", 100);
                
                performClick(x, y, duration);
                
            } else if (ACTION_SWIPE.equals(action)) {
                float startX = intent.getFloatExtra("start_x", 0);
                float startY = intent.getFloatExtra("start_y", 0);
                float endX = intent.getFloatExtra("end_x", 0);
                float endY = intent.getFloatExtra("end_y", 0);
                int duration = intent.getIntExtra("duration", 300);
                
                performSwipe(startX, startY, endX, endY, duration);
            }
        }
    }
}




