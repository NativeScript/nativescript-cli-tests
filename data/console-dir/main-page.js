/*
In NativeScript, a file with the same name as an XML file is known as
a code-behind file. The code-behind is a great place to place your view
logic, and to set up your page’s data binding.
*/

/*
NativeScript adheres to the CommonJS specification for dealing with
JavaScript modules. The CommonJS require() function is how you import
JavaScript modules defined in other files.
*/ 
var createViewModel = require("./main-view-model").createViewModel;

function onNavigatingTo(args) {
    /*
    This gets a reference this page’s <Page> UI component. You can
    view the API reference of the Page to see what’s available at
    https://docs.nativescript.org/api-reference/classes/_ui_page_.page.html
    */
    var page = args.object;

    /*
    A page’s bindingContext is an object that should be used to perform
    data binding between XML markup and JavaScript code. Properties
    on the bindingContext can be accessed using the {{ }} syntax in XML.
    In this example, the {{ message }} and {{ onTap }} bindings are resolved
    against the object returned by createViewModel().

    You can learn more about data binding in NativeScript at
    https://docs.nativescript.org/core-concepts/data-binding.
    */
    page.bindingContext = createViewModel();
    console.log("### TEST START ###");

    var undef;
    var num = -1;
    var str = "text";
    var obj = { name: "John", age: 34 };
    var one_hundred_symbols_string="1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890"
    var very_long_string = "";

    for (i = 0; i < 30; i++) {
        very_long_string = very_long_string + one_hundred_symbols_string;
    }

    console.dir(true);
    console.dir(false);
    console.dir(null);
    console.dir(undef);

    console.dir(num);
    console.dir(str);

    console.dir(obj);

    console.dir(very_long_string);

    console.log("### TEST END ###");
}

/*
Exporting a function in a NativeScript code-behind file makes it accessible
to the file’s corresponding XML file. In this case, exporting the onNavigatingTo
function here makes the navigatingTo="onNavigatingTo" binding in this page’s XML
file work.
*/
exports.onNavigatingTo = onNavigatingTo;