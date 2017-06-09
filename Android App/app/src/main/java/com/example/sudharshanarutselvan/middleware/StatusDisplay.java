package com.example.sudharshanarutselvan.middleware;

import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.support.v4.app.NotificationCompat;
import android.util.Log;
import android.widget.CompoundButton;
import android.widget.EditText;
import android.widget.RelativeLayout;
import android.widget.TextView;
import android.widget.ToggleButton;

import com.pubnub.api.PNConfiguration;
import com.pubnub.api.PubNub;
import com.pubnub.api.callbacks.PNCallback;
import com.pubnub.api.models.consumer.PNPublishResult;
import com.pubnub.api.models.consumer.PNStatus;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

/**
 * Created by SudharshanArutselvan on 5/19/2017.
 */

public class StatusDisplay extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.statusdisplay);
        Intent intent = getIntent();
        String message = intent.getStringExtra(MainActivity.EXTRA_MESSAGE);

        PNConfiguration pnConfiguration = new PNConfiguration();
        pnConfiguration.setSubscribeKey("sub-c-09f86e3c-2e1e-11e7-97de-0619f8945a4f");
        pnConfiguration.setPublishKey("pub-c-52dfaf38-9202-447f-a5c4-4fffdd0fdeac");
        final PubNub pubnub = new PubNub(pnConfiguration);

        RelativeLayout rl = (RelativeLayout)findViewById(R.id.LayoutID);

        // Capture the layout's TextView and set the string as its text
        // EditText textView = (EditText) findViewById(R.id.DisplayScreen);
        try{
            JSONObject reader=new JSONObject(message);
            JSONArray nameArr = reader.names();
            Log.d("TAG","Im here");
            int count=0;count++;
            for(int i=0;i<nameArr.length();i++){
                Log.d("TAG","Tags are "+nameArr.getString(i));
                JSONObject roomType  = reader.getJSONObject(nameArr.getString(i));
                JSONArray secondArr = roomType.names();

                RelativeLayout.LayoutParams topParams = new RelativeLayout.LayoutParams(RelativeLayout.LayoutParams.WRAP_CONTENT, RelativeLayout.LayoutParams.WRAP_CONTENT);

                TextView tv = new TextView(this);
                tv.setText(nameArr.getString(i));
                tv.setId(count);
                topParams.setMargins(50,50,50,50);

                if (i > 0) {
                    topParams.addRule(RelativeLayout.BELOW, count - 1);
                    //topParams.setMargins(50,50,50,50);topParams.setMargins(50,50,50,50);

                }
                tv.setLayoutParams(topParams);
                count++;
                rl.addView(tv);

                for(int j=0;j<secondArr.length();j++) {

                    JSONObject deviceType = roomType.getJSONObject(secondArr.getString(j));

                    RelativeLayout.LayoutParams firstParams = new RelativeLayout.LayoutParams(RelativeLayout.LayoutParams.WRAP_CONTENT, RelativeLayout.LayoutParams.WRAP_CONTENT);
                    String status = deviceType.getString("Status");
                    TextView device = new TextView(this);
                    device.setText(secondArr.getString(j));
                    firstParams.addRule(RelativeLayout.BELOW, count-1);
                    firstParams.setMargins(50,50,50,50);
                    device.setId(count);
                    device.setLayoutParams(firstParams);
                    count++;
                    rl.addView(device);

                    RelativeLayout.LayoutParams newParams = new RelativeLayout.LayoutParams(RelativeLayout.LayoutParams.WRAP_CONTENT, RelativeLayout.LayoutParams.WRAP_CONTENT);

                    ToggleButton tb = new ToggleButton(this);
                    tb.setTextOn(" ON");
                    tb.setTextOff("OFF");
                    Log.d("TAG", "3: " + secondArr.getString(j));
                    if(status.compareTo("true")==0) tb.setChecked(true);
                    else tb.setChecked(false);
                    newParams.addRule(RelativeLayout.BELOW, count-2);
                    newParams.addRule(RelativeLayout.RIGHT_OF, count-1);
                    newParams.setMargins(200,0,50,0);
                    tb.setContentDescription(nameArr.getString(i)+":"+secondArr.getString(j)+":");
                    tb.setLayoutParams(newParams);
                    tb.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {

                        @Override
                        public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                            // TODO Auto-generated method stub
                            Log.d("TAG", "listener true "+ buttonView.getContentDescription()+isChecked);
                            pubnub.publish().channel("Control").message(""+buttonView.getContentDescription()+isChecked).async(new PNCallback<PNPublishResult>() {
                                @Override
                                public void onResponse(PNPublishResult result, PNStatus status) {
                                    // Check whether request successfully completed or not.
                                    if (!status.isError()) {
                                        Log.d("TAG", "Published!");
                                        // Message successfully published to specified channel.

                                    }
                                    // Request processing failed.
                                    else {
                                        Log.d("TAG", "Not Published!");
                                        // Handle message publish error. Check 'category' property to find out possible issue
                                        // because of which request did fail.
                                        //
                                        // Request can be resent using: [status retry];
                                    }
                                }
                            });
                        }
                    });
                    rl.addView(tb);
                    //textView.append(nameArr.getString(i)+ ": " +secondArr.getString(j)+": "+status+"\n");
                }
            }
        }
        catch(final JSONException e){
            Log.d("Error","Error: "+e.getMessage());
        }
        addNotification();
        //textView.setText(message);
    }

    private void addNotification() {
        NotificationCompat.Builder builder =
                new NotificationCompat.Builder(this)
                        .setSmallIcon(R.drawable.icon)
                        .setContentTitle("Notifications Example")
                        .setContentText("This is a test notification");

        Intent notificationIntent = new Intent(this, MainActivity.class);
        PendingIntent contentIntent = PendingIntent.getActivity(this, 0, notificationIntent,
                PendingIntent.FLAG_UPDATE_CURRENT);
        builder.setContentIntent(contentIntent);

        // Add as notification
        NotificationManager manager = (NotificationManager) getSystemService(Context.NOTIFICATION_SERVICE);
        manager.notify(0, builder.build());
    }
}
