var createViewModel = require("./main-view-model").createViewModel;

function onNavigatingTo(args) {
    var page = args.object;
    page.bindingContext = createViewModel();
}
var testList = new java.util.List();
exports.onNavigatingTo = onNavigatingTo;