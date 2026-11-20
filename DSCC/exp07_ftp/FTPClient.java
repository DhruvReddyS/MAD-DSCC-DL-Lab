import java.io.*;
import java.net.*;
import java.util.*;

public class FTPClient {
    public static void main(String[] args) throws Exception {
        Socket s = new Socket("localhost", 5000);
        BufferedReader in = new BufferedReader(new InputStreamReader(s.getInputStream()));
        PrintWriter out = new PrintWriter(s.getOutputStream(), true);

        System.out.print("Enter File Name: ");
        out.println(new Scanner(System.in).nextLine());

        if ("FOUND".equals(in.readLine())) {
            System.out.println("File Contents:");
            String line;
            while ((line = in.readLine()) != null)
                System.out.println(line);
        } else {
            System.out.println("File Not Found");
        }
        s.close();
    }
}
