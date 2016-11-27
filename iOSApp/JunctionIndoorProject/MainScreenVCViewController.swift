//
//  MainScreenVCViewController.swift
//  
//
//  Created by Alexander Malyshev on 25.11.16.
//
//

import UIKit
import GoogleMaps
import GooglePlaces
import GooglePlacePicker

protocol Mapable: class {
    var map: GMSMapView? {set get}
}

var SAVED_POSITION: CLLocationCoordinate2D?
var SAVED_LEVEL: GMSIndoorLevel?

class MainScreenVCViewController: UIViewController, GMSMapViewDelegate, GMSIndoorDisplayDelegate {

    func bind(_ x: GMSOverlay) {
        if (self.mapView?.indoorDisplay.activeLevel == currentLevel) {
            x.map = self.mapView
        } else {
            x.map = nil
        }
    }
    
    var placesClient: GMSPlacesClient?
//    NSArray *_exhibits;     // Array of JSON exhibit data.
//    NSDictionary *_exhibit; // The currently selected exhibit. Will be nil initially.
//    GMSMarker *_marker;
//    NSDictionary *_levels;
    
    let lat = 60.484033
    let lnt = 15.418454
    
    var selectedPlace: Place? { return SELECTED_PLACE }
    
    var mapView: GMSMapView?
//    var marker: GMSMarker?
    var currentBuilding: GMSIndoorBuilding?
    var currentLevel: GMSIndoorLevel?
    var myLocation: GMSMarker?
    var currentLocation: CLLocationCoordinate2D? { return myLocation?.position }
    var destinitionCircle: GMSCircle?
    
    var presentativePath: GMSMutablePath?
    var path: [Coord]?
    
    var goButton: UIButton?
    
