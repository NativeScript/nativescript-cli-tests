var createViewModel = require("./main-view-model").createViewModel;
var utils = require("utils/utils");

function onNavigatingTo(args) {
    var page = args.object;
    page.bindingContext = createViewModel();
    console.log("### TEST START ###");
    com.tns.mylib.useDependency(utils.ad.getApplicationContext());
    console.log("###TEST ARR PLUGIN PASSED###");
    console.log("### TEST END ###");
}
exports.onNavigatingTo = onNavigatingTo;