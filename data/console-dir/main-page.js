var vmModule = require("./main-view-model");

function pageLoaded(args) {
    var page = args.object;
    page.bindingContext = vmModule.mainViewModel;
    console.log("### TEST START ###");

    var undef;
    var num = -1;
    var str = "text";
    var obj = { name: "John", age: 34 };
    var one_hundred_symbols_string="1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890"
    var very_long_string = "";

    for (i = 0; i < 30; i++) {
        very_long_string = very_long_string + one_hundred_symbols_string;
    }

    console.dir(true);
    console.dir(false);
    console.dir(null);
    console.dir(undef);

    console.dir(num);
    console.dir(str);

    console.dir(obj);

    console.dir(very_long_string);

    console.log("### TEST END ###");
}
exports.pageLoaded = pageLoaded;
