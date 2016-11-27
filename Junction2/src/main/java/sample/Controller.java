package sample;

import javafx.geometry.Pos;
import javafx.scene.control.Button;

import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.IOException;
import java.net.URL;
import java.util.LinkedList;
import java.util.List;
import java.util.Random;
import java.util.ResourceBundle;
import java.util.concurrent.Callable;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.ScheduledFuture;
import java.util.concurrent.SynchronousQueue;

import javax.imageio.ImageIO;

import javafx.embed.swing.SwingFXUtils;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.canvas.*;
import javafx.scene.canvas.Canvas;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.layout.GridPane;
import javafx.scene.layout.StackPane;
import javafx.scene.paint.Color;
import javafx.scene.transform.Rotate;

import static java.util.concurrent.TimeUnit.MICROSECONDS;
import static java.util.concurrent.TimeUnit.MILLISECONDS;
import static java.util.concurrent.TimeUnit.SECONDS;

public class Controller implements Initializable {

    private final int TICKS_IN_PERIOD = 30;
    private final int MILLISECONDS_IN_TICK = 100;
    private final double EPS = 1e-6;

    private final ScheduledExecutorService DrawScheduler =
            Executors.newScheduledThreadPool(1);

    private final ScheduledExecutorService RequestScheduler =
            Executors.newScheduledThreadPool(1);
//
//    @FXML
//    private GridPane root;

//    @FXML
//    private Canvas canvas;

    @FXML
    private StackPane stackPane;

    @FXML
    private ImageView map;

    @FXML
    private Button first;
    @FXML
    private Button second;
    @FXML
    private Button third;

    @FXML
    public Button eventFier;

    @FXML
    private Canvas canvas;

    private GraphicsContext gc;

    private EventHandler<ActionEvent> changeFloor;

    private int level;

//     (60.484351, 15.417935)(60.484129, 15.418381),


//    393.5325 - x1
//            220.91250000000002 - y1
//            484.98 - y1
//            314.415 - y2


    private int ticks;
    private List<Gyro> curList;

    private Image mapImage;
    private Image gyro;

    Position check2;


    URL imageUrl;

    private Position translateCoordinates(Position posGeo) {

        Double scaleX = (393.5325 - 484.98) / (15.417935 - 15.418381);
        Double scaleY = (220.91250000000002 - 314.415) / (60.484351 - 60.484129);
        Double moduleScale = Position.calculateDistance(new Position(scaleX, scaleY, 0));

        Position startGeo;
        Position startPix;

        startGeo = new Position(15.417935, 60.484351 , 0);
        startPix = new Position(393.5325, 220.91250000000002, 0);
        Position vector = Position.subtract(posGeo, startGeo);
        return Position.sum(startPix, new Position(vector.getX() * scaleX, vector.getY() * scaleY, 0));
    }




