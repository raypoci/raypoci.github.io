//Author: Reimond Poci 
//BU ID: U18561315

import java.util.*;

//creates an event object
class Event {

	//each event object contains a type {BIRTH,DEATH,MONITOR} and execution time
	String type;
	double execution_time;

	//class constructor
	public Event(String type, double execution_time){
		this.type=type;
		this.execution_time=execution_time;
	}
	//returns the execution time of object
	public double get_execution_time(){
		return this.execution_time;
	}

	//generates an exponentially distributed rate
	public static double exp(double lambda){

		Random RandomRun = new Random();
		double RandomVal = RandomRun.nextDouble();

		//return a random variable that follows exponential distribution
		return (-Math.log(1 - RandomVal))/lambda;
}
	//generates an exponentially distributed rate of service
	public static double generate_time_death(){
		return exp(1/simulatorKN.service_time);
	}
	//generates an exponentially distributed rate of arrivals
	public static double generate_time_event(){
		return exp(simulatorKN.arrival_rate);
	}
}

class EventComparator implements Comparator<Event>{
	//overrides Comparator compare so that we keep Priority Queue sorted by execution time
	public int compare(Event event1, Event event2){
		double time = event1.get_execution_time() - event2.get_execution_time();
		if (time>0){
			return 1;
		}
		else if (time<0){return -1;}
		else return 0;
	}


}

//controller class which practically dictates the state of the simulation at each event
public class Controller{
	private static Request request_server[];
	
	//global constant to keep track on total # of requests
	public static int request_id=0;
	
	//sets id of new request to current request_id and increments request_id by 1
	public static int set_request_id(){
        int birth_id=request_id;
        request_id++;
        return birth_id;
    }
	//initializes scheduke
	public static PriorityQueue<Event> initializeSchedule(){
		//we use Priority Queue to keep events sorted by execution time
		PriorityQueue<Event> schedule = new PriorityQueue<Event>(new EventComparator());
		
		//initiate the new schedule with a birth event and a monitor event
		Event first_event = new Event("BIRTH", Event.generate_time_event());
		schedule.add(first_event);

		Event first_monitor = new Event("MONITOR", Event.generate_time_event());
		schedule.add(first_monitor);

		return schedule;

	}

	public static void simulation(double simulation_len, double arrival_rate, double service_time, int total_servers){
		//initiate state of the system
		State state = new State();
		//initiate schedule for simulation
		PriorityQueue<Event> schedule = initializeSchedule();

		double time = 0;
		//run for the duration of simulation_len
		while (time<simulation_len){
			//begin processing the first event in the schedule
			Event event = schedule.remove();
			time = event.get_execution_time();

			//this function is responsible for executing each event
			//takes as parameters state, schedule, execution time of the event and event itself
			execute_event(state, schedule, time, event);
		}

		for (int i = 0; i < total_servers; i++) {
            System.out.println("UTIL" + i + ": " + state.server_time_served[i] / simulation_len);
        }
		//At the end of while loop we print avg.length of queue, avg.response time, dropped requests
		System.out.println("QLEN: "+ (state.length / state.monitor));
		System.out.println("TRESP: "+ (state.response_time / state.serviced_request));
		System.out.println("DROPPED: " + state.dropped_request);
   
	}

	public static void execute_event(State state, PriorityQueue<Event> schedule, double time, Event event){
		request_server = new Request[simulatorKN.total_servers];
		//if we have a birth event
		if (event.type == "BIRTH"){

			//set the request id and add it to queue
			int req_id = set_request_id();
			Request req = new Request(req_id);
			

			//set arrival time of request as current time
			req.set_arrival(time);
	
			if (state.request_queue.size() == simulatorKN.queue_len){
				state.dropped_request+=1;
				System.out.println("R" + req.id + " DROP: " + time);
			}

			else
			{
				state.request_queue.add(req);
				System.out.println("R" + Integer.toString(req.id) + " ARR: " + time);
			

			//if this request is the only one in the queue
				if (state.request_queue.size()<= simulatorKN.total_servers){
					int next_server= state.next_server();
				
					state.num_busy_servers+=1;
					state.set_busy(next_server);
					req.set_server(next_server);
					//print out service time
					System.out.println("R" + Integer.toString(req.id) + " START: " + req.server_id + ": "+ time);
					//begin servicing request and set service time to current time
				
					req.set_begin_service(time);
				

					//generate a death event by generating an exponentially distributed death time
					double next_death_time = time + event.generate_time_death();
					
					Event death_event = new Event("DEATH", next_death_time);
					//add death event to schedule
					schedule.add(death_event);

			}}
			//regardless of length of queue we schedule next birth event
			//next event is generated by an exponentially distributed IAT
		
			double next_birth_time = time + event.generate_time_event();
			
			Event next_birth = new Event("BIRTH", next_birth_time);
			//add birth event to schedule
			schedule.add(next_birth);
		
	}
		//if event is a death event
		else if (event.type == "DEATH"){
			//we remove the request from queue since its scheduled to "die"
			Request req = state.request_queue.remove();

			//record end of service time
			req.set_end_service(time);
			//print out time the request finished being served
			System.out.println("R" + req.id + " DONE: " + req.server_id + ": "+req.end_service);
			
			//increase number of requests that finished service by 1
			state.serviced_request += 1;
			
			//increase the total service time of the system by the service time of the request
			double service_time = req.service_time();
			state.service_time+= service_time;
			state.server_time_served[req.server_id]+= service_time;
			
			//increase total response time of system by response time of the request
			double response_time = req.response_time();
			state.response_time += response_time;

			state.num_busy_servers-=1;
			state.set_idle(req.server_id);

			//if there are still requests in the queue
			
			if (state.request_queue.size()>state.num_busy_servers){
				
				for(int i=0; i<state.num_busy_servers; i++){
					request_server[i]= state.request_queue.remove();
					
				}
				//we can set the service time of the next request to be dequeued without removing it
				Request next = state.request_queue.peek();
				
				next.set_begin_service(time);
				
				next.set_server(req.server_id);
				state.set_busy(req.server_id);
				
				for(int j=0; j<state.num_busy_servers; j++){
					Request request = request_server[j];
					state.request_queue.addFirst(request);
				}


				state.num_busy_servers+=1;

				//print out the start of service time of next request
				System.out.println("R" + Integer.toString(next.id) + " START: " + req.server_id + ": "+ next.begin_service);

				//schedule the next death event and add to schedule
				double next_death_time= time + event.generate_time_death();
				Event next_death = new Event("DEATH", next_death_time);
				schedule.add(next_death);


			}

		}
		//monitor event records the state of the system
		else if (event.type=="MONITOR"){

			//generate the next monitor event just like we would a birth event
			double monitor_time = time + event.generate_time_event();
			Event next_monitor = new Event("MONITOR", monitor_time);
			schedule.add(next_monitor);
			
			//increase the total number of requests that have been in the system by current size of queue
			state.length += state.request_queue.size();

			//add 1 to the number of monitor events
			state.monitor +=1;
			



		}


	} 
}





