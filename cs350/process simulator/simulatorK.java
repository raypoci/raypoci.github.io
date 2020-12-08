//Author: Reimond Poci 
//BU ID: U18561315

public class simulatorK{
    static double arrival_rate;
    static double service_time;
    static int queue_len; 
    static int total_servers=1;
    public static void simulateK(double simulation_len){
        //runs simulation through Controller class
        ControllerK.simulation(simulation_len, arrival_rate, service_time, 1);
    }

    public static void main(String args[]){

        //5 inputs from calling environment
        //time to run simulation, lamda, Ts, K, N
        double simulation_len= Double.parseDouble(args[0]);
        arrival_rate= Double.parseDouble(args[1]);
        service_time= Double.parseDouble(args[2]);
        queue_len= Integer.parseInt(args[3]);
        simulateK(simulation_len);
    }
}