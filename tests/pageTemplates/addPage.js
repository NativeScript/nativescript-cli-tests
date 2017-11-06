'use strict';

const pathToPackage = require("global-modules-path").getPath("nativescript", "tns");

const tns = require(pathToPackage);

const checkFlavor = (flavor) => {
    if (typeof flavor !== "string") {
        return new Error("Flavor fust be string");
    }
    const isAngular= flavor.indexOf("ng") > -1;
    const isTypeScript = flavor.indexOf("ts") > -1;
    const isJs = flavor.indexOf("js") > -1;

    if (isAngular) {
        flavor = "Angular & TypeScript";
        console.log("Flavor === ", flavor);
    } else if (isTypeScript) {
        flavor = "TypeScript";
        console.log("Flavor === ", flavor);
    } else if (isJs) {
        flavor = "JavaScript";
        console.log("Flavor === ", flavor);
    } else {
        return new Error("Invalid flavor!!!"); // TODO Print help with valid flavors 
    }

    return(flavor);
}

const pageAction = () => {
    const args = process.argv.slice(2, 6);
    let appFlavor = '';
    try {
        appFlavor = checkFlavor(args[2]);
    } catch(error) {
        console.error(error);
    }
    
    const newPageName = args[0];
    const options = {
        displayName: args[1],
        templateFlavor: appFlavor
    }
    const appPath = args[3];

    tns.nsStarterKitsApplicationService.addPage(newPageName, options, appPath)
    .then(function(details){
        console.log('Details=== ', details)
    })
    .catch(function(err){
        console.error('Error=== ', err)
    })
};

Promise.all(tns.extensibilityService.loadExtensions())
    .then(pageAction, pageAction);