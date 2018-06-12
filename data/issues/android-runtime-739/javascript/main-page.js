var createViewModel = require("./main-view-model").createViewModel;
var myRunnable = new java.lang.Runnable({
            run: function(){}
        });

function onNavigatingTo(args) {
    var page = args.object;
    page.bindingContext = createViewModel();
    console.log("### TEST START ###");
    if (myRunnable instanceof java.lang.Runnable) {
          console.log("### TEST PASSED ###");
    }
    else
    {
        console.log("### TEST FAILED ###");
    }
    console.log("### TEST END ###");
}
exports.onNavigatingTo = onNavigatingTo;
