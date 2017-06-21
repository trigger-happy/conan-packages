from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os


class LibxdmcpConan(ConanFile):
    name = "libxdmcp"
    version = "1.1.2"
    license = "Custom https://cgit.freedesktop.org/xorg/lib/libXdmcp/tree/COPYING"
    url = "https://github.com/trigger-happy/conan-packages"
    description = "X11 Display Manager Control Protocol library"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    def source(self):
        pkgLink = 'https://xorg.freedesktop.org/releases/individual/lib/libXdmcp-{version}.tar.bz2'.format(version=self.version)
        self.run("curl -JOL " + pkgLink)
        self.run("tar xf libXdmcp-{version}.tar.bz2".format(version=self.version))

    def build(self):
        envBuild = AutoToolsBuildEnvironment(self)
        installPrefix=os.getcwd()
        with tools.chdir("libXdmcp-{version}".format(version=self.version)):
            with tools.environment_append(envBuild.vars):
                self.run("./configure --prefix={0}".format(installPrefix))
                self.run("make install")

    def package(self):
        self.copy("lib/*", dst=".", keep_path=True)
        self.copy("include/*", dst=".", keep_path=True)

    def package_info(self):
        self.cpp_info.libs = ["Xdmcp"]
