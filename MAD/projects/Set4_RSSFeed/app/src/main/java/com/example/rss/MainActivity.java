package com.example.rss;

import android.os.Bundle;
import android.widget.*;
import androidx.appcompat.app.AppCompatActivity;
import java.io.InputStream;
import java.net.URL;
import java.util.ArrayList;
import org.xmlpull.v1.*;

public class MainActivity extends AppCompatActivity {
    ArrayList<String> titles = new ArrayList<>();

    protected void onCreate(Bundle b) {
        super.onCreate(b);
        ListView lv = new ListView(this);
        setContentView(lv);

        new Thread(() -> {
            try {
                InputStream in = new URL("https://feeds.bbci.co.uk/news/rss.xml").openStream();
                XmlPullParser p = XmlPullParserFactory.newInstance().newPullParser();
                p.setInput(in, null);
                boolean inItem = false;
                while (p.next() != XmlPullParser.END_DOCUMENT) {
                    if (p.getEventType() == XmlPullParser.START_TAG) {
                        if (p.getName().equals("item")) inItem = true;
                        else if (inItem && p.getName().equals("title")) titles.add(p.nextText());
                    }
                }
            } catch (Exception e) { titles.add("Error: " + e.getMessage()); }
            runOnUiThread(() -> lv.setAdapter(
                    new ArrayAdapter<>(this, android.R.layout.simple_list_item_1, titles)));
        }).start();
    }
}
