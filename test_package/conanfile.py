from conans import ConanFile, tools
import os


class TestPackageConan(ConanFile):

    def test(self):
        if not tools.cross_building(self):
            self.run("xsd --version")
