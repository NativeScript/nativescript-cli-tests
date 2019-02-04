var Observable = require("data/observable").Observable;

function getMessage() {
    console.log("### TEST START ###");
    var fileManager = NSFileManager.defaultManager;
    fileManager.contentsOfDirectoryAtPathError('/not-existing-path');
    console.log("### TEST SHOULD NOT CRASH ###");
    console.log("### TEST END ###");
}

function createViewModel() {
    var viewModel = new Observable();
    viewModel.message = getMessage();

    viewModel.onTap = function() {

    }

    return viewModel;
}

exports.createViewModel = createViewModel;