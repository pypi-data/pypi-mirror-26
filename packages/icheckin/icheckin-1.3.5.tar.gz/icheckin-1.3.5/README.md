# icheckin [![PyPI](https://img.shields.io/pypi/v/icheckin.svg)](https://pypi.python.org/pypi/icheckin) [![Travis](https://img.shields.io/travis/chunkhang/icheckin.svg)](https://travis-ci.org/chunkhang/icheckin) [![Code Climate](https://img.shields.io/codeclimate/github/chunkhang/icheckin.svg)](https://codeclimate.com/github/chunkhang/icheckin)

A simple CLI for Sunway University's iCheckin. Quickly check-in your attendance using your laptop without the hassle of using iZone or the official mobile applications. 

## Requirement

#### One must have [Python](https://www.python.org/) to begin with
- Python 2
   - 2.6
   - 2.7
- [Python 3](http://www.diveintopython3.net/installing-python.html) (Recommended)
   - 3.3
   - 3.4
   - 3.5
   - 3.6

## Installation

##### Install using [pip](https://pip.pypa.io/en/stable/quickstart/)
```
$ pip install icheckin
```

## Usage

##### Available commands
```
$ icheckin
Usage: icheckin [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  add     add to existing credentials
  clear   clear all credentials
  code    check-in with code
  remove  remove credentials
  save    save new credentials
  show    show saved credentials
  update  check for updates
```

##### Save credentials
```
$ icheckin save
```

##### Check-in for yourself
```
$ icheckin code 12345
```

##### Check-in for multiple credentials
```
$ icheckin code --multi 12345
```

## Updates

##### Check for updates
```
$ icheckin update
Checking for updates...
Up to date.
```

##### Fetch latest update
```
$ pip install --upgrade icheckin
```

## Releases

### 1.3.0
* Massive architectural overhaul
* Commands have been revamped completely
* Now supports multiple check-in
* Delete ~/.icheckin-credentials if things are not working out

##### 1.3.1
* Fixed problem with checking updates

##### 1.3.2
* Credentials to remove is now okay

##### 1.3.3
* You can now know whether you have already checked-in or in the wrong class

##### 1.3.4
* Check your current version (icheckin update)

##### 1.3.5
* New spinners when checking in and checking for updates
* Color has arrived

---

### 1.2.0
* Checking for updates is now significantly faster
* You can now save your credentials to avoid logging in every time
* Check out the command-line tools (icheckin -h)

##### 1.2.1
* Code housekeeping
* -c (--credentials) is now -s (--save)
* Changes to help details

---

### 1.1.0
* Will now check whether you are connected SunwayEdu Wi-Fi before submitting check-in code
* Improved code checking
* Automatically checks for updates

---

### 1.0.0
* Initial release

##### 1.0.1
* Nothing much

##### 1.0.2
* Some cleaning up

##### 1.0.3
* Aesthetics

##### 1.0.4
* Connection problems can now be handled with grace

## Contact

Feel free to report bugs or suggest features. <br/>
**[Marcus Mu](http://marcusmu.me)** - chunkhang@gmail.com