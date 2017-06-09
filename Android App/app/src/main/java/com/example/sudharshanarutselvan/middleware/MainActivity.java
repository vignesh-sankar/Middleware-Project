package com.example.sudharshanarutselvan.middleware;

import android.content.Context;
import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import com.pubnub.api.*;
import com.pubnub.api.models.consumer.PNStatus;
import com.pubnub.api.models.consumer.pubsub.PNMessageResult;
import com.pubnub.api.models.consumer.pubsub.PNPresenceEventResult;
import com.pubnub.api.models.consumer.PNPublishResult;
import com.pubnub.api.callbacks.PNCallback;
import com.pubnub.api.enums.PNStatusCategory;
import com.pubnub.api.callbacks.SubscribeCallback;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

//import javax.security.auth.callback.Callback;
public class MainActivity extends AppCompatActivity {
    public static final String EXTRA_MESSAGE = "com.example.myfirstapp.MESSAGE";
    EditText username;
    EditText password;
    String user_name ;
    String pass_word;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

    }

    public void statusDisplay(View view){
        username = (EditText) findViewById(R.id.username);
        password = (EditText) findViewById(R.id.password);
        user_name = username.getText().toString();
        pass_word = password.getText().toString();

        connectToTomcat(view);

    }

    public void getStat(){
        PNConfiguration pnConfiguration = new PNConfiguration();
        pnConfiguration.setSubscribeKey("sub-c-09f86e3c-2e1e-11e7-97de-0619f8945a4f");
        pnConfiguration.setPublishKey("pub-c-52dfaf38-9202-447f-a5c4-4fffdd0fdeac");
        PubNub pubnub = new PubNub(pnConfiguration);

        pubnub.addListener(new SubscribeCallback() {
            @Override
            public void status(PubNub pubnub, PNStatus status) {


                if (status.getCategory() == PNStatusCategory.PNUnexpectedDisconnectCategory) {
                    // This event happens when radio / connectivity is lost
                    Log.d("TAG", "connection lost!");
                }

                else if (status.getCategory() == PNStatusCategory.PNConnectedCategory) {

                    // Connect event. You can do stuff like publish, and know you'll get it.
                    // Or just use the connected event to confirm you are subscribed for
                    // UI / internal notifications, etc

                    if (status.getCategory() == PNStatusCategory.PNConnectedCategory){
                        pubnub.publish().channel("GetStatus").message("hello!!").async(new PNCallback<PNPublishResult>() {
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
                }
                else if (status.getCategory() == PNStatusCategory.PNReconnectedCategory) {

                    // Happens as part of our regular operation. This event happens when
                    // radio / connectivity is lost, then regained.
                }
                else if (status.getCategory() == PNStatusCategory.PNDecryptionErrorCategory) {

                    // Handle messsage decryption error. Probably client configured to
                    // encrypt messages and on live data feed it received plain text.
                }
            }

            @Override
            public void message(PubNub pubnub, PNMessageResult message) {
                // Handle new message stored in message.message
                if (message.getChannel() != null) {
                    // Message has been received on channel group stored in
                    // message.getChannel()
                    Log.d("TAG", "Message received! \n"+message);
                    Intent intent = new Intent(getApplicationContext(), StatusDisplay.class);
                    String msg = message.getMessage().toString();
                    intent.putExtra(EXTRA_MESSAGE, msg);
                    startActivity(intent);
//                    TextView textView = (TextView) findViewById(R.id.printText);
//                    textView.setText(message.getMessage().getAsString());
                }
                else {
                    // Message has been received on channel stored in
                    // message.getSubscription()
                    Log.d("TAG", "Message in channel received! \n"+message);
//                    TextView textView = (TextView) findViewById(R.id.printText);
//                    textView.setText(message.getMessage().getAsString());
                }

            /*
                log the following items with your favorite logger
                    - message.getMessage()
                    - message.getSubscription()
                    - message.getTimetoken()
            */
            }

            @Override
            public void presence(PubNub pubnub, PNPresenceEventResult presence){

            }

        });

        pubnub.subscribe().channels(Arrays.asList("StatusChannel")).execute();
    }
    public int connectToTomcat(View view){

        RequestQueue queue = Volley.newRequestQueue(this);

        final Context context = this;
        String url = "http://ec2-54-69-109-215.us-west-2.compute.amazonaws.com:8085/login";


        StringRequest postRequest = new StringRequest(Request.Method.POST, url,
                new Response.Listener<String>()
                {
                    @Override
                    public void onResponse(String response) {

                        Log.d("response", response);
                        // response_name = (response.);
                        String response_name = response.replaceAll("[^a-zA-Z ]", "");
                        if(response_name.equals("Failed"))
                        {Log.d("error", response);}
                        else
                        {
                            getStat();

                        }
                    }
                },
                new Response.ErrorListener()
                {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        // error
                        Log.d("security.error", error.toString());
                    }
                }
        ) {
            @Override
            protected Map<String, String> getParams()
            {
                final Map<String, String> params = new HashMap<String, String>();
                Log.v("email",user_name);
                Log.v("pass_word",pass_word);
                params.put("email",user_name);
                params.put("password",pass_word);
                return params;
            }
        };


        // Add the request to the RequestQueue.
        queue.add(postRequest);


        return 1;
    }
}
