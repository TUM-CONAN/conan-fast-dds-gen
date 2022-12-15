from conans import ConanFile, CMake, tools


class FastDDSConan(ConanFile):
    name = "Fast-DDS-GEN"
    version = "2.2.0"
    license = "Apache License 2.0"
    author = "Frieder Pankratz"
    url = "https://github.com/TUM-CONAN/conan-fast-dds-gen.git"
    description = "Conan wrapper for Fast-DDS-GEN"    
    settings = "os"
    options = {"shared": [True, False], "Build_Java" : [True, False]}
    default_options = {"shared": True, "Build_Java" : False } #, "RPCProto" : "rpcdds"}
    generators = "cmake"

    exports_sources = "CMakeLists.txt", "cmake/*"

    build_requires = (
        "zulu-openjdk/11.0.15",
        )

    def source(self):
        git = tools.Git()        
        git.clone("https://github.com/eProsima/Fast-DDS-Gen.git", "master")#%self.version)

            

    def _configure_cmake(self):        
        cmake = CMake(self)
        cmake.verbose = True

        def add_cmake_option(option, value):
            var_name = "{}".format(option).upper()
            value_str = "{}".format(value)
            var_value = "ON" if value_str == 'True' else "OFF" if value_str == 'False' else value_str
            cmake.definitions[var_name] = var_value        

        for option, value in self.options.items():
            add_cmake_option(option, value)

        cmake.configure()
        return cmake

    def build(self):
        #cmake = self._configure_cmake()
        #cmake.build()
        if tools.os_info.is_windows:
            self.run("gradlew.bat assemble")
        else:
            self.run("./gradlew assemble")

    def package(self):
        #cmake = self._configure_cmake()
        #cmake.install()
        
        self.copy(src="build/libs", pattern="*.jar", dst="share/fastddsgen/java",keep_path=False)
        self.copy(src="", pattern="LICENSE", dst="share/",keep_path=False)
        self.copy(src="scripts", pattern="*", dst="bin",keep_path=False)
        pass

    def package_info(self):        
        #self.cpp_info.libs = tools.collect_libs(self)
        pass
