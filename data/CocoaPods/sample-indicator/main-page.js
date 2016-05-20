var vmModule = require("./main-view-model");
function pageLoaded(args) {
    var page = args.object;
    page.bindingContext = vmModule.mainViewModel;
}
exports.pageLoaded = pageLoaded;

function creatingView(args) {
  var spinnerView = MMMaterialDesignSpinner.alloc().initWithFrame(CGRectMake(0,0,50,50));
    spinnerView.lineWidth = 17;
    spinnerView.tintColor = UIColor.greenColor();

    spinnerView.startAnimating();
    args.view = spinnerView;
}
exports.creatingView = creatingView;
