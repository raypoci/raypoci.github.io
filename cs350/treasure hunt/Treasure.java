import java.io.BufferedReader;
import java.io.FileReader;
import java.util.*;
import java.util.concurrent.Semaphore;

public class Treasure extends Thread{

    private int id;
    static int N;
    //static volatile Semaphore mutex = new Semaphore(1, false);
    static Map<Integer, Integer> visited = new HashMap<Integer, Integer>();
    static LinkedList<Integer> queue= new LinkedList<Integer>();
    static HashMap<String, String> hashed = new HashMap<String, String>();

    static volatile Semaphore mutex = new Semaphore(1, false);
    static int size;
    static String file;
    static Treasure treasure[];
    static boolean done[];

    public Treasure(int i) {
        id = i;
    }

    public void run () {
        int next1 = 0;
        int offset1 = 0;
        String next2 = "";
            
            

            try{
                

                while (queue.size() !=0 && done[this.id]==false) {
                mutex.acquire();
                
                if (size>0 && done[this.id]==false){
                int node = queue.poll();
                size--;
                visited.put(node,1);
                mutex.release();
            

                next1 = Integer.parseInt(hashed.get((file.substring(node, node+32))));
                next2 = hashed.get((file.substring(node+32, node+64)));
                if(next1>=file.length()){
                    if (next1 % 2==1){
                        if(done[this.id]==false){
                            mutex.acquire();
                            size=0;
                            
                            System.out.println(next1); 
                            for (int i=0; i<N; i++){
                                done[i]=true;
                            }
                        mutex.release();
                        return;}}
                }
                else{

                    if (!visited.containsKey(next1)){
                        mutex.acquire(); 
                        queue.add(next1); 
                        size++; 
                        mutex.release();}
                  }

               
                if (next2.equals("add")) {
                    offset1 = next1 + next1 ;
                    if (!visited.containsKey(offset1)){
                        mutex.acquire();
                        queue.add(offset1);
                        size++;
                        mutex.release();
                    }}
                
                else if (next2.equals("div")) {
                    offset1 = next1 / 3 ;
                    if (!visited.containsKey(offset1)){
                        mutex.acquire();
                        queue.add(offset1);
                        size++;
                        mutex.release();
                    }}
               
                else if (next2.equals("mul")) {
                    offset1 = next1 * 3 ;
                    if (!visited.containsKey(offset1)){ 
                        mutex.acquire();
                        queue.add(offset1);
                        size++;
                        mutex.release();
                    }}
                
                else{     
                    offset1 = Integer.parseInt(next2);
                    if(offset1>=file.length()-1){
                        if (offset1%2==1){
                            if(done[this.id]==false){
                                mutex.acquire();
                                size=0;
                                System.out.println(offset1); 
                                for (int i=0; i<N; i++){
                                    done[i]=true;
                        }
                        mutex.release();
                        return;}}}
                    else{
                        if (!visited.containsKey(offset1)){ 
                            mutex.acquire();
                            queue.add(offset1);
                            size++;
                            mutex.release();}

                    }}
                    
            }else{mutex.release();}}}

        catch (InterruptedException e){Thread.currentThread().interrupt();}
        

       

        
    } 
    

    public static void main(String[] args) {
        int k0 = Integer.parseInt(args[0]);
        String fileName = args[1];
        N = Integer.parseInt(args[2]);

        treasure = new Treasure[N];

        done = new boolean[N];

        queue.add(k0);
        size=1;

        try {
            BufferedReader bf = new BufferedReader(new FileReader(fileName));
            StringBuilder buildFile = new StringBuilder();
            String readline = bf.readLine();
            while (readline != null) {
                buildFile.append(readline);
                readline = bf.readLine();
            }

            file = buildFile.toString();
           
        
        } catch (Exception e) {
            e.printStackTrace(System.out);
        }

        hashed.put(Hash.hash("add"), "add");
        hashed.put(Hash.hash("mul"), "mul");
        hashed.put(Hash.hash("div"), "div");

        for (int j=1; j<=2*file.length(); j++){
            hashed.put(Hash.hash(Integer.toString(j)), Integer.toString(j));
        }


        for (int i=0; i<N; i++){
            treasure[i]= new Treasure(i);
            done[i]=false;
            treasure[i].start();
        }

    }
}

