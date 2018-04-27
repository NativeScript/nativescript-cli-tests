var vmModule = require("./main-view-model");

function pageLoaded(args) {
    var page = args.object;
    page.bindingContext = vmModule.mainViewModel;
    console.log("### TEST START ###");

    var undef;
    var num = -1;
    var str = "text";
    var obj = { name: "John", age: 34 };

    console.dir(true);
    console.dir(false);
    console.dir(null);
    console.dir(undef);

    console.dir(num);
    console.dir(str);

    console.dir(obj);

    console.log("### TEST END ###");
}
exports.pageLoaded = pageLoaded;
