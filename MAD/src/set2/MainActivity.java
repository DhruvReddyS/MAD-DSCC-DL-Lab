package com.example.sdcard;

import android.os.Bundle;
import android.widget.*;
import androidx.appcompat.app.AppCompatActivity;
import java.io.*;

public class MainActivity extends AppCompatActivity {
    protected void onCreate(Bundle b) {
        super.onCreate(b);
        LinearLayout l = new LinearLayout(this);
        l.setOrientation(LinearLayout.VERTICAL);
        l.setPadding(50, 150, 50, 50);

        EditText data = new EditText(this); data.setHint("Enter data");
        Button write = new Button(this); write.setText("Write to SD Card");
        Button read = new Button(this); read.setText("Read from SD Card");
        TextView out = new TextView(this); out.setTextSize(20);
        l.addView(data); l.addView(write); l.addView(read); l.addView(out);
        setContentView(l);

        File file = new File(getExternalFilesDir(null), "mydata.txt"); // SD card (external storage)

        write.setOnClickListener(v -> {
            try (FileWriter fw = new FileWriter(file)) {
                fw.write(data.getText().toString());
                out.setText("Saved to: " + file.getAbsolutePath());
            } catch (IOException e) { out.setText("Error: " + e); }
        });

        read.setOnClickListener(v -> {
            try (BufferedReader br = new BufferedReader(new FileReader(file))) {
                out.setText("File data: " + br.readLine());
            } catch (IOException e) { out.setText("Error: " + e); }
        });
    }
}
