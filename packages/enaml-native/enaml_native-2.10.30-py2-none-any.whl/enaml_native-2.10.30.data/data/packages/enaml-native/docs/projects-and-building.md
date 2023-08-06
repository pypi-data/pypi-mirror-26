### Project structure

An enaml-native app is organized similar to a react-native app.

The project directory consists of the basic structure:
  
    :::python
    android/      #: Android project using gradle
    ios/          #: iOS xcode project with cocoapods
    src/          #: Python source for your app 
    packages/     #: Enaml-native packages
    package.json  #: Project config
    enaml-native  #: Symlink to cloned enaml-native cli

This structure is created for you using a modified copy of the example project when you run `./enaml-native init <name> <bundle_id> <destination>`. Your actual apps are in the `android` and `ios` folders. The build scripts are configured to run an enaml-native command that packages your python source files as required for the app.

### Configuring the project

The `package.json` file is your project config. If you open it you see the following.
    
    :::json
    {
      "name": "Enaml-Native Demo",
      "bundle_id":"com.codelv.enamlnative.demo",
      "version": "1.8",
      "private": true,
      "sources": [
        "src/apps/playground",
        "src"
      ],
      "android": {
        "ndk":"~/Android/Crystax/crystax-ndk-10.3.2",
        "sdk":"~Android/Sdk",
        "arches": ["x86"],
        "dependencies": {
          "python2crystax": "2.7.10",
          "enamlnative": ">=2.1",
          "tornado": ">=4.0",
          "singledispatch":">=0",
          "backports_abc":">=0",
          "ply": "==3.10"
        },
        "excluded":[]
      },
      "ios": {
        "project": "demo",
        "arches": [
          "x86_64",
          "i386",
          "armv7",
          "arm64"
        ],
        "dependencies": {
          "openssl":"1.0.2l",
          "python":"2.7.13",
          "tornado": ">=4.0",
          "singledispatch": ">=0",
          "backports_abc": ">=0",
          "ply": "==3.10"
        },
        "excluded":[]
      }
    }


As you can see there's a few shared properties such as `name`, `bundle_id`, and `version` which are self explanitory, 
`sources`, and separate configs for `ios` and `android`. 

The `sources` list is a list of the source folders that the build system will copy into 
the __root__ of your python app. It does a recursive copy so any files, folders, subfolders, and files 
within will be added into your will be available on the actual app. You can add images, data files, etc.. it doesn't care.

Each platform config (`ios` and `android`) has `arches`, `dependencies`, and `excluded`. The rest are specfic for the platform.

As you may have guessed, `arches` defines which platforms to compile python and extensions modules for and `dependencies` is 
a list of python requirements to install on the app. Pure python requirements are installed via pip, anything with compiled
extensions _MUST_ have a recipe for the specific platform. More on that later. 

