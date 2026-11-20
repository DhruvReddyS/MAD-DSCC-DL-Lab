#!/usr/bin/env python3
"""Builds index.html from the real source files and captured outputs.

Run from anywhere:  python3 build_site.py
Text content (aims, theory, run steps) lives in this file.
MAD tested outputs live in MAD/outputs.json.
Program code and outputs are read from MAD/src, DSCC/exp*, DL/.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8").rstrip("\n")


def lang_of(name):
    ext = name.rsplit(".", 1)[-1]
    return {"java": "java", "xml": "markup", "html": "markup", "py": "python",
            "js": "javascript", "sql": "sql", "cql": "sql", "sh": "bash",
            "txt": "none"}.get(ext, "none")


def files(*paths):
    return [{"name": Path(p).name, "lang": lang_of(p), "code": read(p)} for p in paths]


def strip_ansi(s):
    return re.sub(r"\x1b\[[0-9;]*m", "", s)


# --------------------------------------------------------------------- MAD
MAD_PROCEDURE = [
    "Open Android Studio → <b>New Project</b> → <b>Empty Views Activity</b> → Next.",
    "Name it anything, set <b>Language: Java</b>, Minimum SDK API 24 or higher → Finish.",
    "Open <code>app/java/&lt;your package&gt;/MainActivity.java</code>, delete everything and paste the given MainActivity.java. "
    "<b>Keep the first line</b> <code>package ...;</code> the same as your project's package.",
    "<b>No XML to write.</b> The screen is built in Java, so <code>activity_main.xml</code> is not used. "
    "Only GPS, SMS and RSS need 1–2 permission lines pasted in <code>AndroidManifest.xml</code> just above <code>&lt;application&gt;</code>.",
    "Click <b>Run ▶</b> and pick an emulator. Allow the permission if a popup asks.",
]

MAD = [
    dict(id="set1", title="Set 1 · GPS Location",
         question="Explain the role of GPS in Android. What steps and permissions are needed to get the current location? Write an app that shows the current location.",
         aim="To build an Android app that reads the device's current GPS location and shows latitude and longitude.",
         theory=[
             "GPS (Global Positioning System) uses satellites to find the device's latitude, longitude and altitude. Apps use it for maps, navigation, delivery tracking and geo-tagging.",
             "Android gives location through <b>LocationManager</b> (system service <code>LOCATION_SERVICE</code>). Providers: <code>GPS_PROVIDER</code> (accurate, outdoors) and <code>NETWORK_PROVIDER</code> (Wi-Fi / cell towers).",
             "Permissions in the manifest: <code>ACCESS_FINE_LOCATION</code> (GPS, exact) and <code>ACCESS_COARSE_LOCATION</code> (approximate). From Android 6 they are <b>dangerous permissions</b>, so the app must also ask at run time with <code>requestPermissions()</code>.",
             "Steps: (1) declare permissions, (2) check / request permission, (3) get LocationManager, (4) call <code>requestLocationUpdates(provider, minTime, minDistance, listener)</code>.",
             "The activity implements <b>LocationListener</b>; <code>onLocationChanged(Location)</code> is called with each new fix, and <code>getLatitude()</code> / <code>getLongitude()</code> give the values.",
             "On the emulator, send a fake location from <b>Extended controls (⋯) → Location</b> to test the app.",
         ],
         manifest_add='<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />\n<uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />',
         extra_run=["Emulator: ⋯ (Extended controls) → Location → enter latitude/longitude → <b>Set Location</b>."]),
    dict(id="set2", title="Set 2 · Write to SD Card",
         question="Explain external storage in Android. How do you write data to the SD card and which permissions are needed? Write an app that writes data to the SD card.",
         aim="To build an Android app that writes user-entered text to a file on external storage (SD card) and reads it back.",
         theory=[
             "<b>Internal storage</b> is private to the app; <b>external storage</b> (SD card / shared storage) is larger and can hold files like documents and media.",
             "<code>getExternalFilesDir(null)</code> returns the app's own folder on external storage: <code>/storage/emulated/0/Android/data/&lt;package&gt;/files</code>. It is removed when the app is uninstalled.",
             "Permission: <code>WRITE_EXTERNAL_STORAGE</code> was needed up to Android 9 (API 28). From Android 10 (scoped storage) the app's own external folder needs <b>no permission</b>, so nothing is added to the manifest.",
             "Before writing you can check that storage is mounted with <code>Environment.getExternalStorageState()</code>.",
             "Writing uses normal Java I/O: <code>FileWriter</code> / <code>FileOutputStream</code>. Reading uses <code>FileReader</code> + <code>BufferedReader</code>.",
             "In the app, the <b>Write</b> button saves the EditText text to <code>mydata.txt</code> and shows the path; the <b>Read</b> button reads it back.",
         ],
         manifest_add=None),
    dict(id="set3", title="Set 3 · SMS Alert (Broadcast Receiver)",
         question="What is a Broadcast Receiver? Explain how an app receives a message and raises an alert. Write an app that shows an alert when an SMS arrives.",
         aim="To build an Android app that uses a BroadcastReceiver to detect an incoming SMS and show an alert dialog.",
         theory=[
             "A <b>Broadcast Receiver</b> is an Android component that listens for system-wide messages (broadcasts) such as SMS received, battery low, boot completed or network change.",
             "We extend <code>BroadcastReceiver</code> and override <code>onReceive(Context, Intent)</code>; it runs when a matching broadcast arrives.",
             "Receivers are registered either in the manifest (static) or in code using <code>registerReceiver(receiver, IntentFilter)</code> (dynamic). Here it is registered in code for action <code>android.provider.Telephony.SMS_RECEIVED</code> and unregistered in <code>onDestroy()</code>.",
             "Permission: <code>RECEIVE_SMS</code> in the manifest and requested at run time.",
             "<code>Telephony.Sms.Intents.getMessagesFromIntent(intent)</code> gives <code>SmsMessage</code> objects; <code>getOriginatingAddress()</code> = sender, <code>getMessageBody()</code> = text.",
             "The alert is raised using <code>AlertDialog.Builder</code> with title (sender), message (SMS text) and an OK button.",
         ],
         manifest_add='<uses-permission android:name="android.permission.RECEIVE_SMS" />',
         extra_run=["Emulator: ⋯ (Extended controls) → Phone → enter a number and message → <b>Send Message</b>."]),
    dict(id="set4", title="Set 4 · RSS Feed Reader",
         question="What is an RSS feed? Explain how an Android app retrieves and displays RSS items. Write an RSS feed app.",
         aim="To build an Android app that downloads an RSS feed and shows the item titles in a list.",
         theory=[
             "<b>RSS</b> (Really Simple Syndication) is an XML format websites use to publish updates. A feed has a <code>&lt;channel&gt;</code> with many <code>&lt;item&gt;</code>s, each with <code>&lt;title&gt;</code>, <code>&lt;link&gt;</code>, <code>&lt;description&gt;</code>, <code>&lt;pubDate&gt;</code>.",
             "Permission: <code>INTERNET</code>, because the feed is downloaded from a URL.",
             "Network work must run on a <b>background thread</b> (here <code>new Thread()</code>); doing it on the main thread throws <code>NetworkOnMainThreadException</code>.",
             "The XML is read with <b>XmlPullParser</b>: loop over events, and when a <code>START_TAG</code> named <code>title</code> appears inside an <code>item</code>, read it with <code>nextText()</code>.",
             "Titles are stored in an <code>ArrayList</code>; the UI is updated with <code>runOnUiThread()</code>.",
             "A <b>ListView</b> with an <b>ArrayAdapter</b> displays one title per row.",
         ],
         manifest_add='<uses-permission android:name="android.permission.INTERNET" />'),
    dict(id="set5", title="Set 5 · Send Email",
         question="Explain the steps to send an email from an Android app. Which intent is used? Write an app to send an email.",
         aim="To build an Android app that collects To, Subject and Message and sends an email through an installed mail app using an Intent.",
         theory=[
             "Android apps send email by handing the job to an email app (Gmail, Outlook) using an <b>implicit Intent</b>; no password or SMTP code is needed.",
             "The intent action is <code>Intent.ACTION_SEND</code> (or <code>ACTION_SENDTO</code> with a <code>mailto:</code> URI).",
             "<code>setType(\"message/rfc822\")</code> marks the data as an email so only email apps respond.",
             "Data is added with extras: <code>EXTRA_EMAIL</code> (String array of addresses), <code>EXTRA_SUBJECT</code>, <code>EXTRA_TEXT</code> (body); optionally <code>EXTRA_CC</code>, <code>EXTRA_BCC</code>.",
             "<code>Intent.createChooser(intent, \"Send email using\")</code> lets the user pick the app; <code>startActivity()</code> launches it.",
             "No special permission is needed because the mail app does the actual sending.",
         ],
         manifest_add=None),
    dict(id="set6", title="Set 6 · Calculator",
         question="Explain the components and event handling of a native calculator app. Write a calculator app for + − × ÷.",
         aim="To build a simple Android calculator that adds, subtracts, multiplies and divides two numbers.",
         theory=[
             "UI components: two <b>EditText</b>s for the numbers, four <b>Button</b>s (+ − × ÷) and a <b>TextView</b> for the result, arranged in a vertical <b>LinearLayout</b>.",
             "<b>Event handling</b>: each button gets a listener with <code>setOnClickListener()</code>; when tapped, Android calls its <code>onClick</code> (here a lambda <code>v -&gt; calc(op)</code>).",
             "Input is read with <code>getText().toString()</code> and converted using <code>Double.parseDouble()</code>.",
             "The operator decides the calculation: a + b, a − b, a × b or a ÷ b.",
             "Errors are handled: dividing by 0 shows \"Cannot divide by 0\"; empty input is caught by <code>try/catch</code> and shows \"Enter both numbers\".",
             "The answer is shown with <code>setText(\"Result: \" + r)</code>. No permission is needed.",
         ],
         manifest_add=None),
    dict(id="set7", title="Set 7 · Alarm Clock",
         question="Explain alarms in Android. How does AlarmManager schedule and notify? Write an alarm clock app.",
         aim="To build an Android alarm clock that lets the user pick a time and shows a message and plays a tone at that time.",
         theory=[
             "<b>AlarmManager</b> is a system service that runs an action at a future time, even if the app is closed.",
             "The action to run is given either as a <b>PendingIntent</b> (to a BroadcastReceiver) or, simpler, as an <code>OnAlarmListener</code> callback (used here).",
             "<code>setExact(AlarmManager.RTC_WAKEUP, timeMillis, tag, listener, null)</code> schedules it; RTC_WAKEUP uses wall-clock time and wakes the device. Other methods: <code>set()</code>, <code>setRepeating()</code>, <code>cancel()</code>.",
             "The time is taken from a <b>TimePicker</b> and put into a <code>Calendar</code>; if it is already past, one day is added.",
             "At alarm time the listener runs: it shows a Toast and plays the alarm ringtone using <code>RingtoneManager</code>.",
             "An exact alarm with a listener needs <b>no permission and no manifest entry</b> (a PendingIntent version would need <code>SCHEDULE_EXACT_ALARM</code> and a <code>&lt;receiver&gt;</code>).",
         ],
         manifest_add=None),
]


def build_mad():
    outputs = json.loads(read("MAD/outputs.json"))
    progs = []
    for s in MAD:
        p = dict(s)
        p["files"] = files(f"MAD/src/{s['id']}/MainActivity.java")
        if not s.get("manifest_add"): p.pop("manifest_add", None)
        p["run"] = ["New Project → <b>Empty Views Activity</b> → Language <b>Java</b>.",
                    "Paste MainActivity.java (keep your own <code>package</code> line).",
                    "Paste the permission line(s) shown below into AndroidManifest.xml above <code>&lt;application&gt;</code>." if s.get("manifest_add")
                    else "Nothing to add in the manifest, no XML needed.",
                    *s.get("extra_run", []),
                    "Run ▶ on the emulator."]
        p.pop("extra_run", None)
        out = outputs.get(s["id"], "").strip()
        p["output"] = {"text": out or "(not tested yet)",
                       "badge": "Tested on emulator" if out else "Pending"}
        progs.append(p)
    return progs


# -------------------------------------------------------------------- DSCC
JAVA_RUN = "Needs JDK 8+ (<code>java -version</code>)."
DSCC = [
    dict(id="exp06", title="Exp 6 · Two-Phase Commit", dir="exp06_2pc",
         aim="To implement the Two-Phase Commit (2PC) protocol for coordinating a distributed transaction.",
         theory=[
             "2PC keeps a distributed transaction <b>atomic</b>: either every node commits or every node rolls back.",
             "One node is the <b>coordinator</b>; the others are <b>participants</b>.",
             "<b>Phase 1 – Prepare (voting):</b> the coordinator sends PREPARE; each participant replies YES (ready) or NO.",
             "<b>Phase 2 – Decision:</b> if <i>all</i> vote YES the coordinator sends COMMIT, else it sends ROLLBACK (abort).",
             "In the program, <code>prepare()</code> prints each vote and <code>allYes &amp;= ...</code> tracks if everyone agreed.",
             "Transaction 1 (all YES) commits; Transaction 2 (Node2 votes NO) rolls back on every node.",
         ],
         src=["TwoPhaseCommitDemo.java"],
         run=[JAVA_RUN, "<code>javac TwoPhaseCommitDemo.java</code>", "<code>java TwoPhaseCommitDemo</code>"],
         out="output.txt", badge="Ran locally (Java 21)"),
    dict(id="exp07", title="Exp 7 · FTP (Java Sockets)", dir="exp07_ftp",
         aim="To implement a simple file transfer between a client and a server using Java sockets.",
         theory=[
             "FTP (File Transfer Protocol) transfers files between computers using a <b>client–server</b> model over TCP.",
             "The server creates a <code>ServerSocket</code> on a port (5050) and waits with <code>accept()</code>.",
             "The client connects with <code>new Socket(\"localhost\", 5050)</code> and sends the file name.",
             "The server checks the file with <code>File.isFile()</code>: if found it sends <code>FOUND</code> and the file's lines, otherwise <code>NOTFOUND</code>.",
             "Streams: <code>BufferedReader</code> reads lines from the socket, <code>PrintWriter</code> (auto-flush) writes lines.",
             "The client prints the received contents (or \"File not found\") and both sockets are closed.",
         ],
         src=["FTPServer.java", "FTPClient.java", "sample.txt"],
         run=[JAVA_RUN, "Put both .java files and <code>sample.txt</code> in one folder.",
              "<code>javac FTPServer.java FTPClient.java</code>",
              "Terminal 1: <code>java FTPServer</code>",
              "Terminal 2: <code>java FTPClient</code> → type <code>sample.txt</code>",
              "Port 5050 is used because port 5000 is taken by AirPlay on macOS. Any free port works if both files match."],
         out="output.txt", badge="Ran locally (Java 21)"),
    dict(id="exp08", title="Exp 8 · EC2 Virtual Instance (IIS)", dir="exp08_ec2",
         aim="To create a Windows virtual machine on Amazon EC2 and host a web page on it using IIS.",
         theory=[
             "<b>Amazon EC2</b> (Elastic Compute Cloud) gives virtual servers (instances) on demand: an example of <b>IaaS</b>.",
             "An instance is launched from an <b>AMI</b> (here Windows Server) with an <b>instance type</b> (t2.micro / t3.micro, free tier).",
             "A <b>key pair</b> (.pem) is used to decrypt the Windows Administrator password.",
             "A <b>security group</b> is a firewall: allow RDP (3389) to log in and HTTP (80) for the website.",
             "<b>IIS</b> (Internet Information Services) is Windows' web server; it serves files from <code>C:\\inetpub\\wwwroot</code>.",
             "Opening <code>http://&lt;public-IP&gt;</code> in any browser shows our index.html.",
         ],
         src=["index.html"],
         run=["AWS Console → EC2 → <b>Launch instance</b>: name it, choose <b>Windows Server</b> AMI, type t2.micro/t3.micro.",
              "Create a key pair (.pem) and download it.",
              "Network settings: allow <b>RDP</b> and <b>HTTP</b> traffic → Launch.",
              "Instance → Connect → RDP client → <b>Get password</b> (upload .pem) → download the .rdp file and log in.",
              "Server Manager → Add Roles and Features → tick <b>Web Server (IIS)</b> → Install.",
              "Save index.html in <code>C:\\inetpub\\wwwroot</code> (delete or rename iisstart.htm).",
              "Open <code>http://PUBLIC-IP</code> in your browser. Stop/terminate the instance after the lab."],
         out="expected_output.txt", badge="Expected (cloud step, not run here)"),
    dict(id="exp09", title="Exp 9 · MySQL on Amazon RDS", dir="exp09_rds",
         aim="To create a MySQL database on Amazon RDS and perform CRUD operations from a client.",
         theory=[
             "<b>Amazon RDS</b> (Relational Database Service) is a managed database: AWS handles setup, backups, patching (<b>DBaaS / PaaS</b>).",
             "Engine chosen: <b>MySQL</b>; free-tier class db.t3.micro / db.t4g.micro.",
             "We set a master username and password; RDS gives an <b>endpoint</b> (host name) and port <b>3306</b>.",
             "The security group must allow inbound MySQL/Aurora (3306) from your IP, and <b>Public access = Yes</b> for connecting from a laptop.",
             "We connect using MySQL Workbench / SQLectron / <code>mysql</code> CLI with endpoint, user and password.",
             "CRUD = <b>C</b>reate (INSERT), <b>R</b>ead (SELECT), <b>U</b>pdate (UPDATE), <b>D</b>elete (DELETE).",
         ],
         src=["student.sql"],
         run=["AWS Console → RDS → <b>Create database</b> → Standard create → <b>MySQL</b> → Free tier.",
              "Set DB identifier, master username (e.g. admin) and password. Public access: <b>Yes</b>.",
              "After it is <b>Available</b>, copy the <b>Endpoint</b> from Connectivity &amp; security.",
              "Edit the security group: inbound rule MySQL/Aurora, port 3306, source My IP.",
              "Connect in MySQL Workbench (host = endpoint, port 3306) or CLI: <code>mysql -h ENDPOINT -u admin -p</code>",
              "Run the SQL in student.sql. Delete the database after the lab."],
         out="expected_output.txt", badge="Expected (cloud step; SQL checked with sqlite3)"),
    dict(id="exp10", title="Exp 10 · Cassandra CRUD", dir="exp10_cassandra",
         aim="To perform Create, Read, Update and Delete operations in Apache Cassandra using CQL.",
         theory=[
             "<b>Apache Cassandra</b> is a distributed <b>NoSQL</b> (wide-column) database with no single point of failure and high write speed.",
             "We run it in <b>Docker</b> so no installation is needed; <code>cqlsh</code> is the CQL shell.",
             "A <b>keyspace</b> is like a database; it sets replication (<code>SimpleStrategy</code>, factor 1 for one node).",
             "A <b>table</b> needs a <b>primary key</b> (here <code>userid</code>), which decides which node stores the row.",
             "<b>CQL</b> looks like SQL: INSERT, SELECT, UPDATE, DELETE. <code>toTimestamp(now())</code> stores the current time.",
             "UPDATE and DELETE must use the primary key in the WHERE clause.",
         ],
         src=["commands.sh", "cart.cql"],
         run=["Install Docker Desktop and start it.",
              "<code>docker run -d --name cassandralab cassandra:latest</code> (wait about 1 minute).",
              "<code>docker exec -it cassandralab cqlsh</code>",
              "Type or paste the commands from cart.cql.",
              "Clean up: <code>docker rm -f cassandralab</code>"],
         out="expected_output.txt", badge="Expected (Docker daemon was not running)"),
    dict(id="exp11", title="Exp 11 · Node.js Web Page on EC2", dir="exp11_nodejs",
         aim="To create a web page with Node.js and host it on an Ubuntu EC2 instance.",
         theory=[
             "<b>Node.js</b> runs JavaScript on the server; it is event-driven and non-blocking.",
             "The built-in <code>http</code> module creates a web server with <code>http.createServer()</code>.",
             "For every request the callback sets status 200 and <code>Content-Type: text/html</code> with <code>res.writeHead()</code>, then sends HTML with <code>res.end()</code>.",
             "<code>server.listen(3000, '0.0.0.0')</code> listens on port 3000 on all network interfaces, so it is reachable from outside.",
             "On EC2 we launch an <b>Ubuntu</b> instance, SSH into it, install nodejs and run <code>node app.js</code>.",
             "The security group must allow inbound <b>TCP 3000</b>; open <code>http://PUBLIC-IP:3000</code>.",
         ],
         src=["app.js", "commands.sh"],
         run=["Local test: install Node.js, then <code>node app.js</code> and open <code>http://localhost:3000</code>.",
              "EC2: Launch an <b>Ubuntu</b> instance (t2.micro), create a key pair, allow SSH (22) and Custom TCP <b>3000</b>.",
              "<code>ssh -i key.pem ubuntu@PUBLIC-IP</code>",
              "Run the commands in commands.sh (install nodejs, create app.js, <code>node app.js</code>).",
              "Browser: <code>http://PUBLIC-IP:3000</code>"],
         out="output.txt", badge="Ran locally (Node 22) - EC2 part not run"),
    dict(id="exp12", title="Exp 12 · Google Cloud Bigtable", dir="exp12_bigtable",
         aim="To create a Google Cloud Bigtable instance and table, and insert, read and delete data using cbt.",
         theory=[
             "<b>Cloud Bigtable</b> is Google's fully managed, wide-column <b>NoSQL</b> database for huge, low-latency workloads (IoT, analytics).",
             "Data model: <b>table → row key → column family → column qualifier → value</b>, every cell has a timestamp.",
             "An <b>instance</b> holds one or more <b>clusters</b> (nodes in a zone) that store the tables.",
             "<code>gcloud</code> (Cloud SDK) creates the project setup and instance; <b>cbt</b> is the Bigtable command-line tool for tables and data.",
             "<code>~/.cbtrc</code> stores the project and instance so cbt commands stay short.",
             "Commands: <code>createtable</code>, <code>createfamily</code>, <code>set</code> (insert), <code>read</code>, <code>deleterow</code>, <code>deletetable</code>.",
         ],
         src=["bigtable.sh"],
         run=["Create a Google Cloud project (billing / free trial enabled) and note its <b>Project ID</b>.",
              "Install the Google Cloud SDK, or simply open <b>Cloud Shell</b> in the console (gcloud is ready there).",
              "Run the commands in bigtable.sh one by one (replace YOUR_PROJECT_ID).",
              "Delete the instance after the lab: <code>gcloud bigtable instances delete my-instance</code>"],
         out="expected_output.txt", badge="Expected (cloud step, not run here)"),
]


def build_dscc():
    progs = []
    for e in DSCC:
        p = {k: v for k, v in e.items() if k not in ("dir", "src", "out", "badge", "theory")}
        p["files"] = files(*[f"DSCC/{e['dir']}/{f}" for f in e["src"]])
        p["output"] = {"text": read(f"DSCC/{e['dir']}/{e['out']}"), "badge": e["badge"]}
        progs.append(p)
    return progs


# ---------------------------------------------------------------------- DL
DL_RUN = ["Install Python 3.10+, then <code>pip install tensorflow</code>.",
          None,
          "First run downloads the dataset automatically (internet needed)."]
DL = [
    dict(id="cnn", title="CNN · MNIST Digits",
         aim="To build a Convolutional Neural Network in Keras that classifies handwritten digits (MNIST).",
         theory=[
             "A <b>CNN</b> is a deep network made for images; it learns features (edges → shapes → digits) automatically.",
             "<b>Conv2D</b> slides small 3×3 filters over the image to make feature maps; <b>ReLU</b> adds non-linearity.",
             "<b>MaxPooling2D</b> halves the size of each map, keeping the strongest values and reducing computation.",
             "<b>Flatten</b> turns the maps into a vector; <b>Dense</b> layers classify; <b>softmax</b> gives the probability of each of the 10 digits.",
             "Data: 60,000 train + 10,000 test grey images (28×28), pixels scaled to 0–1. Loss = sparse categorical cross-entropy, optimizer = Adam.",
             "After only 2 epochs the test accuracy is about <b>98%</b>.",
         ]),
    dict(id="rnn", title="RNN · IMDB Sentiment",
         aim="To build a simple Recurrent Neural Network in Keras that classifies IMDB movie reviews as positive or negative.",
         theory=[
             "An <b>RNN</b> reads a sequence one step (word) at a time and keeps a <b>hidden state</b> that remembers earlier words.",
             "IMDB: 50,000 reviews labelled 1 (positive) or 0 (negative); words are already integers. We keep the top 10,000 words.",
             "<code>pad_sequences</code> makes every review exactly 200 words (cut long ones, pad short ones with 0).",
             "<b>Embedding</b> turns each word number into a 32-value vector that captures meaning.",
             "<b>SimpleRNN(32)</b> processes the vectors; <b>Dense(1, sigmoid)</b> outputs the probability of a positive review. Loss = binary cross-entropy.",
             "Accuracy is about <b>83%</b>. Simple RNNs suffer from the <b>vanishing gradient</b> problem and forget long-range context, which LSTM fixes.",
         ]),
    dict(id="lstm", title="LSTM · IMDB Sentiment",
         aim="To build a Long Short-Term Memory (LSTM) network in Keras for IMDB movie review sentiment classification.",
         theory=[
             "<b>LSTM</b> is a special RNN that remembers long-term information using a <b>cell state</b>, solving the vanishing gradient problem.",
             "It has three <b>gates</b>: <b>forget gate</b> (what to erase), <b>input gate</b> (what new info to store), <b>output gate</b> (what to output).",
             "Same data pipeline as the RNN: top 10,000 words, reviews padded to 200, Embedding of size 32.",
             "<b>LSTM(32)</b> replaces SimpleRNN; it has 4× the parameters (8,320 vs 2,080) because of the gates.",
             "<b>Dense(1, sigmoid)</b> gives positive/negative; loss = binary cross-entropy, optimizer = Adam.",
             "It reaches about <b>87%</b> test accuracy in just 2 epochs, better than the simple RNN.",
         ]),
    dict(id="gan", title="GAN · Generate MNIST Digits",
         aim="To build a simple Generative Adversarial Network in Keras that generates handwritten-digit images from random noise.",
         theory=[
             "A <b>GAN</b> has two networks: the <b>Generator (G)</b> makes fake images from random noise, the <b>Discriminator (D)</b> says real (1) or fake (0).",
             "They are trained against each other (a min-max game): G tries to fool D, D tries to catch G. Over time G's images look real.",
             "G: noise(64) → Dense 128 ReLU → Dense 784 <b>tanh</b> (a 28×28 image in −1…1). D: 784 → Dense 128 ReLU → Dense 1 <b>sigmoid</b>.",
             "Step 1 – train D on a batch of real images (label 1) and G's fake images (label 0).",
             "Step 2 – freeze D (<code>D.trainable = False</code>) and train the combined model G→D with label 1, so only G learns to fool D.",
             "Trained for 5,000 steps on 10,000 MNIST images; the output shows the losses and one generated digit as text art (<code>#</code> = bright pixel). Losses going up and down is normal for GANs.",
         ]),
]


def build_dl():
    progs = []
    for d in DL:
        p = {k: v for k, v in d.items() if k != "theory"}
        p["files"] = files(f"DL/{d['id']}.py")
        run = list(DL_RUN)
        run[1] = f"<code>python {d['id']}.py</code> (takes under a minute on a laptop CPU)."
        p["run"] = run
        p["output"] = {"text": strip_ansi(read(f"DL/outputs/{d['id']}.txt")),
                       "badge": "Ran locally (TensorFlow 2.21, CPU)"}
        progs.append(p)
    return progs


# -------------------------------------------------------------------- page
SUBJECTS = [
    {"id": "mad", "name": "MAD", "full": "Mobile Application Development",
     "intro": "Android programs in Java. Each set has the theory answer and one file: MainActivity.java. No XML needed.",
     "procedure": MAD_PROCEDURE, "programs": build_mad()},
    {"id": "dscc", "name": "DSCC", "full": "Distributed Systems & Cloud Computing",
     "intro": "Experiments 6–12: aim, program/commands, how to run and output.",
     "programs": build_dscc()},
    {"id": "dl", "name": "DL", "full": "Deep Learning",
     "intro": "Keras programs: CNN, RNN, LSTM and GAN. Each runs in under a minute on a CPU.",
     "programs": build_dl()},
]

PRISM = "https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/"
PRISM_LANGS = ["core", "clike", "markup", "javascript", "java", "python", "sql", "bash"]

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Lab Programs</title>
<meta name="description" content="Short exam-ready lab programs for MAD, DSCC and DL with theory, code and output.">
<link rel="stylesheet" href="style.css?v=__V__">
<script>try { if (localStorage.getItem("theme") === "light") document.documentElement.dataset.theme = "light"; } catch (e) {}</script>
</head>
<body>
<header class="top">
  <div class="brand">Lab Programs</div>
  <nav class="tabs" id="tabs" role="tablist"></nav>
  <div class="top-right">
    <button class="icon-btn" id="themeBtn" type="button" aria-label="Switch light/dark theme">☀️ Light</button>
    <button class="menu-btn" id="menuBtn" aria-label="Show program list">☰ Programs</button>
  </div>
</header>
<div class="layout">
  <aside class="side" id="side"></aside>
  <main class="main" id="main"></main>
</div>
<script id="data" type="application/json">__DATA__</script>
<script>window.Prism = { manual: true };</script>
__PRISM__
<script src="site.js?v=__V__"></script>
</body>
</html>
"""


def main():
    data = json.dumps(SUBJECTS, ensure_ascii=False).replace("</", "<\\/")
    prism = "\n".join(f'<script src="{PRISM}prism-{l}.min.js" defer></script>' for l in PRISM_LANGS)
    prism = prism.replace(" defer", "")
    import hashlib
    v = hashlib.md5((ROOT / "site.js").read_bytes() + (ROOT / "style.css").read_bytes()).hexdigest()[:8]
    html = TEMPLATE.replace("__DATA__", data).replace("__PRISM__", prism).replace("__V__", v)
    (ROOT / "index.html").write_text(html, encoding="utf-8")
    n = sum(len(s["programs"]) for s in SUBJECTS)
    print(f"index.html written: {n} programs, {len(html) // 1024} KB")


if __name__ == "__main__":
    main()
