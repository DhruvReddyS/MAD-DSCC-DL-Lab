# Lab Programs (MAD · DSCC · DL)

Open `index.html` in a browser (works from a file or on GitHub Pages).

| Folder | Contents |
| --- | --- |
| `MAD/src/set1..set7/` | Android (Java) programs: `MainActivity.java` + `AndroidManifest.xml` |
| `MAD/outputs.json` | Tested emulator output for each set (edit, then rebuild) |
| `DSCC/exp06_2pc … exp12_bigtable/` | Experiments 6–12: Java, SQL, CQL, Node.js and cloud commands, with `output.txt` (ran locally) or `expected_output.txt` (cloud steps) |
| `DL/cnn.py rnn.py lstm.py gan.py` | Keras programs; `DL/outputs/*.txt` are real run outputs; `DL/run_all.sh` reruns them |
| `build_site.py` | Builds `index.html` from the source files + outputs (text content is inside this script) |
| `index.html`, `site.js`, `style.css` | The website |

Rebuild after editing any program or output:

```sh
python3 build_site.py
```

Sets / experiments:

- **MAD**: 1 GPS location · 2 Write to SD card · 3 SMS alert (BroadcastReceiver) · 4 RSS feed · 5 Send email · 6 Calculator · 7 Alarm clock
- **DSCC**: 6 Two-Phase Commit · 7 FTP (sockets) · 8 EC2 + IIS · 9 MySQL on RDS · 10 Cassandra CRUD · 11 Node.js on EC2 · 12 Cloud Bigtable
- **DL**: CNN (MNIST) · RNN (IMDB) · LSTM (IMDB) · GAN (MNIST)
