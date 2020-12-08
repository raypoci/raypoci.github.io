//Author: Reimond Poci 
//BU ID: U18561315

public class simulatorKN{
    static double arrival_rate;
    static double service_time;
    static int queue_len; 
    static int total_servers;
    public static void simulate(double simulation_len){
        //runs simulation through Controller class
        Controller.simulation(simulation_len, arrival_rate, service_time, total_servers);
    }

    public static void main(String args[]){

        //5 inputs from calling environment
        //time to run simulation, lamda, Ts, K, N
        double simulation_len= Double.parseDouble(args[0]);
        arrival_rate= Double.parseDouble(args[1]);
        service_time= Double.parseDouble(args[2]);
        queue_len= Integer.parseInt(args[3]);
        total_servers= Integer.parseInt(args[4]);
        simulate(simulation_len);
    }
}