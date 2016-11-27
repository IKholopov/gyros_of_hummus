package sample;

import java.util.List;
import java.util.concurrent.ConcurrentLinkedQueue;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.canvas.Canvas;
import javafx.scene.layout.GridPane;
import javafx.stage.Stage;

public class Main extends Application {
    private static Main instance;

    private Controller controller;


    final ConcurrentLinkedQueue<List<Gyro> > results
            = new ConcurrentLinkedQueue<List<Gyro>>();


    @Override
    public void start(Stage primaryStage) throws Exception{
        FXMLLoader fxmlLoader = new FXMLLoader(Main.class.getResource("/sample.fxml"));
        GridPane root = null;
        fxmlLoader.setRoot(root);
        root = (GridPane)fxmlLoader.load();
        controller = fxmlLoader.getController();
        primaryStage.setTitle("Hello World");
        primaryStage.setScene(new Scene(root));
        primaryStage.show();
    }

    public Main() {
        instance = this;
    }
    public static Main getInstance() {
        return instance;
    }

    public void addResult(List<Gyro> newEl) {
//        System.out.println(newEl.get(0).getRoute().size());
        results.add(newEl);
    }

    public List<Gyro> getResult() {
        List<Gyro> res =  (List<Gyro>)results.poll();
//        System.out.println(res.get(0).getRoute().size());
        return res;
    }

    public static void main(String[] args) {
        launch(args);
    }

    public Controller getController() {
        return controller;
    }
}
