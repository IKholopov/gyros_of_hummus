package sample;

import java.util.List;


/**
 * Created by valeriyasin on 11/26/16.
 */
public class Gyro {
    private List<Position> route;
    private double speed;


    public List<Position> getRoute() {
        return route;
    }

    public void setRoute(List<Position> route) {
        this.route = route;
    }

    public double getSpeed() {
        return speed;
    }

    public void setSpeed(double speed) {
        this.speed = speed;
    }
}
