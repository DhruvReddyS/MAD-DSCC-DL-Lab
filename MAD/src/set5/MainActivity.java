package com.example.sendmail;

import android.content.Intent;
import android.os.Bundle;
import android.widget.*;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {
    protected void onCreate(Bundle b) {
        super.onCreate(b);
        LinearLayout l = new LinearLayout(this);
        l.setOrientation(LinearLayout.VERTICAL);
        l.setPadding(50, 150, 50, 50);

        EditText to = new EditText(this); to.setHint("To");
        EditText sub = new EditText(this); sub.setHint("Subject");
        EditText msg = new EditText(this); msg.setHint("Message");
        Button send = new Button(this); send.setText("Send Email");
        l.addView(to); l.addView(sub); l.addView(msg); l.addView(send);
        setContentView(l);

        send.setOnClickListener(v -> {
            Intent i = new Intent(Intent.ACTION_SEND);
            i.setType("message/rfc822");
            i.putExtra(Intent.EXTRA_EMAIL, new String[]{to.getText().toString()});
            i.putExtra(Intent.EXTRA_SUBJECT, sub.getText().toString());
            i.putExtra(Intent.EXTRA_TEXT, msg.getText().toString());
            startActivity(Intent.createChooser(i, "Send email using"));
        });
    }
}
