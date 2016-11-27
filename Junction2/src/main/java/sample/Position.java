package sample;

import javafx.geometry.Pos;

/**
 * Created by valeriyasin on 11/26/16.
 */
public class Position {
    private Double x;
    private Double y;
    private int floor;

    Position(double x, double y, int floor) {
        this.x = x;
        this.y = y;
        this.floor = floor;
    }

    public final static Double calculateDistance(Position a) {
        return Math.sqrt((a.getY()) * (a.getY()) +
                (a.getX()) * (a.getX()));
    }

    public final static Position subtract(Position a, Position b) {
//        if (a.getFloor() != b.getFloor()) {
//            System.out.println("can't subtract\n");
//        }
        Position ret = new Position(a.getX() - b.getX(), a.getY() - b.getY(), a.getFloor());
        ret.setFloor(a.getFloor());
        return ret;
    }

    public final static Position mult(Position a, double m) {
        return new Position(a.getX() * m, a.getY() * m, a.getFloor());
    }

    public final static Position sum(Position a, Position b) {
        return new Position(a.getX() + b.getX(), a.getY() + b.getY(), a.getFloor());
    }

    public final static Position divide(Position a, double m) {
        return new Position(a.getX() / m, a.getY() / m, a.getFloor());
    }

    public Double getX() {
        return x;
    }

    public void setX(Double x) {
        this.x = x;
    }

    public Double getY() {
        return y;
    }

    public void setY(Double y) {
        this.y = y;
    }

    public int getFloor() {
        return floor;
    }

    public void setFloor(int floor) {
        this.floor = floor;
    }
}
