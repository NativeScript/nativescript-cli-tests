var vmModule = require("./main-view-model");
var buttonModule = require("tns-core-modules/ui/button");

function pageLoaded(args) {
    var page = args.object;
    page.bindingContext = vmModule.mainViewModel;
    console.log("### TEST START ###");
    console.log("### TEST END ###");
}
exports.pageLoaded = pageLoaded;
