import os
from conan import ConanFile
from conan.tools.scm import Git
from conan.tools.files import update_conandata, copy, chdir, collect_libs
from conan.tools.layout import basic_layout
from conan.tools.env import Environment

class FastDDSConan(ConanFile):
    name = "fast-dds-gen"
    version = "2.4.0"
    package_type = "application"
    license = "Apache License 2.0"
    author = "Frieder Pankratz"
    url = "https://github.com/TUM-CONAN/conan-fast-dds-gen.git"
    description = "Conan wrapper for Fast-DDS-GEN"    

    settings = "os"
    generators = "VirtualBuildEnv"
    no_copy_source = True

    def build_requirements(self):
        self.build_requires("zulu-openjdk/11.0.15")

    def export(self):
        update_conandata(self, {"sources": {
            "commit": "v{}".format(self.version),
            "url": "https://github.com/eProsima/Fast-DDS-Gen.git"
            }}
            )

    def source(self):
        git = Git(self)
        sources = self.conan_data["sources"]
        git.clone(url=sources["url"], target=self.source_folder, args=["--recursive", ])
        git.checkout(commit=sources["commit"])

    def generate(self):
        env = Environment()
        return env

    def layout(self):
        basic_layout(self, src_folder="source_subfolder")

    def build(self):
        with chdir(self, self.source_folder):
            if self.settings.os == "Windows":
                self.run("gradlew.bat assemble")
            else:
                self.run("./gradlew assemble")

    def package_id(self):
        self.info.clear()

    def package(self):
        copy(self, pattern="*.jar",
             dst=os.path.join(self.package_folder, "share", "fastddsgen", "java"),
             src=os.path.join(self.source_folder, "build", "libs"),
             keep_path=False)
        copy(self, pattern="*",
             dst=os.path.join(self.package_folder, "bin"),
             src=os.path.join(self.source_folder, "scripts"),
             keep_path=False)
        copy(self, pattern="LICENSE",
             dst=os.path.join(self.package_folder, "licenses"),
             src=self.source_folder)

    def package_info(self):
        self.cpp_info.includedirs = []
        self.cpp_info.libdirs = []
        self.buildenv_info.append_path("PATH", os.path.join(self.package_folder, "bin"))
        self.runenv_info.append_path("PATH", os.path.join(self.package_folder, "bin"))