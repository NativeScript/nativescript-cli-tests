var createViewModel = require("./main-view-model").createViewModel;
var utils = require("utils/utils");

function onNavigatingTo(args) {
    var page = args.object;
    page.bindingContext = createViewModel();
    console.log("### TEST START ###");
    com.tns.mylib.useDependency(utils.ad.getApplicationContext());
    sleep(2000);
    console.log("###TEST ARR PLUGIN PASSED###");
    console.log("### TEST END ###");
}
exports.onNavigatingTo = onNavigatingTo;

function sleep(milliseconds) {
  var start = new Date().getTime();
  for (var i = 0; i < 1e7; i++) {
    if ((new Date().getTime() - start) > milliseconds){
      break;
    }
  }
}