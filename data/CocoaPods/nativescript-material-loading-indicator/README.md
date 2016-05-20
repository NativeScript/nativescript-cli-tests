# NativeScript Material design activity indicator for iOS

Following the material design loading indicator for Android, this plugin provides the same look and feel for iOS.

## Prerequisites
NativeScript 1.3.0 (`tns --version`) has solved many build issues, so please upgrade if you need to.

## Installation
From the command prompt go to your app's root folder and execute:
```
tns plugin add nativescript-material-loading-indicator
```

## Usage

```js
function creatingView(args) {

  var spinnerView = MMMaterialDesignSpinner.alloc().initWithFrame(CGRectMake(0,0,40,40));
    spinnerView.lineWidth = 1.5;
    spinnerView.tintColor = UIColor.redColor();

    spinnerView.startAnimating();
    args.view = spinnerView;

}

exports.creatingView = creatingView;
```

```xml
<Page xmlns="http://www.nativescript.org/tns.xsd">
      <Placeholder creatingView="creatingView"/>
</Page>
```