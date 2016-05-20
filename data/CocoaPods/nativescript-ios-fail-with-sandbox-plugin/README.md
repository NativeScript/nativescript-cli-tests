# nativescript-ios-fail-with-sandbox-plugin
Plugin used for testing sandbox-pod and pod support in nativescript-cli.
This plugin will try to create file called `I_MADE_THIS_FILE.txt` in `<project_name>/platforms` directory.

## How to use

### NativeScript CLI:
In your project execute:
```
$ tns plugin add https://github.com/rosen-vladimirov/nativescript-ios-fail-with-sandbox-plugin/tarball/master
```

or add the following entry in your `package.json`


```JSON
"dependencies": {
	"nativescript-ios-fail-with-sandbox-plugin": "https://github.com/rosen-vladimirov/nativescript-ios-fail-with-sandbox-plugin/tarball/master"
}
```

### AppBuilder
Add the following entry in your `package.json`


```JSON
"dependencies": {
	"nativescript-ios-fail-with-sandbox-plugin": "https://github.com/rosen-vladimirov/nativescript-ios-fail-with-sandbox-plugin/tarball/master"
}
```

### AppBuilder CLI
In your project execute:
```
$ appbuilder plugin add https://github.com/rosen-vladimirov/nativescript-ios-fail-with-sandbox-plugin/tarball/master
```

or add the following entry in your `package.json`


```JSON
"dependencies": {
	"nativescript-ios-fail-with-sandbox-plugin": "https://github.com/rosen-vladimirov/nativescript-ios-fail-with-sandbox-plugin/tarball/master"
}
```

## Expected result when building the project

### NativeScript CLI
In the default scenario the build should fail with some sandbox-pod error.
In case you open `<cli_install_dir>/config/config.json` and set `USE_POD_SANDBOX` to `false`, the build will succeed.
When the build succeeds, you will find file called `I_MADE_THIS_FILE.txt` inside `<project_name>/platforms` directory.

### AppBuilder
The build will fail with some sandbox-pod error.
