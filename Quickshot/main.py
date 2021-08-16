from Quickshot_builder import Quickshot_builder

build_for = "dev"
# build_for = "windows_installer"
# build_for = "windows_msix"
# build_for = "linux_appimage"

if __name__ == '__main__':
    Qshot_builder = Quickshot_builder()
    Qshot_builder.build(build_for)
