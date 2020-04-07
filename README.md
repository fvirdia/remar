# Remar	🚣‍♀️

![Screenshot](/screenshots/main_window.png?raw=true "Remar's main window")

Remar is a toy reMarkable cloud GUI alternative to the official reMarkable app.

## Why

While it is possible to run the official app through Wine, my personal experience is that the automatic updater crashes it, forcing me to reinstall the app every time I want to use it.

## Bugs and Features

The aim of Remar would be to imitate all the functionailty of the official client. Currently, only a small subset of features is supported:

- Navigating the cloud file system
- Uploading PDF files
- Bookmarking files and directories
- Moving, renaming, deleting files and directories
- Searching for filenames

## Install

The app is distributed as source, or as an AppImage that you can fetch from [Releases](https://github.com/fvirdia/remar/releases). Electron currently (wisely) runs in sandboxed mode by default. Yet, some versions of Debian and Ubuntu do not support this out of the box. In that case, running the binary with `--no-sandbox` as option should solve the issue.

It should also be possible to repackage the app to run on macOS and Windows, although I have not tried that.

## Build form source

Install [Yarn](https://yarnpkg.com/).

To fetch dependencies, run 
```
yarn
```

To run the app as a developer, run
```
yarn start
```

To generate the AppImage binary, run
```
yarn dist
```

## License

Remar is MIT licensed. 

In particular, I would like to stress the LICENSE disclaimer that there is no warranty of any kind that the client won't screw up your files, either on your personal computer, on the cloud, or anywhere else.