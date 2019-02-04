var application = require("application");

global.__onDiscardedError = function(error){
    console.log(error.message);
    console.log(error.stackTrace);
    console.log(error.nativeException);
}

application.start({ moduleName: "main-page" });