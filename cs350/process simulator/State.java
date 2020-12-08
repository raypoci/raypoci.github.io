//Author: Reimond Poci 
//BU ID: U18561315

import java.util.*;

//represents the system queue and some performance metrics
public class State{

    //queue
    public LinkedList<Request> request_queue;
    //global constant to keep track of number of requests in system
    static int id;
    //total number of requests serviced so far
    double serviced_request;
    //total number of requests that have been 'monitored' in the queue
    double length;
    //total number of monitor events
    double monitor;
    //total service time of all requests
    double service_time;
    //total response time of all requests
    double response_time;

    int dropped_request;
    int num_busy_servers;
    int[] busy_servers;
    double[] server_time_served;

    //class constructor initializes everything 
    public State(){
        request_queue= new LinkedList<Request>();
        id=0;
        serviced_request=0;
        length=0;
        monitor=0;
        service_time=0;
        response_time=0;
        dropped_request=0;
        num_busy_servers=0;
        busy_servers= new int[simulatorKN.total_servers];
        server_time_served = new double[simulatorKN.total_servers];

    } 

    //sets the id of each request by returning current id and adding 1 to global constant
    public int set_request_id(){
        int birth_id=id;
        id++;
        return birth_id;
    }

    public int next_server(){
        Random rand = new Random();
        int index = 0;
        List<Integer> choices = new ArrayList<Integer>();
        int num_servers = simulatorKN.total_servers;
        for (int i=0; i<num_servers; i++){
            if (busy_servers[i]==0){
                choices.add(i);
            }
        }
        int rand_choice = rand.nextInt(choices.size());
        index = choices.get(rand_choice);
        return index;

    }
    public void set_busy(int index){
        busy_servers[index]= 1;
    }
    public void set_idle(int index){
        busy_servers[index]=0;
    }
}