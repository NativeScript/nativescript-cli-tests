var Observable = require("data/observable").Observable;

function getMessage() {
    console.log("### TEST START ###");
    console.log("Hex: " + interop.Pointer(-1).toHexString());
    console.log("Decimal: " + interop.Pointer(-1).toDecimalString());
    console.log("Hex: " + interop.Pointer(-2).toHexString());
    console.log("Decimal: " + interop.Pointer(-2).toDecimalString());
    console.log("Hex: " + interop.Pointer(34359738368).toHexString());
    console.log("Decimal: " + interop.Pointer(34359738368).toDecimalString());
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