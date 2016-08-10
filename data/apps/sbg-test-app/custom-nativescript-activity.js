var MyCustomActivityClass = (function (_super) {
    __extends(MyCustomActivityClass, _super);
    function MyCustomActivityClass() {
        _super.call(this);
        return global.__native(this);
    }
    MyCustomActivityClass.prototype.onCreate = function (savedInstanceState) {
     	_super.prototype.onCreate.call(this, false ? savedInstanceState : null);
     	android.util.Log.d("Sbg.Test","we got called from onCreate of custom-nativescript-activity.js");

        var myIntent = new android.content.Intent(this, com.tns.MyJavaClass.class);
        myIntent.setFlags(android.content.Intent.FLAG_ACTIVITY_NEW_TASK);
        wentToMyJavaClassOnce = true;
        this.startActivity(myIntent);
    };

    MyCustomActivityClass = __decorate([
        JavaProxy("com.tns.NativeScriptActivity")
    ], MyCustomActivityClass);

    return MyCustomActivityClass;
}(android.app.Activity));