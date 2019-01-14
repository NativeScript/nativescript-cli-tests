var vmModule = require("./main-view-model");

function pageLoaded(args) {
    var page = args.object;
    page.bindingContext = vmModule.mainViewModel;
    
    var objTC = new TestClass();
    console.log(objTC.sayName());
    console.log(objTC.sayName("John"));
    console.log(objTC.sayName("John","James"));
}
exports.pageLoaded = pageLoaded;
