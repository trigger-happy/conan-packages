from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os


class LibpqxxConan(ConanFile):
    name = "libpqxx"
    version = "6.0.0"
    license = "BSD 3 https://github.com/jtv/libpqxx/blob/master/COPYING"
    url = "https://github.com/trigger-happy/conan-packages"
    description = "C++ library for interfacing with postgresql"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    commit = "aeecce843ccd08d8a3c9583aedc788862ba82d4b"

    def source(self):
        self.run("git clone https://github.com/jtv/libpqxx.git")
        with tools.chdir("libpqxx"):
            self.run("git checkout {0}".format(self.commit))

    def configure(self):
        self.requires("libpq/9.6.3@trigger-happy/stable")
        self.options["libpq/9.6.3"].shared = self.options.shared

    def build(self):
        env_build = AutoToolsBuildEnvironment(self)
        install_prefix=os.getcwd()
        shared = "--enabled-shared=yes" if self.options.shared else ""
        with tools.chdir("libpqxx"):
            with tools.environment_append(env_build.vars):
                self.run("./configure --disable-documentation --prefix={0} {1}".format(install_prefix, shared))
                self.run("make install")

    def package(self):
        self.copy("bin/*", dst="bin", keep_path=False)
        self.copy("lib/*", dst="lib", keep_path=False)
        self.copy("include/*", dst=".", keep_path=True)

    def package_info(self):
        self.cpp_info.libs = ["pqxx"]
