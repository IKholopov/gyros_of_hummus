//
//  Place.swift
//  JunctionIndoorProject
//
//  Created by Alexander Malyshev on 26.11.16.
//  Copyright © 2016 Gyros Of Hummus. All rights reserved.
//

import UIKit
import GoogleMaps

class Place: NSObject {
    let name: String
    let location: CLLocationCoordinate2D
    let floor: Int
    init(_ name: String, _ coord: (Double, Double), _ floor: Int) {
        self.name = name
        self.location = CLLocationCoordinate2D(latitude: coord.0, longitude: coord.1)
        self.floor = floor
    }
}

class Coord: NSObject {
    let googleCoord: CLLocationCoordinate2D
    let floor: GMSIndoorLevel
    init(_ googleCoord: CLLocationCoordinate2D, _ floor: GMSIndoorLevel) {
        self.googleCoord = googleCoord
        self.floor = floor
    }
}


let places: [Place] = {
    var instance: [Place] = []
    instance.append(Place("Hotel Kupolen", (60.4839371,
        15.4187693), 1))
    instance.append(Place("McDonald's", (60.4853481, 15.4181156), 2))
    instance.append(Place("Apoteket Kupolen", (60.484216, 15.418711), 1))
    instance.append(Place("Telia", (60.4840221, 15.4184573), 1))
    instance.append(Place("Phone House", (60.4843145, 15.4184791), 3))
    instance.append(Place("DinSko", (60.4839972, 15.4184886), 2))
    return instance
}()


var SELECTED_PLACE: Place?
