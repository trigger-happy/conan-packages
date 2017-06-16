from conans import ConanFile, CMake


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
        self.run("curl -JOL http://fltk.org/pub/fltk/1.3.4/fltk-1.3.4-1-source.tar.gz")
        self.run("tar xf fltk-1.3.4-1-source.tar.gz")
        self.run("cd fltk-1.3.4-1")

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
