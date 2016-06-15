var createViewModel = require("./main-view-model").createViewModel;
var application = require("application");

function onNavigatingTo(args) {
    var page = args.object;
    page.bindingContext = createViewModel();

    var context = application.android.context;
    console.log(context);
    var myIntent = new android.content.Intent(context, com.tns.MyJavaClass.class);
    console.log(myIntent)
    console.log(context.startActivity)

    myIntent.setFlags(android.content.Intent.FLAG_ACTIVITY_NEW_TASK);
    context.startActivity(myIntent);
}
exports.onNavigatingTo = onNavigatingTo;