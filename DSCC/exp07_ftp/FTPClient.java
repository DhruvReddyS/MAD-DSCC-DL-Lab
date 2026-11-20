import java.io.*;
import java.net.*;
import java.util.Scanner;

public class FTPClient {
    public static void main(String[] args) throws Exception {
        Socket s = new Socket("localhost", 5050);
        BufferedReader in = new BufferedReader(new InputStreamReader(s.getInputStream()));
        PrintWriter out = new PrintWriter(s.getOutputStream(), true);

        System.out.print("Enter file name: ");
        out.println(new Scanner(System.in).nextLine());  // send file name
        if ("FOUND".equals(in.readLine())) {
            System.out.println("File contents:");
            String line;
            while ((line = in.readLine()) != null) System.out.println(line);
        } else {
            System.out.println("File not found");
        }
        s.close();
    }
}
