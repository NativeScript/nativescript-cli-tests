function getExtendedClasses() {
    var ExtendedClass = java.lang.Object.extend({

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