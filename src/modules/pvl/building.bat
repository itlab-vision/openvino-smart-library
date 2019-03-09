mkdir build
cmake  -G"Visual Studio 15 2017 Win64" -Bbuild
cd build
msbuild ALL_BUILD.vcxproj /p:Configuration=Release