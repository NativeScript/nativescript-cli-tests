/*
In NativeScript, the app.js file is the entry point to your application.
You can use this file to perform app-level initialization, but the primary
purpose of the file is to pass control to the app’s first module.
*/

require("./bundle-config");
var application = require("application");
var extendedClassesSpaces = require("./extended-classes spaces");
var extendedClassesDashes = require("./extended-classes-dashes");
var extendedClassesInDirWithSpaces = require("./dir spaces/extended-classes");

var i1 = extendedClassesSpaces.getExtendedClassInstance();
var i2 = extendedClassesDashes.getExtendedClassInstance();
var i3 = extendedClassesInDirWithSpaces.getExtendedClassInstance();

application.start({ moduleName: "main-page" });

/*
Do not place any code after the application has been started as it will not
be executed on iOS.
*/
