from conans import ConanFile, AutoToolsBuildEnvironment, tools
import urllib3
import tarfile
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
        pkgLink = 'https://xorg.freedesktop.org/releases/individual/proto/inputproto-{0}.tar.bz2'.format(self.version)
        fileName = 'inputproto-{0}.tar.bz2'.format(self.version)
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

    def build(self):
        envBuild = AutoToolsBuildEnvironment(self)
        installPrefix=os.getcwd()
        shared = "--enable-shared" if self.options.shared else "--disable-shared"
        with tools.chdir("inputproto-{version}".format(version=self.version)):
            with tools.environment_append(envBuild.vars):
                self.run("./configure --prefix={0} {1}".format(installPrefix, shared))
                self.run("make install")

    def package(self):
        self.copy("lib/*", dst=".", keep_path=True)
        self.copy("include/*", dst=".", keep_path=True)

    def package_info(self):
        self.cpp_info.libs = []
