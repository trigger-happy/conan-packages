from conans import ConanFile, CMake
import urllib3
import tarfile

class FltkConan(ConanFile):
    name = "FLTK"
    version = "1.3.4"
    license = "GNU LGPL with exceptions (http://www.fltk.org/COPYING.php)"
    url = "https://github.com/trigger-happy/conan-packages"
    description = "FLTK widget library for C++"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    def source(self):
        fileName = 'fltk-{0}-1-source.tar.gz'.format(self.version)
        sourceUrl = 'http://fltk.org/pub/fltk/1.3.4/fltk-{0}-1-source.tar.gz'.format(self.version)
        pool = urllib3.PoolManager()
        request = pool.request('GET', sourceUrl)
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
        self.requires("libxcb/1.12@trigger-happy/stable")
        self.requires("pcre/8.40.0@kmaragon/stable")
        self.requires("graphite/1.3.10@trigger-happy/stable")
        self.options["libxdmcp/1.1.2"].shared = self.options.shared
        self.options["libxau/1.0.8"].shared = self.options.shared
        self.options["libxcb/1.12"].shared = self.options.shared
        self.options["pcre/8.40.0"].shared = self.options.shared
        self.options["graphite/1.3.10"].shared = self.options.shared

    def build(self):
        cmake = CMake(self.settings)
        shared = "-DBUILD_SHARED_LIBS=ON" if self.options.shared else ""
        self.run('cmake fltk-1.3.4-1 %s %s' % (cmake.command_line, shared))
        self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("FL", dst="include", src="fltk-1.3.4-1")
        self.copy("lib/*", dst="lib", keep_path=False)
        self.copy("bin/fluid", dst="bin", keep_path=False)
        self.copy("bin/fltk-config", dst="bin", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["fltk", "fltk_images", "fltk_gl", "fltk_forms"]
