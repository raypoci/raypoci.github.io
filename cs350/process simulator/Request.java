//Author: Reimond Poci 
//BU ID: U18561315

//class to structure requests
public class Request{
    // each request has id, rate of arrival,
    // time when it began service and time when it finished
    int id;
    double arrival;
    double begin_service;
    double end_service;
    int server_id;

    //class constructor
    public Request(int id){
        this.id = id;
        this.begin_service=-1;
        this.end_service=-1;
        this.server_id=-1;

    }

    public void set_server(int id){
        this.server_id=id;
    }
    //sets value for arrival time 
    public void set_arrival(double arrival){
        this.arrival = arrival; 
    }

    //sets value for begin of service time
    public void set_begin_service(double begin_service){
        this.begin_service = begin_service; 
    }
    //sets value for end of service time
    public void set_end_service(double end_service){
        this.end_service = end_service; 
    }
    //calculates time spent being serviced
    public double service_time(){
        return end_service - begin_service;
    }
    //calculates turnaround time spent in system
    public double response_time(){

        return end_service - arrival;
    }
}
