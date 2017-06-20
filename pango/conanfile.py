from conans import ConanFile, tools
import os

class PangoConn(ConanFile):
    name = "pango"
    version = "1.40.6"
    license = "LGPL https://git.gnome.org/browse/pango/tree/COPYING"
    url = "https://github.com/trigger-happy/conan-packages"
    description = "A library for layout and rendering text"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    commit = "92cc73c898e4665fd739704417d487d137dd271b"

    def source(self):
        self.run("git clone https://git.gnome.org/browse/pango")
        with tools.chdir("pango"):
            self.run("git checkout {0}".format(self.commit))

    def build(self):
        install_prefix=os.getcwd()
        self.run("mkdir build")
        with tools.chdir("build"):
            self.run("meson ../pango --buildtype=release --prefix={0}".format(install_prefix))
            self.run("ninja install")

    def package(self):
        self.copy("lib/*", dst="lib", keep_path=False)
        self.copy("include/*", dst=".", keep_path=True)

    def package_info(self):
        self.cpp_info.libs = ["pango-1.0", "pangocairo-1.0", "pangoft2-1.0", "pangoxft-1.0"]