    public void initialize(URL fxmlFileLocation, ResourceBundle resources) {


        Position check1 = new Position(15.417935,60.484351, 0);
        check2 = translateCoordinates(check1);
//        mockCurList();
        gc = canvas.getGraphicsContext2D();
        eventFier.setVisible(false);
        imageUrl = getClass().getResource("/1.jpg");
        try {
            Image image = SwingFXUtils.toFXImage(ImageIO.read(imageUrl), null);
            map.setImage(image);
            mapImage = image;
        } catch (IOException ex) {
            ex.printStackTrace();
        }
        level = 0;
        ticks = 0;

        imageUrl = getClass().getResource("/gyro.png");
        try {
            gyro = SwingFXUtils.toFXImage(ImageIO.read(imageUrl), null);
        } catch (IOException ex) {
            ex.printStackTrace();
        }

        final ScheduledFuture<?> drawHandler =
                DrawScheduler.scheduleAtFixedRate(new RunnableDrawer(), 0, 100, MILLISECONDS);

        final ScheduledFuture<?> requestHandler =
                RequestScheduler.scheduleAtFixedRate(new RunnableRequester(), 0, 3, SECONDS);

        changeFloor  = new EventHandler<ActionEvent>() {
            public void handle(final javafx.event.ActionEvent event) {
                Button button = (Button)event.getTarget();
                GraphicsContext gc = canvas.getGraphicsContext2D();
                switch (button.getId()) {
                    case "first":
                        imageUrl = getClass().getResource("/1.jpg");
                        try {
                            Image image = SwingFXUtils.toFXImage(ImageIO.read(imageUrl), null);
                            map.setImage(image);
                            mapImage = image;
                            level = 0;
//                            DrawScheduler.scheduleAtFixedRate(new RunnableDrawer(), 0, 100, MILLISECONDS);
//                            gc.clearRect(0, 0, canvas.getWidth(), canvas.getHeight());
                        } catch (IOException ex) {
                            ex.printStackTrace();
                        }
                        break;
                    case "second":
                        imageUrl = getClass().getResource("/2.jpg");
                        try {
                            Image image = SwingFXUtils.toFXImage(ImageIO.read(imageUrl), null);
                            map.setImage(image);
                            mapImage = image;
                            level = 1;
//                            DrawScheduler.scheduleAtFixedRate(new RunnableDrawer(), 0, 100, MILLISECONDS);
//                            gc.clearRect(0, 0, canvas.getWidth(), canvas.getHeight());
                        } catch (IOException ex) {
                            ex.printStackTrace();
                        }
                        break;
                    case "third":
                        imageUrl = getClass().getResource("/3.jpg");
                        try {
                            Image image = SwingFXUtils.toFXImage(ImageIO.read(imageUrl), null);
                            map.setImage(image);
                            mapImage = image;
                            level = 2;
//                            DrawScheduler.scheduleAtFixedRate(new RunnableDrawer(), 0, 100, MILLISECONDS);
//                            gc.clearRect(0, 0, canvas.getWidth(), canvas.getHeight());
                        } catch (IOException ex) {
                            ex.printStackTrace();
                        }
                        break;
                }
            }
        };

        first.setOnAction(changeFloor);
        second.setOnAction(changeFloor);
        third.setOnAction(changeFloor);

        map.fitWidthProperty().bind(stackPane.widthProperty());


        EventHandler<ActionEvent> fireEvent = new EventHandler<ActionEvent>() {
            public void handle(final javafx.event.ActionEvent event) {
//                gc.clearRect(0, 0, canvas.getWidth(), canvas.getHeight());
                List<java.awt.Color> cs = new LinkedList<>();
                cs.add(java.awt.Color.RED);
                cs.add(java.awt.Color.BLUE);
                cs.add(java.awt.Color.YELLOW);
                cs.add(java.awt.Color.GREEN);
                cs.add(java.awt.Color.BLACK);

                BufferedImage img = SwingFXUtils.fromFXImage(mapImage, null);
                Graphics2D g2 = img.createGraphics();
                g2.setStroke(new BasicStroke(4));
//                g2.fillOval(check2.getX().intValue(), check2.getY().intValue(), 50, 50);
                int k = 0;
                for (Gyro g : curList) {
                    g2.setColor(cs.get(k));
                    if (g.getRoute().get(0).getFloor() != level) {
                        System.out.println("level");
                        System.out.println(g.getRoute().get(0).getFloor());
                        continue;
                    }
                    drawRoute(g, g2);
                    k = (k + 1) % cs.size();

                }
                Image imgS = SwingFXUtils.toFXImage(img, null);
                map.setImage(imgS);
                System.out.println("pictured\n");
            }
        };
        eventFier.setOnAction(fireEvent);
    }

    @FXML
    private void rotate( double angle, double px, double py) {
        Rotate r = new Rotate(angle, px, py);
        gc.setTransform(r.getMxx(), r.getMyx(), r.getMxy(), r.getMyy(), r.getTx(), r.getTy());
    }

    @FXML
    private void drawRotatedImage(Image image, double angle, double tlpx,
                                  double tlpy, int w, int h, double width, double height) {
        gc.save(); // saves the current state on stack, including the current transform
        rotate(angle, width / 2, height / 2);
        gc.drawImage(image, tlpx, tlpy, w, h);
        gc.restore(); // back to original state (before rotation)
    }

