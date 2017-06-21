from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os


class InputprotoConan(ConanFile):
    name = "inputproto"
    version = "2.3.2"
    license = "Custom https://cgit.freedesktop.org/xorg/proto/inputproto/tree/COPYING"
    url = "https://github.com/trigger-happy/conan-packages"
    description = "X11 Input extension wire protocol"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    def source(self):
        pkgLink = 'https://xorg.freedesktop.org/releases/individual/proto/inputproto-{version}.tar.bz2'.format(version=self.version)
        self.run("curl -JOL " + pkgLink)
        self.run("tar xf inputproto-{version}.tar.bz2".format(version=self.version))

    def build(self):
        envBuild = AutoToolsBuildEnvironment(self)
        installPrefix=os.getcwd()
        with tools.chdir("inputproto-{version}".format(version=self.version)):
            with tools.environment_append(envBuild.vars):
                self.run("./configure --prefix={0}".format(installPrefix))
                self.run("make install")

    def package(self):
        self.copy("lib/*", dst=".", keep_path=True)
        self.copy("include/*", dst=".", keep_path=True)

    def package_info(self):
        self.cpp_info.libs = []
