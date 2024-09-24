# ScreenCapper

Here we have *yet another* screencap tool.  Initially, it was just going to be a basic "grab the whole screen" type of thing, but it was fun, so I just kept going.  
  
## A Powerful Screenshot Tool for Linux 😁

**ScreenCapper** was written in Python. Sitting in your system tray like a beloved pet, it empowers you to capture specific areas of your screen and save them as images. Woof!

### Features

* Capture full screenshots or select smaller regions for precise capturing.
* System tray icon for easy access without cluttering your desktop.
* Audio cues for capture and successful/failed saves to provide feedback.
* The tool remembers the last directory used for image saving, defaulting to your ~/Pictures directory.

### Installation

**Prerequisites:**

* Python 3 ([https://www.python.org/downloads/](https://www.python.org/downloads/))

**Dependencies:**

This application relies on the following Python libraries:

* PySide6 (`pip install pyside6`)
* pyautogui (`pip install pyautogui`)
* Pillow (PIL Fork) (`pip install Pillow`)

**Installation Steps:**

1. Open a terminal window and navigate to the directory containing the `screenshot_tool.py` script.
2. Install the required libraries using pip:

```bash
    pip install pyside6 pyautogui Pillow
```

### Usage

1. Run the script using the following command:

```bash
    python screenshot_tool.py
```

**Tips:**

* Left-click on the ScreenCapper icon in the system tray to capture a screenshot.
* Right-click on the ScreenCapper icon in the system tray to access a menu with  options to capture a screenshot, view info about the app, and quit.
* The tool remembers the last used save directory for convenient image saving.

### Contributing

We appreciate any contributions to improve ScreenCapper! Feel free to fork the repository, make changes, and submit a pull request.

### Media Attribution

Please read [this](Media_Attribution_ScreenCapper.md).

# Thanks

<p>Ryon Shane Hall</p>
<br>
endorpheus@gmail.com<br>
[ryonshanehall.com](http://ryonshanehall.com)
