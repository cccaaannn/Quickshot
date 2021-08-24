## Compiling and packaging on windows
---

## Tested compile environment
- Python 3.7.6
- PyInstaller 4.3

## Known lib version problems
- `pynput==1.7.3` causes import error when compiled. [stackoverflow](https://stackoverflow.com/questions/63681770/getting-error-when-using-pynput-with-pyinstaller)
- `pyqt5>=5.15.0` causes some resizing problems, use `pyqt5==5.14.2`

## Compile
- Before compiling switch `build_for` to `windows_installer` or `windows_msix` on the `main.py` file.
- PyInstaller uses all paths relative to spec file path. [github](https://github.com/pyinstaller/pyinstaller/issues/3333)
- Run commands from the project's root folder.

From scratch
```shell
python -m PyInstaller --noconsole --specpath bin\windows\spec --distpath bin\windows\dist --workpath bin\windows\build --name Quickshot --add-data "..\..\..\Quickshot\cfg;cfg" --add-data "..\..\..\Quickshot\statics;statics" --noconfirm --icon="..\..\..\Quickshot\statics\icons\Qs.ico" Quickshot\main.py
```
With spec file
```shell
python -m PyInstaller --distpath bin\windows\dist --workpath bin\windows\build --noconfirm bin\windows\spec\Quickshot.spec
```

---

## Package win32 installer
- Download [inno setup](https://jrsoftware.org/isinfo.php)
- Change `ApplicationRootPath` in `Quickshot_setup.iss`.
- Run inno setup with `Quickshot_setup.iss`.

---

## Package msix installer
- Download [packaging-tool](https://docs.microsoft.com/en-us/windows/msix/packaging-tool/tool-overview)
- Create a Certificate
```powershell
New-SelfSignedCertificate -Type Custom -Subject "CN=can-kurt, O=can-kurt, C=TR" -KeyUsage DigitalSignature -FriendlyName "Can Kurt" -CertStoreLocation "Cert:\LocalMachine\My"
$pwd = ConvertTo-SecureString –String <password> –Force –AsPlainText
Export-PfxCertificate -cert “Cert:\LocalMachine\My\<Certificate Thumbprint>” -FilePath quickshot_certificate.pfx -Password $pwd
```
- Use packaging-tool to package installer.
- Add timeserver `http://timestamp.digicert.com`
