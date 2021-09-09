## Compiling and packaging on Linux
---

## Tested compile environment
- Python 3.8.10
- PyInstaller 4.4

## Known lib version problems
- `pynput==1.7.3` causes import error when compiled. [stackoverflow](https://stackoverflow.com/questions/63681770/getting-error-when-using-pynput-with-pyinstaller)
- `pyqt5>=5.15.0` causes some resizing problems, use `pyqt5==5.14.2`

## Compile
- Before compiling switch `build_for` to `linux_appimage` on the `main.py` file.
- PyInstaller uses all paths relative to spec file path. [github](https://github.com/pyinstaller/pyinstaller/issues/3333)
- Run commands from the project's root folder.

From scratch
```shell
python -m PyInstaller --noconsole --specpath bin/linux/spec --distpath bin/linux/dist --workpath bin/linux/build --name Quickshot --add-data "../../../Quickshot/cfg:cfg" --add-data "../../../Quickshot/statics:statics"  --noconfirm --icon="../../../Quickshot/statics/icons/Qs.ico" Quickshot/main.py
```
With spec file
```shell
python -m PyInstaller --distpath bin/linux/dist --workpath bin/linux/build --noconfirm bin/linux/spec/Quickshot.spec
```

---

## Package
- Download [appimagetool](https://appimage.github.io/appimagetool/).
- Move compiled binaries to `Quickshot.AppDir/usr/bin`.
- Run `appimagetool` with `Quickshot.AppDir` directory.
```shell
ARCH=x86_64 ./appimagetool-x86_64.AppImage bin/linux/Quickshot.AppDir
```