    override func viewDidLoad() {
        super.viewDidLoad()
        let position = SAVED_POSITION ?? CLLocationCoordinate2D(latitude: lat, longitude: lnt)
        let camera = GMSCameraPosition.camera(withTarget: position, zoom: 18)
        let mapView = GMSMapView.map(withFrame: CGRect(x: 0, y: 50, width: 320, height: 465), camera: camera)
        mapView.isMyLocationEnabled = true
        self.view.addSubview(mapView)
        self.mapView = mapView
        self.mapView?.delegate = self
        self.mapView?.indoorDisplay.delegate = self
    
        let blurViewFrame = CGRect(x: 110, y: 360, width: 100, height: 100)
        let buttonFrame = blurViewFrame
        let button = UIButton(frame: buttonFrame)
        
        
        button.setTitle("Go!", for: .normal)
        button.setTitleColor(UIColor.black, for: .normal)
        button.layer.borderWidth = 1.5
        //        button.layer.borderColor = CGColor(
        button.backgroundColor = UIColor(colorLiteralRed: 0, green: 0, blue: 255, alpha: 0.6)
        
        
        button.layer.cornerRadius = button.layer.bounds.height/2.0
        button.tintColor = UIColor(colorLiteralRed: 0, green: 0, blue: 0, alpha: 0.5)
        button.addTarget(self, action: #selector(runDemo), for: UIControlEvents.allEvents)
//        button.titleLabel?.font = UIFont(name: "System Thin", size: 30.0)
        
        let blur = UIVisualEffectView(effect: UIBlurEffect(style:
            UIBlurEffectStyle.extraLight))
        blur.frame = button.bounds
        blur.layer.opacity = 0.2
        blur.layer.cornerRadius = button.layer.cornerRadius
        blur.clipsToBounds = true
        blur.isUserInteractionEnabled = false //This allows touches to forward to the button.
        button.insertSubview(blur, at: 0)
        
        
        
        goButton = button
        
//        viewWithBlur.addSubview(goButton!)
//        mapView.addSubview(viewWithBlur)
        mapView.addSubview(goButton!)
        
        
    }
    
    var isRunning: Bool = false
    
    @IBAction func runDemo(_ sender: Any) {
        self.goButton?.isHidden = true
        if (isRunning) {
            return
        }
        isRunning = true
        moveCameraToCurrentLocation()
        
        var currentLevelInt: Int = 0
        var distLevelInt: Int = 0
        if (currentLevel?.name?.contains("1"))! {
            currentLevelInt = 0
        }
        if (currentLevel?.name?.contains("2"))! {
            currentLevelInt = 1
        }
        if (currentLevel?.name?.contains("3"))! {
            currentLevelInt = 2
        }
        
        distLevelInt = (selectedPlace?.floor)! - 1
        
        
        
        getPath(currentLoc: self.currentLocation!, currentLevel: currentLevelInt,destLoc: (self.selectedPlace?.location)!, destLevel: distLevelInt) {
            self.drawPolyline()
            
            
//            let path = GMSMutablePath()
//            path.add(self.currentLocation!)
//            path.add((self.selectedPlace?.location)!)
//            path.add(CLLocationCoordinate2D(latitude: 60.486033, longitude: 15.419454))
//            let anotherPoly = GMSPolyline(path: path)
//            anotherPoly.strokeColor = UIColor.blue
//            anotherPoly.strokeWidth = 3
//            anotherPoly.map = self.mapView
            
            
    //        TEMPMARKER.map = self.mapView
            
            self.recursivelyAnimate(marker: self.myLocation!, index: 0)
            self.isRunning = false
        }
    }
    
    func drawPolyline() {
        self.presentativePath = GMSMutablePath()
        for coord in self.path! {
            if (currentLevel == coord.floor) {
                self.presentativePath?.add(coord.googleCoord)
            }
        }
        let polyline = GMSPolyline(path: self.presentativePath!)
        polyline.strokeWidth = 3
        polyline.strokeColor = UIColor.red
        polyline.map = self.mapView
        self.polylineRoad = polyline
    }
    
    var polylineRoad: GMSPolyline?
    
    func recursivelyAnimate(marker: GMSMarker, index: Int) {
        if ((self.path?.count)! <= index) {
            return
        }
        CATransaction.begin()
        CATransaction.setCompletionBlock { 
            self.recursivelyAnimate(marker: marker, index: index + 1)
        }
        
        if let nextPos = self.path?[index].googleCoord, let level = self.path?[index].floor {
            let prevPos = marker.position
            let distance = GMSGeometryDistance(prevPos, nextPos)
            CATransaction.setAnimationDuration(distance/8)
            marker.position = nextPos
            if (level != currentLevel) {
                polylineRoad?.map = nil
                currentLevel = level
                self.mapView?.indoorDisplay.activeLevel = level
                drawPolyline()
            }
            let camera = GMSCameraPosition.camera(withTarget: (myLocation?.position)!, zoom: 19)
            self.mapView?.animate(to: camera)
        }
        CATransaction.commit()
    }
    
    func changeLocation(_ coord: CLLocationCoordinate2D) {
        self.myLocation?.position = coord
    }
    
    func getPath(currentLoc: CLLocationCoordinate2D, currentLevel: Int, destLoc: CLLocationCoordinate2D, destLevel: Int, completionHandler: @escaping () -> Void) {
        self.path = [Coord]()
        let urlPath = "http://46.101.182.16/navigate/?floor_from=\(currentLevel)&x_from=\(currentLoc.longitude)&y_from=\(currentLoc.latitude)&floor_to=\(destLevel)&x_to=\(destLoc.longitude)&y_to=\(destLoc.latitude)"
        print(urlPath)
        let url = URL(string: urlPath)!
        let session = URLSession(configuration: URLSessionConfiguration.default)
        var task = session.dataTask(with: url) { (data, urlresponse, error) in
            if let error = error {
                print(error)
                return
            }
            let json = try! JSONSerialization.jsonObject(with: data!, options: JSONSerialization.ReadingOptions.allowFragments) as! NSArray
            for item in json {
                print("JSON SIZE \(json.count)")
                let itemArr = item as! NSArray
                let level = itemArr[0] as! NSNumber
                let coords = itemArr[1] as! NSArray
                let lat = coords[0] as! Double
                let lng = coords[1] as! Double
                
                print(level, lat, lng)
                
                let googleCoord = CLLocationCoordinate2D(latitude: CLLocationDegrees(lat), longitude: CLLocationDegrees(lng))
                let coord = Coord.init(googleCoord, (self.currentBuilding?.levels[2 - level.intValue])!)
                self.path?.append(coord)
            }
            print("Finished parsing")
            completionHandler()
        }
        task.resume()
    }
    
    override func viewWillAppear(_ animated: Bool) {
        self.myLocation?.position = SAVED_POSITION!
        self.mapView?.indoorDisplay.activeLevel = SAVED_LEVEL
        goButton?.isHidden = (selectedPlace == nil)
    }
    
    

    
    override func viewDidAppear(_ animated: Bool) {
        if (selectedPlace?.location != nil) {
            moveCameraToDestinition()
        }
    }
    
    func moveCameraToCurrentLocation() {
        mapView?.indoorDisplay.activeLevel = currentLevel
        let newCameraPosition = GMSCameraPosition.camera(withTarget: (myLocation?.position)!, zoom: 17)
        self.mapView?.animate(to: newCameraPosition)
        self.mapView?.animate(toZoom: 19)
    }
    
    func moveCameraToDestinition() {
        let newCameraPosition = GMSCameraPosition.camera(withTarget: (selectedPlace?.location)!, zoom: 17)
        
        self.mapView?.animate(to: newCameraPosition)
        self.mapView?.animate(toZoom: 19)
    }
    
    var activeLevel: GMSIndoorLevel? { return (self.mapView?.indoorDisplay.activeLevel) }
    
    func drawObjects() {

        
    }
    
    func didChangeActiveBuilding(_ building: GMSIndoorBuilding?) {
        currentLevel = building?.levels[2]
        currentBuilding = building
        if (selectedPlace != nil) {
            self.mapView?.indoorDisplay.activeLevel = activeLevel(building, (selectedPlace?.floor)!)
        }
    }
    
    func didChangeActiveLevel(_ level: GMSIndoorLevel?) {
        if (self.mapView?.indoorDisplay.activeLevel == currentLevel) {
            if (myLocation == nil) {
                if (SAVED_POSITION == nil) {
                    myLocation = GMSMarker(position: CLLocationCoordinate2D(latitude: lat, longitude: lnt))
                } else {
                    myLocation = GMSMarker(position: SAVED_POSITION!)
                }
            }
            myLocation?.map = self.mapView
            
        } else {
            mapView?.clear()
        }
        
        if let selPlace = selectedPlace, let cBuilding = self.currentBuilding {
            if (activeLevel?.name == activeLevel(cBuilding, selPlace.floor)?.name) {
                destinitionCircle = GMSCircle(position: selPlace.location, radius: 1)
                destinitionCircle?.fillColor = UIColor.blue
                destinitionCircle?.map = self.mapView
            } else {
                mapView?.clear()
                
                if (self.mapView?.indoorDisplay.activeLevel == currentLevel) {
                    if (SAVED_POSITION == nil) {
                        myLocation = GMSMarker(position: CLLocationCoordinate2D(latitude: lat, longitude: lnt))
                    } else {
                        myLocation = GMSMarker(position: SAVED_POSITION!)
                    }
                    myLocation?.map = self.mapView
                }
                
                
//                destinitionCircle?.map = nil
            }
        }
    }

    
    
    func activeLevel(_ building: GMSIndoorBuilding?, _ floor: Int) -> GMSIndoorLevel? {
        return (building?.levels[2 - (floor - 1)])
    }
    
    
    
    func getPlaces() {
       let urlPath = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=\(lat),\(lnt)&radius=250&key=AIzaSyAmJdkJ_LUy0MNtAovXVzHDjeWcqmQpQMQ"
//        let urlRequst = NSURLRequest(url: URL(fileURLWithPath: urlPath))
//        let url = URL(string: "http://46.101.182.16/maplayer")!
        let url = URL(string: urlPath)!
//        let url = URL(fileURLWithPath: urlPath)
        
//        let request = NSURLRequest(url: urlPath)

        
        let session = URLSession(configuration: URLSessionConfiguration.default)
        
        var task = session.dataTask(with: url) { (data, urlresponse, error) in
            if let error = error {
                print(error)
                return
            }
//            print(urlresponse)
//            print(data)
            let json = try! JSONSerialization.jsonObject(with: data!, options: JSONSerialization.ReadingOptions.allowFragments) as! NSDictionary
            let results = json["results"] as! NSArray
            for (it) in results {
                let item = it as! NSDictionary
                
//                print(item["place_id"] as! String)
                let itemGeom = item["geometry"] as! NSDictionary
                let itemLoc = itemGeom["location"] as! NSDictionary
                let name = item["name"] as! String
                let lat = itemLoc["lat"] as! Double
                let lng = itemLoc["lng"] as! Double
                let formatedString = " \"" + name + "\"" +  ", (" + String(lat) + ", " + String(lng) + ")" + ", "
                print(formatedString)
                
//                print("---")
                
            }
//            name
//            place_id
//            geometry location  lat lng
//            
//            print(results)
        }

        
        task.resume()
    }
    

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    // it is not go button, but who cares
    @IBAction func selectPlaceButtonPressed(_ sender: Any) {
//        SAVED_POSITION = self.currentLocation
//        SAVED_LEVEL = self.currentLevel
    }
    @IBAction func goButtonPressed(_ sender: Any) {

    }

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
    }
    */

}
