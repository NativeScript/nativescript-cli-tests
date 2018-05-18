var vmModule = require("./main-view-model");
var buttonModule = require("tns-core-modules/ui/button");

function pageLoaded(args) {
    var page = args.object;
    page.bindingContext = vmModule.mainViewModel;
    console.log("### TEST START ###");
    console.time("Time");

    var undef;
    var num = -1;
    var str = "text";
    var obj = { name: "John", age: 34 };
    var button = new buttonModule.Button();

    var one_hundred_symbols_string="1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890"
    var very_long_string = "";

    for (i = 0; i < 30; i++) {
        very_long_string = very_long_string + one_hundred_symbols_string;
    }

    console.log(very_long_string);

    console.log(true);
    console.log(false);
    console.log(null);
    console.log(undef);

    console.log(num);
    console.log(str);
    console.log(obj);

    console.log(`number: ${num}`);
    console.log(`string: ${str}`);
    console.log(`${str} ${num}`);

    console.info("info");
    console.warn("warn");
    console.error("error");

    console.assert(false, `false == true`);
    console.assert(true, "1 equals 1");

    console.assert("", "empty string evaluates to 'false'");

    console.trace("console.trace() called");

    console.log(`${button}`);

    console.log(num, str, obj);
    console.log([1, 5, 12.5, obj, str, 42]);

    console.trace();

    console.timeEnd("Time");
    console.log("### TEST END ###");
}
exports.pageLoaded = pageLoaded;
