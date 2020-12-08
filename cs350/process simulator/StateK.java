//Author: Reimond Poci 
//BU ID: U18561315

import java.util.*;

//represents the system queue and some performance metrics
public class StateK{

    //queue
    public LinkedList<RequestK> request_queue;
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

    //class constructor initializes everything 
    public StateK(){
        request_queue= new LinkedList<RequestK>();
        id=0;
        serviced_request=0;
        length=0;
        monitor=0;
        service_time=0;
        response_time=0;
        dropped_request=0;


    } 

    //sets the id of each request by returning current id and adding 1 to global constant
    public int set_request_id(){
        int birth_id=id;
        id++;
        return birth_id;
    }

}