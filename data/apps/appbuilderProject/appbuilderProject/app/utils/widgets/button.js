'use strict';
function onLoaded(args) {
    var button = args.object.getViewById('button');

    if (button) {
        button.text = args.object.text;
    }
}

exports.onLoaded = onLoaded;
