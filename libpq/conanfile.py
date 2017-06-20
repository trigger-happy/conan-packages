from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os

class LibpqConn(ConanFile):
    name = "libpq"
    version = "9.6.3"
    license = "PostgreSQL license https://www.postgresql.org/about/licence/"
    url = "https://github.com/trigger-happy/conan-packages"
    description = "C library for interfacing with postgresql"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    def source(self):
        pkgLink = 'https://ftp.postgresql.org/pub/source/v{pkgver}/postgresql-{pkgver}.tar.bz2'.format(pkgver=self.version)
        self.run("curl -JOL " + pkgLink)
        self.run("tar xf postgresql-{pkgver}.tar.bz2".format(pkgver=self.version))

    def build(self):
        env_build = AutoToolsBuildEnvironment(self)
        install_prefix=os.getcwd()
        with tools.chdir("postgresql-{pkgver}".format(pkgver=self.version)):
            with tools.environment_append(env_build.vars):
                self.run("./configure --with-openssl --without-readline --prefix={0}".format(install_prefix))
                with tools.chdir("src/interfaces/libpq"):
                    self.run("make install")

    def package(self):
        self.copy("lib/*", dst="lib", keep_path=False)
        self.copy("include/*", dst=".", keep_path=True)

    def package_info(self):
        self.cpp_info.libs = ["pq"]
