from conans import ConanFile, AutoToolsBuildEnvironment, tools
import urllib3
import tarfile
import os


class LibxauConan(ConanFile):
    name = "libxau"
    version = "1.0.8"
    license = "Custom https://cgit.freedesktop.org/xorg/lib/libXau/tree/COPYING"
    url = "https://github.com/trigger-happy/conan-packages"
    description = "X11 authorisation library"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    def source(self):
        pkgLink = 'https://xorg.freedesktop.org/releases/individual/lib/libXau-{0}.tar.bz2'.format(self.version)
        fileName = 'libXau-{0}.tar.bz2'.format(self.version)
        pool = urllib3.PoolManager()
        request = pool.request('GET', pkgLink)
        if request.status == 200:
            f = open(fileName, 'w')
            f.write(request.data)
            f.close()
            tf = tarfile.open(fileName)
            tf.extractall('.')
            tf.close()
        else:
            raise Exception('Could not download source file')

    def configure(self):
        self.requires("xproto/7.0.31@trigger-happy/stable")
        self.options["xproto/7.0.31"].shared = self.options.shared

    def build(self):
        envBuild = AutoToolsBuildEnvironment(self)
        installPrefix=os.getcwd()
        shared = "--enable-shared" if self.options.shared else "--disable-shared"
        with tools.chdir("libXau-{version}".format(version=self.version)):
            with tools.environment_append(envBuild.vars):
                self.run("./configure --prefix={0} {1}".format(installPrefix, shared))
                self.run("make install")

    def package(self):
        self.copy("lib/*", dst=".", keep_path=True)
        self.copy("include/*", dst=".", keep_path=True)

    def package_info(self):
        self.cpp_info.libs = ["Xau"]
