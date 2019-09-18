mkdir build
cd build
cmake  -G"Visual Studio 15 2017 Win64" ../
msbuild ALL_BUILD.vcxproj /p:Configuration=Release