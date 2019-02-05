/*
In NativeScript, the app.js file is the entry point to your application.
You can use this file to perform app-level initialization, but the primary
purpose of the file is to pass control to the app’s first module.
*/

var application = require("tns-core-modules/application");

application.run({ moduleName: "app-root" });

new com.google.android.exoplayer2.source.smoothstreaming.DefaultSsChunkSource.Factory((new com.google.android.exoplayer2.upstream.DataSource.Factory("Date",new java.lang.Object())))

/*
Do not place any code after the application has been started as it will not
be executed on iOS.
*/
