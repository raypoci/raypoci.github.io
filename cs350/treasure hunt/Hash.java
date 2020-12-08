import java.math.BigInteger;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

public class Hash {
    public static String hash(String input) {
        try {

            // Convert integer to string
            //String strValue = Integer.toString(input);
             String strValue = input; 

            // Static getInstance method is called with hashing MD5
            MessageDigest md = MessageDigest.getInstance("MD5");

            // digest() method is called to calculate message digest
            //  of an input digest() return array of byte
            byte[] messageDigest = md.digest(strValue.getBytes());

            // Convert byte array into signum representation
            BigInteger no = new BigInteger(1, messageDigest);

            // Convert message digest into hex value
            String hashtext = no.toString(16);
            while (hashtext.length() < 32) {
                hashtext = "0" + hashtext;
            }
            return hashtext;
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException(e);
        }
    }


public static void main(String[] args) {
       // int k0 = Integer.parseInt(args[0]);
          String  input=  args[0];
           String hash = Hash.hash(input);
          System.out.println(hash);
       // Treasure t = new Treasure(args[1]);
     //    System.out.println(UnHash.unhash(hash));
    }

}
