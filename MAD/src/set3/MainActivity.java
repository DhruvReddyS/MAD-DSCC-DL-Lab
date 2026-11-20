package com.example.smsalert;

import android.Manifest;
import android.app.AlertDialog;
import android.content.*;
import android.os.Bundle;
import android.provider.Telephony;
import android.telephony.SmsMessage;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {
    BroadcastReceiver receiver = new BroadcastReceiver() {
        public void onReceive(Context c, Intent i) {
            for (SmsMessage m : Telephony.Sms.Intents.getMessagesFromIntent(i)) {
                new AlertDialog.Builder(MainActivity.this)
                        .setTitle("New Message from " + m.getOriginatingAddress())
                        .setMessage(m.getMessageBody())
                        .setPositiveButton("OK", null).show();
            }
        }
    };

    protected void onCreate(Bundle b) {
        super.onCreate(b);
        TextView tv = new TextView(this);
        tv.setTextSize(22); tv.setPadding(50, 150, 50, 50);
        tv.setText("Waiting for messages...");
        setContentView(tv);
        requestPermissions(new String[]{Manifest.permission.RECEIVE_SMS}, 1);
        registerReceiver(receiver, new IntentFilter("android.provider.Telephony.SMS_RECEIVED"), RECEIVER_EXPORTED);
    }

    protected void onDestroy() {
        super.onDestroy();
        unregisterReceiver(receiver);
    }
}
