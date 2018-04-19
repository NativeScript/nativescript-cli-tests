function getExtendedClasses() {
    var ExtendedClass = android.view.View.MeasureSpec.extend({

    });

    return {
        ExtendedClass
    };
}

function getExtendedClassInstance() {
    var Clazz = getExtendedClasses().ExtendedClass;
    var instance;

    instance = new Clazz();

    return instance;
}

module.exports = {
    getExtendedClasses,
    getExtendedClassInstance
}