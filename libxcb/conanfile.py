from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os


class LibxcbConan(ConanFile):
    name = "libxcb"
    version = "1.12"
    license = "Custom https://cgit.freedesktop.org/xcb/libxcb/tree/COPYING"
    url = "https://github.com/trigger-happy/conan-packages"
    description = "X11 client-side library"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    def source(self):
        pkgLink = 'https://xcb.freedesktop.org/dist/libxcb-{version}.tar.bz2'.format(version=self.version)
        self.run("curl -JOL " + pkgLink)
        self.run("tar xf libxcb-{version}.tar.bz2".format(version=self.version))

    def build(self):
        envBuild = AutoToolsBuildEnvironment(self)
        installPrefix=os.getcwd()
        with tools.chdir("libxcb-{version}".format(version=self.version)):
            with tools.environment_append(envBuild.vars):
                self.run("./configure --prefix={0} --enable-xinput --enable-xkb".format(installPrefix))
                self.run("make install")

    def package(self):
        self.copy("lib/*", dst=".", keep_path=True)
        self.copy("include/*", dst=".", keep_path=True)

    def package_info(self):
        self.cpp_info.libs = ["xcb", "xcb-composite", "xcb-damage", "xcb-dpms", "xcb-dri2", "xcb-dri3", "xcb-glx", "xcb-present", "xcb-randr", "xcb-record", "xcb-res", "xcb-screensaver", "xcb-shape", "xcb-shm", "xcb-sync", "xcb-xf86dri", "xcb-xfixes", "xcb-xinerama", "xcb-xinput", "xcb-xkb", "xcb-xtest", "xcb-xv"]
