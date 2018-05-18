var createViewModel = require("./main-view-model").createViewModel;
var AlbumSelectActivity = $in.myinnos.awesomeimagepicker.activities.AlbumSelectActivity;

function onNavigatingTo(args) {
    var page = args.object;
    page.bindingContext = createViewModel();
    console.log("###TEST PASSED###");
}
exports.onNavigatingTo = onNavigatingTo;