var createViewModel = require("./main-view-model").createViewModel;
var AlbumSelectActivity = $in.myinnos.awesomeimagepicker.activities.AlbumSelectActivity;

function onNavigatingTo(args) {
    var page = args.object;
    page.bindingContext = createViewModel();
    sleep(2000);
    console.log("###TEST PASSED###");
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