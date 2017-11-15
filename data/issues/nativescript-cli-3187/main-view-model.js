var observable = require("data/observable");
var http = require("http");
var HelloWorldModel = (function (_super) {
    __extends(HelloWorldModel, _super);
    function HelloWorldModel() {
        _super.call(this);
        this.counter = 42;
        this.set("message", this.counter + " taps left");
    }
    HelloWorldModel.prototype.tapAction = function () {
        this.counter--;
        if (this.counter <= 0) {
            this.set("message", "Hoorraaay! You unlocked the NativeScript clicker achievement!");
        }
        else {
            this.set("message", this.counter + " taps left");

            http.getString("https://httpbin.org/get").then(function (r) {
            //// Argument (r) is string!
            }, function (e) {
            //// Argument (e) is Error!
            });
        }
    };
    return HelloWorldModel;
})(observable.Observable);
exports.HelloWorldModel = HelloWorldModel;
exports.mainViewModel = new HelloWorldModel();
