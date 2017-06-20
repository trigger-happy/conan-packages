from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os

class LibpqConn(ConanFile):
    name = "libharu"
    version = "2.3.0"
    license = "ZLIB https://github.com/libharu/libharu/blob/master/LICENCE"
    url = "https://github.com/trigger-happy/conan-packages"
    description = "C library for generating PDF documents"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    def source(self):
        pkgLink = 'https://github.com/libharu/libharu/archive/RELEASE_2_3_0.tar.gz'
        self.run("curl -JOL " + pkgLink)
        self.run("tar xf libharu-RELEASE_2_3_0.tar.gz")

    def build(self):
        env_build = AutoToolsBuildEnvironment(self)
        install_prefix=os.getcwd()
        with tools.chdir("libharu-RELEASE_2_3_0"):
            with tools.environment_append(env_build.vars):
                self.run("touch include/config.h.in")
                self.run("aclocal")
                self.run("libtoolize")
                self.run("automake --add-missing")
                self.run("autoconf")
                self.run("./configure --prefix={0}".format(install_prefix))
                self.run("make install")

    def package(self):
        self.copy("lib/*", dst="lib", keep_path=False)
        self.copy("include/*", dst=".", keep_path=True)

    def package_info(self):
        self.cpp_info.libs = ["hpdf"]
