var vmModule = require("./main-view-model");
var count = 0;
function pageLoaded(args) {
    var page = args.object;
    page.bindingContext = vmModule.mainViewModel;
    console.log("Page loaded " + ++count + " times.");
    
    var objTC = new TestClass();
    console.log(objTC.sayHey());
}
exports.pageLoaded = pageLoaded;
