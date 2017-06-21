from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os


class Libx11Conan(ConanFile):
    name = "libx11"
    version = "1.6.5"
    license = "Custom https://cgit.freedesktop.org/xorg/lib/libX11/tree/COPYING"
    url = "https://github.com/trigger-happy/conan-packages"
    description = "X11 client-side library"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    def source(self):
        pkgLink = 'https://xorg.freedesktop.org/releases/individual/lib/libX11-{version}.tar.bz2'.format(version=self.version)
        self.run("curl -JOL " + pkgLink)
        self.run("tar xf libX11-{version}.tar.bz2".format(version=self.version))

    def build(self):
        envBuild = AutoToolsBuildEnvironment(self)
        installPrefix=os.getcwd()
        with tools.chdir("libX11-{version}".format(version=self.version)):
            with tools.environment_append(envBuild.vars):
                self.run("./configure --prefix={0} --disable-xf86bigfont".format(installPrefix))
                self.run("make install")

    def package(self):
        self.copy("lib/*", dst=".", keep_path=True)
        self.copy("include/*", dst=".", keep_path=True)

    def package_info(self):
        self.cpp_info.libs = ["X11", "X11-xcb"]
