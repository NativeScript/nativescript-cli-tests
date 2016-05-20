// main-page.js
var vmModule = require("./main-view-model");
function pageLoaded(args) {
    var page = args.object;
    page.bindingContext = vmModule.mainViewModel;
}
exports.pageLoaded = pageLoaded;

var camera;
var mapView;
var marker;

function createMapView(args) {
    console.log("Creating map view...");
    camera = GMSCameraPosition.cameraWithLatitudeLongitudeZoom(-33.86, 151.20, 6);
    mapView = GMSMapView.mapWithFrameCamera(CGRectZero, camera);

    console.log("Setting a marker...");
    marker = GMSMarker.alloc().init();
    // NOTE: In-line functions such as CLLocationCoordinate2DMake are not exported.
    marker.position = { latitude: -33.86, longitude: 151.20 }
    marker.title = "Sydney";
    marker.snippet = "Australia";
    marker.map = mapView;

    console.log("Displaying map...");
    args.view = mapView;
}
exports.createMapView = createMapView;
