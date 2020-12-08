import java.math.BigInteger;
import java.util.*;


public class UnHash {
  static HashMap<String, String> hashed = new HashMap<String, String>();
  static String add = Hash.hash("add");
  static String div = Hash.hash("div");
  static String mul = Hash.hash("mul");

    public static String unhash(String to_unhash) {
      String input;
      
      if (!hashed.containsKey(to_unhash)){

        
        if (add.equals(to_unhash)){
       
          hashed.put(add, "add");
         return "add";
         }else if(div.equals(to_unhash)){
         
          hashed.put(div, "div");
         return "div";
         } else if(mul.equals(to_unhash)){
      
          hashed.put(mul, "mul");
         return "mul";
         } 
    /* if we are here, the input is not mul,add, or div, it is a number*/
     for(int i =1; ; i++){
      input = Integer.toString(i);
      if (!hashed.containsValue(input)){
        input = Hash.hash(input);
        hashed.put(input, Integer.toString(i));
        if(input.equals(to_unhash)){
         
          return input;
      }}
     }
   }
   else{
     return hashed.get(to_unhash);}}


}
