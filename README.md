# Quickshot
#### A simple, portable, customizable screenshot tool.
___

![GitHub top language](https://img.shields.io/github/languages/top/cccaaannn/Quickshot?style=flat-square) ![](https://img.shields.io/github/repo-size/cccaaannn/Quickshot?style=flat-square) [![GitHub license](https://img.shields.io/github/license/cccaaannn/Quickshot?style=flat-square)](https://github.com/cccaaannn/Quickshot/blob/master/LICENSE) [![GitHub release](https://img.shields.io/github/v/release/cccaaannn/Quickshot?style=flat-square)](https://github.com/cccaaannn/Quickshot/releases?style=flat-square)

## Check out [Quickshot website](https://cccaaannn.github.io/Quickshot)

## Features
- **Fast**, no more choosing save path or name every time.
- **Easy to use**, simple ui single button.
- **Customizable**, check [Settings](#Settings).
- **Portable**, all required files in one folder on a path that you choose. check [versions](#versions).

<br/>

## Custom color Quickshot examples

<img src="docs/src/images/example1.png" alt="drawing" width="250"/><img src="docs/src/images/example2.png" alt="drawing" width="250"/>
<br/>
<img src="docs/src/images/example3.png" alt="drawing" width="250"/><img src="docs/src/images/example4.png" alt="drawing" width="250"/>
<br/>
<img src="docs/src/images/example5.png" alt="drawing" width="250"/><img src="docs/src/images/example6.png" alt="drawing" width="250"/>
<br/>
<img src="docs/src/images/example7.png" alt="drawing" width="250"/><img src="docs/src/images/example8.png" alt="drawing" width="250"/>
<br/>

## Settings
Quickshot has several customization options.

- Background, accent color and opacity customization.
- Hotkey customization.
- Multi screen support for full screen screenshots.
- Clipboard support.
- Screenshot save customizations
    - Save name and path.
    - Options for screenshot numbering.
    - Date formatting.
    - Locale date naming.
    - jpg and png support.

<br/>
<img src="docs/src/images/settings_example1.png" alt="drawing" width="400"/><img src="docs/src/images/settings_example2.png" alt="drawing" width="400"/>
<br/>
<br/>


## Versions

## Windows
- win32 installer
    - This version has an **option** for adding shortcut to context menu, if selected you can not move the installation folder.
- msix installer
    - msix packages needs to use another folder for saving settings since they can not be changed, this version saves settings to `C:\Users\USER\.Quickshot`.
- portable
    - Portable version without installer.


## Linux

- AppImage | [appimage.org](https://appimage.org/)
    - AppImages needs to use another folder for saving settings since they can not be changed, this version saves settings to `/HOME/USER/.Quickshot`.
    - Extra dependencies
        - Clipboard function requires [xclip](https://github.com/astrand/xclip) to be installed on Linux.
    - Known issues
        - Scaling display causes coordinate problems on screenshots on kde plasma but works on gnome 🤷🏻‍♂️.  
        - Some long animations causes Quickshot's frame to be visible on screenshots, use `Window invisibility time` option for delaying screenshot (or disable display compositor). 
