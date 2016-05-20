// app.js
var application = require("application");

application.onLaunch = function() {
    console.log('Providing Google Map API key...');
    // NOTE: Visit the Google documentation to learn how to obtain an API key: https://developers.google.com/maps/documentation/ios/start
    GMSServices.provideAPIKey("AIzaSyAju-slsCHJ_jcUuepHeWX1geeZBZYqL48");
}

application.mainModule = "main-page";
application.cssFile = "./app.css";
application.start();
