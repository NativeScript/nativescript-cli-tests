var createViewModel = require("./main-view-model").createViewModel;
var AlbumSelectActivity = $in.myinnos.awesomeimagepicker.activities.AlbumSelectActivity;
var ConstantsCustomGallery = $in.myinnos.awesomeimagepicker.helpers.ConstantsCustomGallery;
var utils = require("utils/utils");
var application = require("application");
function onNavigatingTo(args) {
    var page = args.object;
    page.bindingContext = createViewModel();
    console.log("### TEST START ###");
    var context = utils.ad.getApplicationContext();
    var myIntent = new android.content.Intent(context, AlbumSelectActivity.class);
    myIntent.putExtra(ConstantsCustomGallery.INTENT_EXTRA_LIMIT, 20); // set limit for image selection
    application.android.foregroundActivity.startActivityForResult(myIntent, ConstantsCustomGallery.REQUEST_CODE);
    sleep(2000);
    console.log("###TEST IMPLEMENTATION PASSED###");
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