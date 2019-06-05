// Copyright 2019 ivanvikhrev
#pragma once
#include <iostream>
#include <fstream>
#include <opencv2/opencv.hpp>
#include <opencv2/pvl.hpp>

extern "C" __declspec(dllexport)
    int Recognize(int rows, int cols, unsigned char* imgData,
                                int* x, int* y, int* w, int* h);
extern "C" __declspec(dllexport) int Register(int rows, int cols,
                                      unsigned char* imgData, int ID);
extern "C" __declspec(dllexport) int UnknownID();
extern "C" __declspec(dllexport) int GetNewID();
extern "C" __declspec(dllexport) void SetDB(char* path);

