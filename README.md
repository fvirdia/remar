# Remar	🚣‍♀️

![Screenshot](/screenshots/main_window.png?raw=true "Remar's main window")

Remar is a toy reMarkable cloud GUI alternative to the official reMarkable app. Remar is written in wxPython, and powered by the [rMAPI](https://github.com/juruen/rmapi) backend.

## Why

While it is possible to run the official app through Wine, my personal experience is that the automatic updater crashes it, forcing me to reinstall the app every time I want to use it.

## Bugs and Features

Remar currently lets you navigate your reMarkable cloud, upload files, and extract them. Extraction of files has the same limitations that rMAPI has.

The whole experience will be particularly slow if your internet connection is poor. The reason being that for every single interaction, Remar launches a new instance or rMAPI, rather than using a single CLI process all along.
While the api in `rmapi.py` would in principle allow to keep a single rMAPI instance open (making operations much faster), interacting with a CLI via standard input/output parsing can be unreliable, and I don't want to risk screwing up the files stored on the cloud.

Unreliability of text parsing is also the reason why I did not implement any "destructive" operations, such as "move", "rename" or "delete".

## Dependencies
- [rMAPI](https://github.com/juruen/rmapi) 0.0.9, already authenticated with your cloud,
- [Python](https://www.python.org/) 3.5+ (really, one just needs async/await support),
- [wxPython](https://wxpython.org/) for the ui,
- [wxasync](https://github.com/sirk390/wxasync) for async/await support in wxPython.

## How to install

The following instructions were tested on a Xubuntu 18.04 clean install, but should probably apply to most Debian derivatives/easily translate to other distributions.

Install wxPython:
```
$ sudo apt install python3-wxgtk4.0
```

Install wxasync (pip is the easiest way, but not the only one): 
```
$ sudo apt install python3-pip # in case you don't already have pip
$ sudo pip3 install wxasync
```

Get a copy of rMAPI 0.0.9:
```
$ wget https://github.com/juruen/rmapi/releases/download/v0.0.9/rmapi-linuxx86-64.tar.gz
$ tar xf rmapi-linuxx86-64.tar.gz
```

At this point you should have a local copy of the `rmapi` binary. Copy it into some directory that is part of your `PATH` (for now, will probably get around to making this optional later), so that you can run it from anywhere by just typing `rmapi`.

Now, run `rmapi` for the first time in your command line. It will ask you a reMarkable one-time code to authenticate to the cloud, follow the instructions there.

Finally, get a copy of Remar, and run it. For example:
```
$ git clone https://github.com/fvirdia/remar
$ cd remar
$ chmod +x remar.py
$ ./remar.py
```

Of course, once everything is running, one can can create a desktop launcher pointing at `remar.py`, or add a symlink to `remar.py` somewhere in your `PATH`.

## Future

I'm happy for someone more competent with desktop application development to pick up my slack and improve/clone/fork/steal Remar and run with it. 
Personally, I would love to see a Python wrapper for rMAPI, so that each interaction could be implemented as a function call, rather than having to wrap their CLI. Then I would feel comfortable adding more functionality to the app, and the performance would also likely improve.

Having a better interface to rMAPI would also possibly allow someone to write a FUSE driver for the reMarkable cloud, which would probably be the preferable solution for using the reMarkable with Linux.

## License

Remar is GPL3 licensed. It currently uses icons from the Tango Icon Library project, and wraps the [rMAPI](https://github.com/juruen/rmapi) command line client.

In particular, I would like to stress the LICENSE disclaimer that there is no warranty of any kind that the client won't screw up your files, either on your personal computer, on the cloud, or anywhere else.