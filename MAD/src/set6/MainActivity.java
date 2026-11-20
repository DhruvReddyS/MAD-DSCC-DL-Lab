package com.example.calculator;

import android.os.Bundle;
import android.widget.*;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {
    EditText n1, n2;
    TextView res;

    protected void onCreate(Bundle b) {
        super.onCreate(b);
        LinearLayout l = new LinearLayout(this);
        l.setOrientation(LinearLayout.VERTICAL);
        l.setPadding(50, 150, 50, 50);

        n1 = new EditText(this); n1.setHint("Enter number 1");
        n2 = new EditText(this); n2.setHint("Enter number 2");
        res = new TextView(this); res.setTextSize(26);
        l.addView(n1); l.addView(n2);

        for (String op : new String[]{"+", "-", "*", "/"}) {
            Button btn = new Button(this);
            btn.setText(op);
            btn.setOnClickListener(v -> calc(op));
            l.addView(btn);
        }
        l.addView(res);
        setContentView(l);
    }

    void calc(String op) {
        try {
            double a = Double.parseDouble(n1.getText().toString());
            double b = Double.parseDouble(n2.getText().toString());
            if (op.equals("/") && b == 0) { res.setText("Cannot divide by 0"); return; }
            double r = op.equals("+") ? a + b : op.equals("-") ? a - b : op.equals("*") ? a * b : a / b;
            res.setText("Result: " + r);
        } catch (Exception e) {
            res.setText("Enter both numbers");
        }
    }
}
