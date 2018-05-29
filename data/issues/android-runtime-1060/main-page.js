var createViewModel = require("./main-view-model").createViewModel;

function onNavigatingTo(args) {
    var page = args.object;
    page.bindingContext = createViewModel();
    var bb = java.nio.ByteBuffer.allocate(12);
    var ab = ArrayBuffer.from(bb);
    console.log("###TEST PASSED###");
}
exports.onNavigatingTo = onNavigatingTo;