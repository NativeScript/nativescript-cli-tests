module.exports = (function() {
    var hello;
    var bye;
    (function() {
        if (!hello) {
            hello = Hello.alloc().init();
        }
        if (!bye) {
            bye = Bye.alloc().init();
        }
    })();

    var resultingObject = {
        sayHi: function() {
            hello.printHello();
        },
        sayBye: function() {
            bye.printBye();
        }
    };
    return resultingObject;
})();