The `excluded` list is a list of [patterns](https://docs.python.org/2.7/library/glob.html) that you can use to exclude unused python modules from your app to reduce the app size.

For android there's `sdk` and `ndk` which are the paths used for building you MUST update these to point to 
wherever your's is installed. 

For ios there's the `project` which defines the name of the `<project>.xcworkspace` that will be built.

If you're interested you can read through the [enaml-native cli](https://github.com/codelv/enaml-native/blob/master/enaml-native) source which 
is what actually uses this config file.

### Build process

The build process depends on the platfom but from a high level the following must occur.

1. Python dependencies must be cross compiled for the target platfom and arches for each platform.
2. App python source, site-packages, and the standard library must be "bundled" to be included in the native app
3. The native app build system (gradle, xcode) must be configured to include the bundled python and any linked with compiled libraries. 
4. Native build system builds the app and uses python via native hooks and [the bridge](https://www.codelv.com/projects/enaml-native/docs/bridge).

> See [enaml-native packages](#enamlnativepackages)

### Building python

The `package.json` config file defines an `arches` list for each platfom. This is the list of ABI's or target platforms to build your python and extensions for. 

> This is very complicated internally and only supported by OSX and linux! 
> Note: You can skip this by downloading and including precompiled libraries. Links to come see issue [#22](https://github.com/codelv/enaml-native/issues/22)

To cross compile python and modules for different arches you must:

1. Add or remove from the config `arches` list
2. Run `./enaml-native clean-python`
3. Run `./enaml-native build-python`

This will rebuild for both Android and iOS (if applicable). 
If you want to restrict building to only one or the other (on OSX only) pass the flag `--ios` or `--android`.

Python builds are done using modified versions of [python-for-android](https://github.com/kivy/python-for-android/) and [kivy-ios](https://github.com/kivy/kivy-ios/). 
The python build process is VERY complicated and prone to errors on new installs due to the various system dependencies.  

These modifed projects are included within this project.

I've been thinking about making a server to do this for you or perhaps creating a VM or docker image that is pre-configured.


### Release your app

It's easiest to just make release builds using android-studio or xcode. It will prompt you do do any configuration necessary.

Once that is done you can then do release builds with the enaml-native cli using `./enaml-native build-android --release` 
or `./enaml-native build-ios --release`. The `--release` flag tells it to do a release build (it's debug by default). 

For help see the documentation for each platform, enaml-native does nothing special here.


### Android specifics

You can open the `android` folder in Android studio and it will load like any normal android project. 
This way you can easily modify any native java code and get all the highlighting and error checking, etc. 
all android documentation applies here. The project uses the gradle build system.  

#### Building for Android

The android build process is done in two phases.

1. Build CPython and compiled extensions  for each arch via `./enaml-native build-python`
2. Gradle hook to bundle all pure python app source, the standard library,  and site-packages. 

##### Building python and compiled extensions for Android

enaml-native builds python and any dependencies that have compiled components (c, c++, cython) 
using a fork of [python-for-android](https://github.com/codelv/enaml-native/tree/master/python-for-android).

This fork is modified as follows:

1. Added python2crystax support and uses the prebuilt python 2.7 from the [crystax NDK](https://www.crystax.net/)
1. Added an enaml bootstrap
1. Modified several recipies to work with enaml-native

Building is invoked with `./enaml-native build-python` in [enaml-native](https://github.com/codelv/enaml-native/blob/master/enaml-native)
based on the config file. This calls ndk-build on the [native hooks](https://github.com/codelv/enaml-native/blob/master/packages/enaml-native/android/src/main/jni) 
and then does a p4a's build to compile python and any recipes.  

Once done all of your libraries will go to the jni libs folder `packages/enaml-native/android/src/main/libs/<arch>`. 
All modules here will be included in the app by gradle (see [build.gradle](https://github.com/codelv/enaml-native/blob/master/packages/enaml-native/android/build.gradle#L24)).

> Note: Libraries matching the pattern `lib*.so` are automatically copied during the App intall on the device. This speeds up the startup. Any modules NOT matching this need copied manually in your app's main activity.


The entire build process is complicated and very issue prone. I'm hoping to be able to make this easier this by
providing a build server to compile libraries for you.

> Note: If you want to add a dependency that has a compiled component it MUST have a recipe! You can create your own if one is missing

These compiled modules are then imported using a custom import hook, see [import_hooks.py](https://github.com/codelv/enaml-native/blob/master/src/enamlnative/core/import_hooks.py).

##### Bundling python for Android

enaml-native hooks itself into the gradle build process to include your python source and libraries.
This hook is in [packages/enaml-native/build.grade](https://github.com/codelv/enaml-native/blob/master/packages/enaml-native/android/build.gradle).

It simply runs `./enaml-native bundle-assets` which packages all the python and app source code into a zip 
and copies it to `android/app/src/main/assets/python/python.zip`. 

> Note: This hook does NOT include python or any extensions ONLY pure python assets! See above for building extensions.

#### Adding libraries with Gradle

To add custom libraries:

1. Open the project in android-studio 
2. Modify the `android/app/build.gradle` as needed.  
3. Run gradle sync (should prompt you when you make a change) and it will collect your new libraries

You can see there's a few already being used. Once a library is added with gradle you can use it via making
a wrapper Proxy and Toolkit component (see the [native component](https://www.codelv.com/projects/enaml-native/docs/native-components) docs) .


### iOS specifics

You can open the project.xcworkspace within the `ios` folder in xcode and work in your app normally. All iOS
docs apply here.

The android build process is done in two phases.

1. Build CPython and compiled extensions  for each arch via `./enaml-native build-python`
2. Gradle hook to bundle all pure python app source, the standard library,  and site-packages. 

#### Building for iOS

The iOS build process is done in two phases.

1. Build CPython and compiled extensions  for each arch via `./enaml-native build-python`
2. A Build Phase hook to bundle all pure python app source, the standard library, and site-packages. 

##### Building python and compiled extensions for iOS

enaml-native builds python and any dependencies that have compiled components (c, c++, cython) 
using a fork of [kivy-ios](https://github.com/codelv/enaml-native/tree/master/python-for-ios).

This fork is __heavily__ modified as follows:

1. All builds were converted to create dylibs (Min iOS version is set to 8)
2. Python updated to 2.7.13
3. Added and modified several recipies to work with enaml-native

Building is invoked with `./enaml-native build-python` in [enaml-native](https://github.com/codelv/enaml-native/blob/master/enaml-native)
based on the config file. This calls `python-for-ios/toolchain.py` build internally.

The entire build process is complicated and very issue prone. I'm hoping to be able to elimnate this entriely by
providing a build server to compile libraries for you.

> Note: As of this writing I have NOT submitted an app to the App Store

These compiled modules are then imported using a custom import hook, see [import_hooks.py](https://github.com/codelv/enaml-native/blob/master/src/enamlnative/core/import_hooks.py).

There's a few blog posts on what exactly was changed that may help you when building new recipies [on my blog](http://blog.codelv.com).


#### Adding libraries with CocoaPods

To add custom libraries:

1. Modify the `ios/<app>/Podfile` as needed
2. cd to `ios/<app>` and run `pod install` or `pod update`
3. Rebuild your xcode project

You can see there's a few already being used. Once a library is added with cocopods you can use it via making
a wrapper Proxy and Toolkit component (see the [native component](https://www.codelv.com/projects/enaml-native/docs/native-components) docs) .

That's all for now! Thanks for reading! Please suggest more docs if something is confusing.



### Enaml-native packages

Because `enaml-native` is growing and apps will typically want to only include the native dependencies they need. 

The project was redesigned and broken down into installable `EnamlPackages` with separate requirements.

This is to address issues python-for-android is having with non-reproducible builds due to recipes linking to master versions.

It is also a step making it more like react-native which does package management very well.

> Note: This is VERY early development and will probably change 

The concept is pretty simple. 

1. Each "app" project will have it's own `venv` with the `enaml-native-cli` installed.
2. You install your apps `enaml package` dependencies or regular pip dependencies
3. The enaml-native build process will install the python "sub" packages and any recipes included. 


#### Package format

A package is simply a directory with the following subdirectories and files.

    :::python
    android/          #: Android library using gradle (if applicable)
    android/recipes/  #: python-for-android recipes (if applicable)
    ios/              #: iOS xcode library with cocoapods (if applicable)
    ios/recipes/      #: python-for-ios recipes (if applicable)
    src/              #: Python source for your app 
    src/setup.py      #: Setupfile for your package's source 
    setup.py          #: Pip setup file for the enaml-native package
    

To make an "enaml-package" that follows this format use: 
`./enaml-native init-package <some-package-name> <destination/folder>`




