package com.example.alarm;

import android.app.*;
import android.content.*;
import android.media.RingtoneManager;
import android.os.Bundle;
import android.widget.*;
import androidx.appcompat.app.AppCompatActivity;
import java.util.Calendar;

public class MainActivity extends AppCompatActivity {
    protected void onCreate(Bundle b) {
        super.onCreate(b);
        LinearLayout l = new LinearLayout(this);
        l.setOrientation(LinearLayout.VERTICAL);
        TimePicker tp = new TimePicker(this);
        Button set = new Button(this); set.setText("Set Alarm");
        l.addView(tp); l.addView(set);
        setContentView(l);

        set.setOnClickListener(v -> {
            Calendar c = Calendar.getInstance();
            c.set(Calendar.HOUR_OF_DAY, tp.getHour());
            c.set(Calendar.MINUTE, tp.getMinute());
            c.set(Calendar.SECOND, 0);
            if (c.before(Calendar.getInstance())) c.add(Calendar.DATE, 1);

            PendingIntent pi = PendingIntent.getBroadcast(this, 0,
                    new Intent(this, AlarmReceiver.class), PendingIntent.FLAG_IMMUTABLE);
            AlarmManager am = (AlarmManager) getSystemService(ALARM_SERVICE);
            am.setExact(AlarmManager.RTC_WAKEUP, c.getTimeInMillis(), pi);
            Toast.makeText(this, "Alarm set for " + tp.getHour() + ":" + tp.getMinute(), Toast.LENGTH_SHORT).show();
        });
    }

    public static class AlarmReceiver extends BroadcastReceiver {
        public void onReceive(Context c, Intent i) {
            Toast.makeText(c, "Wake up! Alarm ringing", Toast.LENGTH_LONG).show();
            RingtoneManager.getRingtone(c, RingtoneManager.getDefaultUri(RingtoneManager.TYPE_ALARM)).play();
        }
    }
}