    @FXML
    public void drawRoute(Gyro g, Graphics2D g2) {
//        System.out.println(g.getRoute().size())

        List<Position> route = g.getRoute();

        if (route.size() < 2) {
            return;
        }

        for (int i = 0; i < route.size() - 1; ++i) {
            if (route.get(i + 1).getFloor() != level) {
                break;
            }

            if ((route.get(i +1).getX().intValue() - 5 < 0 || route.get(i +1).getX().intValue() - 5 > mapImage.getWidth()
                    || route.get(i +1).getY().intValue() - 5 < 0 || route.get(i +1).getY().intValue() - 5 > mapImage.getHeight())) {
                g2.fillOval(route.get(i +1).getX().intValue() - 5, route.get(i +1).getY().intValue() - 5, 10, 10);
                break;
            }

            g2.drawLine(route.get(i).getX().intValue(), route.get(i).getY().intValue(),
                    route.get(i + 1).getX().intValue(), route.get(i + 1).getY().intValue());
//            gc.setFill(Color.BLUE);
//            gc.setLineWidth(10);
//            gc.strokeLine(route.get(i).getX(), route.get(i).getY(),
//                    route.get(i + 1).getX(), route.get(i + 1).getY());
        }
        g2.fillOval(route.get(0).getX().intValue() - 5, route.get(0).getY().intValue() - 5,
                10, 10);

//        double angle = -Math.atan2(route.get(1).getY() - route.get(0).getY(), route.get(1).getX() - route.get(0).getX());
//
//        drawRotatedImage(gyro, angle - 90, route.get(0).getX(), route.get(0).getY(), 40, 40,
//                map.getFitWidth(), map.getFitHeight());
////        stackPane.getChildren().add(gyroCanvas);
    }



    public void processTrajectory(Gyro gyro) {
//        System.out.println("begin");
//        System.out.println(gyro.getRoute().size());
        List<Position> trajectory = gyro.getRoute();
        double speed = gyro.getSpeed(); // (pixel / 100?)
//        System.out.println(speed);
        double curTime = MILLISECONDS_IN_TICK;
        while(curTime > EPS && trajectory.size() > 1) {
            if (trajectory.get(1).getFloor() != trajectory.get(0).getFloor()) {
//                System.out.printf("aaa\n");
                trajectory.remove(0);
                break;
            }
            else {
                Position distance = Position.subtract(trajectory.get(1), trajectory.get(0));
                Double distanceValue =  Position.calculateDistance(distance);
                Double deltaDistanceValue = speed;
                if (distanceValue > deltaDistanceValue + EPS) {
                    Position newPosition = Position.sum(trajectory.get(0),
                            Position.mult(Position.subtract(trajectory.get(1), trajectory.get(0)), deltaDistanceValue / distanceValue));
                    Position removed =  trajectory.remove(0);
                    newPosition.setFloor(removed.getFloor());
                    trajectory.add(0, newPosition);
//                    System.out.println("rem\n");
//                    System.out.printf(removed.getX().toString(), removed.getY());
//                    System.out.println("new\n");
//                    System.out.printf(newPosition.getX().toString(), newPosition.getY());
                    break;
                } else if (distanceValue < deltaDistanceValue - EPS) {
                    curTime = curTime - distanceValue / speed * 100; //pixels in 100 millisecs
//                    System.out.println(curTime);
                    trajectory.remove(0);
                }
                else {
                    trajectory.remove(0);
                    break;
                }
            }
        }
//        System.out.println("end");
//        System.out.println(gyro.getRoute().size());
//        return gyro;
    }


    final class RunnableDrawer implements Runnable {
        public void run() {
            try {
                if (ticks % TICKS_IN_PERIOD == 0) {
                    try {
                        if (Main.getInstance().results.size() == 0) {
//                            System.out.println((Main.getInstance().results.size()));
                            return;
                        }
                        else {
                            curList = Main.getInstance().getResult();
//                            System.out.println(curList.get(0).getRoute().size());
                        }
                    } catch (Exception ex) {
                        ex.printStackTrace();
                        return;
                    }
                }
                else {
                    System.out.println(curList.size());
                    for (Gyro g : curList) {
                        if (g.getRoute().get(0).getFloor() != level) {
                            System.out.println(g.getRoute().get(0).getFloor());
                            continue;
                        }
                        processTrajectory(g);
                    }
                }
                System.out.println("rendered\n");
                eventFier.fire();
                ticks++;
            }  catch (Exception e) {
                System.out.println("hey\n");
                e.printStackTrace();
//                Main.getInstance().addResult(new LinkedList<Gyro>()); // Assuming I want to know that an invocation failed
            }
        }

    };

}
