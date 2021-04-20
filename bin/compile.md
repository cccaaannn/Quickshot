## Compile info
---

## Compile environment
- Python 3.7.6
- PyInstaller 4.3
- Before compiling switch `is_dev` to False on the `main.py` file.
- Icon's path is relative to spec file path. <a href="https://github.com/pyinstaller/pyinstaller/issues/3333">github</a>

## Known lib version problems
- `pynput==1.7.3` causes import error when compiled. <a href="https://stackoverflow.com/questions/63681770/getting-error-when-using-pynput-with-pyinstaller">stackoverflow</a>
- `pyqt5>=5.15.0` causes some resizing problems, use `pyqt5==5.14.2`

## Compile with
From scratch
```shell
python -m PyInstaller --noconsole --specpath bin\spec --distpath bin\dist --workpath bin\build --name Quickshot --add-data "..\..\Quickshot\cfg;cfg" --add-data "..\..\Quickshot\icons;icons" --noconfirm --icon="..\..\Quickshot\icons\Qs.ico" Quickshot\main.py
```
With .spec file
```shell
python -m PyInstaller --distpath bin\dist --workpath bin\build --noconfirm bin\spec\Quickshot.spec
```
