var MyClass = (function (_super) {
    __extends(MyClass, _super);
    function MyClass() {
        _super.call(this);
        return global.__native(this);
    }
    MyClass.prototype.onCreate = function (savedInstanceState) {
     	_super.prototype.onCreate.call(this, false ? savedInstanceState : null);
     	android.util.Log.d("Sbg.Test","we got called from onCreate of my-custom-class.js");
    };

    MyClass = __decorate([
        JavaProxy("com.tns.MyJavaClass")
    ], MyClass);

    return MyClass;
}(android.app.Activity));
