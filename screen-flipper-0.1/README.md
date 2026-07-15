# Screen Flipper
A simple Linux app for flipping your display orientation from a small GUI.

## Install
1. Install Python and PyQt5.
2. Open the project folder in a terminal.
3. Run:

```bash
chmod +x install.sh
./install.sh
```

This adds the app to your launcher and installs the icon.

## Use
- Open Screen Flipper from your application menu.
- Click the button to flip the screen.
- Click it again to restore the normal orientation.

## Run manually
If you want to start it without installing:

```bash
python3 screen-flipper.py
```

## Notes
- The app tries to use the primary connected display automatically.
- If your system does not support the default method, it will fall back to another available display tool.

