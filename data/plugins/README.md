**inquirer-test-0.0.1.tgz**
Test plugin for https://github.com/NativeScript/nativescript-cli/issues/1610

Scenario:
Plugin add and verify console do not freeze on post-install script.

**plugin-test-variables-1.0.0.tgz**
Test plugin for https://github.com/NativeScript/nativescript-cli/issues/1634

Scenario:
tns plugin add plugin-test-variables-1.0.0.tgz --var.MY-VAR myVariable --var.COLOR "#00FF00"

Assert platforms/android/src/plugin-test-variables contains:
 - AndroidManifest.xml, with following in content: android:label="myVariable">
 - res/values/colors.xml, with following in content: <color name="varcolor">true</color>
 - res/values/strings.xml, with following in content: <string name="myvar">"myVariable"</string>
 
Assert Info.plist in platforms/ios contains:
<dict>
    <key>MY-VAR</key>
    <string>myVariable</string>
    <key>COLOR</key>
    <string>#00FF00</string>
</dict>