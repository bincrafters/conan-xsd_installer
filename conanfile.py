from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os
import glob


class XSDInstallerConan(ConanFile):
    name = "xsd_installer"
    version = "4.0.0"
    description = "XSD is a W3C XML Schema to C++ data binding compiler"
    topics = ("conan", "xsd", "xml", "binding")
    url = "https://github.com/bincrafters/conan-xsd_installer"
    homepage = "https://www.codesynthesis.com/projects/xsd/"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "GPL-2.0-only"
    exports = ["LICENSE.md"]
    exports_sources = ["patches/*.patch"]
    settings = "os_build", "arch_build", "compiler"
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"
    requires = "xerces-c/3.2.2@bincrafters/stable"

    @property
    def _is_mingw_windows(self):
        return self.settings.os_build == "Windows" and self.settings.compiler == "gcc" and os.name == "nt"

    def build_requirements(self):
        if tools.os_info.is_windows and "CONAN_BASH_PATH" not in os.environ:
            self.build_requires("msys2_installer/latest@bincrafters/stable")

    def source(self):
        version_tokens = self.version.split(".")
        major_minor = "%s.%s" % (version_tokens[0], version_tokens[1])
        source_url = "https://www.codesynthesis.com/download/xsd/{}/xsd-{}+dep.tar.bz2".format(major_minor, self.version)
        tools.get(source_url, sha256="eca52a9c8f52cdbe2ae4e364e4a909503493a0d51ea388fc6c9734565a859817")
        extracted_dir = "xsd-%s+dep" % self.version
        os.rename(extracted_dir, self._source_subfolder)

    def build(self):
        for filename in sorted(glob.glob("patches/*.patch")):
            self.output.info('applying patch "%s"' % filename)
            tools.patch(base_path=self._source_subfolder, patch_file=filename)
        # https://www.codesynthesis.com/pipermail/xsd-users/2015-February/004529.html
        tools.replace_in_file(os.path.join(self._source_subfolder, "libxsd-frontend", "xsd-frontend",
                                           "semantic-graph", "elements.cxx"),
                              "#include <algorithm>",
                              "#include <algorithm>\n#include <iostream>")
        with tools.chdir(self._source_subfolder):
            env_build = AutoToolsBuildEnvironment(self, win_bash=tools.os_info.is_windows)
            env_build.make()
            env_build.install(args=["install_prefix=%s" % self.package_folder])

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)

    def package_id(self):
        del self.info.settings.compiler

    def package_info(self):
        bindir = os.path.join(self.package_folder, "bin")
        self.output.info("Appending PATH environment variable: {}".format(bindir))
        self.env_info.PATH.append(bindir)
