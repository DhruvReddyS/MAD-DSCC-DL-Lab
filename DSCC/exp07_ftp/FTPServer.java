import java.io.*;
import java.net.*;

public class FTPServer {
    public static void main(String[] args) throws Exception {
        ServerSocket ss = new ServerSocket(5000);
        System.out.println("Server Started...");
        Socket s = ss.accept();

        BufferedReader in = new BufferedReader(new InputStreamReader(s.getInputStream()));
        PrintWriter out = new PrintWriter(s.getOutputStream(), true);

        File file = new File(in.readLine());
        if (file.isFile()) {
            out.println("FOUND");
            BufferedReader fr = new BufferedReader(new FileReader(file));
            String line;
            while ((line = fr.readLine()) != null)
                out.println(line);
            fr.close();
        } else {
            out.println("NOTFOUND");
        }
        s.close();
        ss.close();
    }
}
