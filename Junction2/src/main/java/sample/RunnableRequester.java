package sample;


import com.sun.org.apache.regexp.internal.RE;
import com.sun.org.apache.xerces.internal.impl.xpath.regex.ParseException;
import com.sun.org.apache.xerces.internal.util.SAX2XNI;
import com.sun.org.apache.xerces.internal.util.URI;

import org.json.simple.*;
import org.json.simple.parser.JSONParser;
import org.omg.CORBA.Request;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.LinkedList;
import java.util.List;
import java.util.concurrent.Callable;
import static java.util.concurrent.TimeUnit.SECONDS;

//    (60.484129, 15.418381), (60.484351, 15.417935)


//    393.5325 - x1
//            220.91250000000002 - y1
//            484.98 - y1
//            314.415 - y2



/**
 * Created by valeriyasin on 11/26/16.
 */

final class RunnableRequester implements Runnable {

    private Double scaleX = (393.5325 - 484.98) / (15.418381 - 15.417935);
    private Double scaleY = (220.91250000000002 - 314.415) / (60.484129 - 60.484351);
    private Double moduleScale = Position.calculateDistance(new Position(scaleX, scaleY, 0));

    private Position startGeo;
    private Position startPix;

    private JSONArray stringToJson(String string) {
        JSONParser parser = new JSONParser();
        try {
            JSONArray json = (JSONArray) parser.parse(string);
            return json;
        } catch (org.json.simple.parser.ParseException ex) {
            ex.printStackTrace();
        }
        System.out.printf("wrong\n");
        return null;
    }

    private Position translateCoordinates(Position posGeo) {
        Position vector = Position.subtract(posGeo, startGeo);
        return Position.sum(startPix, new Position(vector.getX() * scaleX, vector.getY() * scaleY, 0));
    }


    private List<Gyro> processJson(JSONArray gyrosJson) {
        List<Gyro> gyros = new LinkedList<>();
        for (int i = 0; i < gyrosJson.size(); ++i) {
            JSONObject obj = (JSONObject)gyrosJson.get(i);
            JSONObject route =  (JSONObject)obj.get("route");
            Double y_c = Double.parseDouble(obj.get("y_coord").toString());
            Double x_c = Double.parseDouble(obj.get("x_coord").toString());
            Double floor_c = Double.parseDouble(obj.get("floor").toString());
            if (route != null) {
                Gyro newG = new Gyro();
                Double speed =  Double.parseDouble(obj.get("speed").toString()) * moduleScale / 3 / 10;
                newG.setSpeed(speed);
                List<Position> rout = new LinkedList<>();
                rout.add(translateCoordinates(new Position(x_c, y_c,
                        floor_c.intValue())));
                String path = (String)route.get("path");
                JSONArray pathJson = stringToJson(path);
                for (int j = 0; j < pathJson.size(); ++j) {
                    JSONArray pp = (JSONArray) pathJson.get(j);
                    int floor = Integer.parseInt(pp.get(0).toString());
                    JSONArray p = (JSONArray)pp.get(1);
                    Double y = Double.parseDouble(p.get(0).toString());
                    Double  x = Double.parseDouble(p.get(1).toString());
                    Position pos = translateCoordinates(new Position(x, y,
                            floor));
//                    System.out.println(pos.getX());
                    rout.add(pos);

//                    System.out.println(rout.size());
                }
                newG.setRoute(rout);
//                System.out.println(newG.getRoute().size());
                gyros.add(newG);
            }
        }
        return gyros;
    }

    private static String Url = "http://46.101.182.16/scooters_data/?format=json";

    final class Requester implements Callable<List<Gyro> > {

        Requester() {
            startGeo = new Position(15.418381, 60.484129, 0);
            startPix = new Position(393.5325, 220.91250000000002, 0);
        }
        public List<Gyro> call() {
            try {
                System.out.println("req\n");
                URL obj = new URL(Url);
                HttpURLConnection con = (HttpURLConnection) obj.openConnection();
                con.setRequestMethod("GET");
                int responseCode = con.getResponseCode();
//                System.out.println(responseCode);
                if (responseCode == HttpURLConnection.HTTP_OK) { // success
                    BufferedReader in = new BufferedReader(new InputStreamReader(
                            con.getInputStream()));
                    String inputLine;
                    StringBuffer response = new StringBuffer();
                    while ((inputLine = in.readLine()) != null) {
                        response.append(inputLine);
                    }
                    JSONArray jsonObject = stringToJson(response.toString());
//                    System.out.println(response);
                    in.close();
                    List<Gyro> l = processJson(jsonObject);
                    return l;
                }
                return new LinkedList<Gyro>();
            } catch(IOException ex) {
                ex.printStackTrace();
            }
            return null;
        }
    };

    public void run() {
        try {
            System.out.println("request\n");
            Callable req = new Requester();
            List<Gyro> l = (List<Gyro>)req.call();
//            System.out.println(l.get(0).getRoute().size());
            Main.getInstance().addResult(l);
        }  catch (Exception e) {
            e.printStackTrace();
            Main.getInstance().addResult(new LinkedList<Gyro>()); // Assuming I want to know that an invocation failed
        }
    }

};


