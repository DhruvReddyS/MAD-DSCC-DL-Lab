package com.example.gps;

import android.Manifest;
import android.content.pm.PackageManager;
import android.location.*;
import android.os.Bundle;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity implements LocationListener {
    TextView tv;

    protected void onCreate(Bundle b) {
        super.onCreate(b);
        tv = new TextView(this);
        tv.setTextSize(24); tv.setPadding(50, 150, 50, 50);
        tv.setText("Getting location...");
        setContentView(tv);

        if (checkSelfPermission(Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED)
            requestPermissions(new String[]{Manifest.permission.ACCESS_FINE_LOCATION,
                    Manifest.permission.ACCESS_COARSE_LOCATION}, 1);
        else start();
    }

    public void onRequestPermissionsResult(int c, String[] p, int[] r) {
        super.onRequestPermissionsResult(c, p, r);
        if (r.length > 0 && r[0] == PackageManager.PERMISSION_GRANTED) start();
    }

    @SuppressWarnings("MissingPermission")
    void start() {
        LocationManager lm = (LocationManager) getSystemService(LOCATION_SERVICE);
        lm.requestLocationUpdates(LocationManager.GPS_PROVIDER, 1000, 0, this);
    }

    public void onLocationChanged(Location loc) {
        tv.setText("Latitude: " + loc.getLatitude() + "\nLongitude: " + loc.getLongitude());
    }
}
