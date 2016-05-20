Static Libraries
================

{N} CLI supports only static libraries built for all required architectures (universal* libraries).

**hello-plugin** contains an universal library

**bye-plugin** contains a non-universal library

*universal* - a library is called universal when it is build for all required architectures:
- iOS Devices - armv7 and arm64,
- (OS X) iOS Simulators - i386 and х86_64.

In order to determinate if your lib is universal or not:

`lipo -i <path_to_staticLib.a>`
