var createViewModel = require("./main-view-model").createViewModel;
var utils = require("utils/utils");
var application = require("application");

function onNavigatingTo(args) {
    var page = args.object;
    page.bindingContext = createViewModel();
    console.log("### TEST START ###");
    var test = com.tns.AbstractInterface.test();
    //var ddd = java.lang.Object.extend({
        //interfaces: [com.tns.AbstractInterface],
        //});
    //var testClass = new com.tns.AbstractInterface({});
    //(new ddd()).testDefault();

    sleep(2000);
    console.log("###TEST CALL PUBLIC METHOD IN ABSTRACT INTERFACE PASSED###");
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