import java.io.*;
import java.net.*;
import java.nio.file.*;

public class FTPServer {
    public static void main(String[] args) throws Exception {
        ServerSocket ss = new ServerSocket(5050);
        System.out.println("Server started on port 5050...");
        Socket s = ss.accept();                          // wait for a client
        BufferedReader in = new BufferedReader(new InputStreamReader(s.getInputStream()));
        PrintWriter out = new PrintWriter(s.getOutputStream(), true);

        String name = in.readLine();                     // file name from client
        System.out.println("Client requested: " + name);
        File f = new File(name);
        if (f.isFile()) {
            out.println("FOUND");
            for (String line : Files.readAllLines(f.toPath())) out.println(line);
        } else {
            out.println("NOTFOUND");
        }
        s.close();
        ss.close();
    }
}
