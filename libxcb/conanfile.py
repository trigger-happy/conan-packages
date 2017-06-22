from conans import ConanFile, AutoToolsBuildEnvironment, tools
import urllib3
import tarfile
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
        pkgLink = 'https://xcb.freedesktop.org/dist/libxcb-{0}.tar.bz2'.format(self.version)
        fileName = 'libxcb-{0}.tar.bz2'.format(self.version)
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
        self.requires("libxdmcp/1.1.2@trigger-happy/stable")
        self.requires("libxau/1.0.8@trigger-happy/stable")
        self.options["libxdmcp/1.1.2"].shared = self.options.shared
        self.options["libxau/1.0.8"].shared = self.options.shared

    def build(self):
        envBuild = AutoToolsBuildEnvironment(self)
        installPrefix=os.getcwd()
        shared = "--enable-shared" if self.options.shared else "--disable-shared"
        with tools.chdir("libxcb-{version}".format(version=self.version)):
            with tools.environment_append(envBuild.vars):
                self.run("./configure --prefix={0} --enable-xinput --enable-xkb {1}".format(installPrefix, shared))
                self.run("make install")

    def package(self):
        self.copy("lib/*", dst=".", keep_path=True)
        self.copy("include/*", dst=".", keep_path=True)

    def package_info(self):
        self.cpp_info.libs = ["xcb", "xcb-composite", "xcb-damage", "xcb-dpms", "xcb-dri2", "xcb-dri3", "xcb-glx", "xcb-present", "xcb-randr", "xcb-record", "xcb-res", "xcb-screensaver", "xcb-shape", "xcb-shm", "xcb-sync", "xcb-xf86dri", "xcb-xfixes", "xcb-xinerama", "xcb-xinput", "xcb-xkb", "xcb-xtest", "xcb-xv"]
