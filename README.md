# Smart Library

The applicattion is automated “smart library” based on [OpenVINO toolkit][openvino-toolkit] and pre-trained
models from [Open Model Zoo](OMZ). It involves the registration of the reader; authorization of the reader
through face recognition; receiving and returning books by recognizing QR codes generated for each book in the library.
The following pretrained models for face recognition is used:

* `face-detection-retail-0004`, to detect faces and predict their bounding boxes;
* `landmarks-regression-retail-0009`, to predict face keypoints;
* `face-reidentification-retail-0095`, to recognize readers.

For more information about the pre-trained models, refer to the [model documentation][OMZ-models].

## Demonstration

![](imgs/demo.gif)

### How it works

The application is started from the command line or by using shell script `smart_library_start.bat`.
At application's first run you should register in the `Smart Library` by providing all the necessary information.
To register in the library press `Sign Up` button on the GUI form, fill in necessary fields and press `Accept` button.
There are two roles in the app: regular user and administrator. The latter has access for additional statistics
and is responsible for filling library with new books. To become an administrator fill in `Access code` field when 
registering (default value is `1111`).
After the reader has been registered all infromation about him will be contained in data base, so now user can access
to the library by pressing `Sign In` button. Registration allows receiving and returning books by recognizing
QR codes generated for each book in the library.
For face recognition this app reads video stream frame-by-frame from a web-camera device and performs independent
analysis of each frame. To make predictions it uses 3 models. An input frame is processed by the face detection model
to detect bounding boxes. Then face keypoints are predicted by the facial landmarks regression model.
Keypoints are used to align the face and match it with faces in the database.
To make book recognition press `Get/return book` on the form and scan book's qr-code with the web-camera.
Also application provides information such as list of registered readers, full list of books in the library,
history of borrowing books and more.

### Installation and dependencies

The demo depends on:
- OpenVINO toolkit (2019R3 or newer)
- OpenCV (>=4.1.2-openvino, provided by OpenVINO)
- Python (>=3.6.7, which is supported by OpenVINO)
- PyQt5 (>=5.13.0)
- pyzbar (>=0.1.8)
- qrcode (>=6.1)

To install all the required Python modules you can use:\
'''
pip install -r requirements.txt
'''

### Creating QR-codes for books
Once you've added a new book, qr-code will be generated automatically and placed at [qr-codes folder][qr-codes-folder].

### Running the application

Example of a valid command line to run the application:

Linux (`sh`, `bash`, ...) (assuming OpenVINO installed in `/opt/intel/openvino`):

``` sh
# Set up the environment
source /opt/intel/openvino/bin/setupvars.sh

python ./smart_library.py
```

Windows (`cmd`, `powershell`) (assuming OpenVINO installed in `C:/Program Files (x86)/IntelSWTools/openvino/`):

``` powershell
# Set up the environment
call C:/Program Files (x86)/IntelSWTools/openvino_2019.3.334/bin/setupvars.bat

python smart_library.py
```
Or use script `smart_library_start.bat`.

## See also

* [Console demo of this app][onsole-demo]
* [More Demos][OMZ-demos]

<!-- LINKS -->
[openvino-toolkit]: https://software.intel.com/en-us/openvino-toolkit
[OMZ]: https://github.com/openvinotoolkit/open_model_zoo
[OMZ-models]: https://github.com/openvinotoolkit/open_model_zoo/blob/master/models/intel/index.md
[OMZ-demos]: https://github.com/openvinotoolkit/open_model_zoo/tree/master/demos
[qr-codes-folder]: /qr-codes
[console-demo]: https://github.com/itlab-vision/openvino-smart-library/tree/console-version
