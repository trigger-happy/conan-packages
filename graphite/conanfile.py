from conans import ConanFile, CMake
import urllib3
import tarfile
import os


class GraphiteConan(ConanFile):
    name = "graphite"
    version = "1.3.10"
    license = "LGPL, GPL and Custom https://github.com/silnrsi/graphite/blob/master/LICENSE"
    url = "https://github.com/trigger-happy/conan-packages"
    description = "Reimplementation of the SIL Graphite text processing engine"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    def source(self):
        pkgLink = 'https://github.com/silnrsi/graphite/releases/download/{0}/graphite2-{0}.tgz'.format(self.version)
        fileName = 'graphite2-{0}.tgz'.format(self.version)
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
        installPrefix=os.getcwd()
        cmake = CMake(self.settings)
        shared = "-DBUILD_SHARED_LIBS=ON" if self.options.shared else ""
        self.run('cmake graphite2-%s %s %s -DCMAKE_INSTALL_PREFIX=%s' % (self.version, cmake.command_line, shared, installPrefix))
        self.run("cmake --build . %s --target install" % cmake.build_config)

    def package(self):
        self.copy("lib/*", dst=".", keep_path=True)
        self.copy("include/*", dst=".", keep_path=True)

    def package_info(self):
        self.cpp_info.libs = ["graphite2"]
