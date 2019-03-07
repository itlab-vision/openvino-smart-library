#include "pvl.hpp"

using namespace cv;
using namespace std;
using namespace cv::pvl;

static int counter = 0;
static Ptr<FaceDetector> pvlFD;
static Ptr<FaceRecognizer> pvlFR;
static bool isOpen = false;
static string dbPath = "defaultdb.xml";

void GetPath(char* path) {
	dbPath = (string)path;
}

int Register(int rows, int cols, unsigned char* imgData, int ID) {
    //const string& dbPath = "defaultdb.xml";
    
    if (counter == 0) {
        pvlFD = FaceDetector::create();
        
		if (pvlFD.empty()){
            cerr << "Error: fail to create PVL face detector" << endl;
            return -1;
        }
        
		pvlFR = FaceRecognizer::create();
        if (pvlFR.empty()){
            cerr << "Error: fail to create PVL face recognizer" << endl;
            return -2;
        }
        bool bTracking = false;

        pvlFD->setTrackingModeEnabled(bTracking);
        pvlFR->setTrackingModeEnabled(bTracking);

        if (std::ifstream(dbPath)){
            pvlFR = Algorithm::load<FaceRecognizer>(dbPath);
            isOpen = true;
        }
    }

    Mat img(rows, cols, CV_8UC3, imgData);

    if (img.empty()){
        cerr << "Error: no input image" << endl;
        return -3;
    }

    Mat imgGray;
    cvtColor(img, imgGray, COLOR_BGR2GRAY);
    if (imgGray.empty()){
        cerr << "Error: no gray image()" << endl;
        return -4;
    }

    int keyDelay = 0;
    bool bTracking = false;
    int personID = FACE_RECOGNIZER_UNKNOWN_PERSON_ID;


    vector<Face> faces;
    vector<int>  personIDs;
    vector<int>  confidence;

    faces.clear();
    personIDs.clear();
    confidence.clear();

    pvlFD->detectFaceRect(imgGray, faces);
    if (faces.size() == 1 ){   
        pvlFR->recognize(imgGray, faces, personIDs, confidence);
        
        for (uint i = 0; i < personIDs.size(); i++)
            if (personIDs[i] == FACE_RECOGNIZER_UNKNOWN_PERSON_ID){
                personID = ID;
                pvlFR->registerFace(imgGray, faces[i], personID, true);
                pvlFR->save(dbPath);
                pvlFR = Algorithm::load<FaceRecognizer>(dbPath);
            }

    }

    return personID;
}

int Recognize(int rows, int cols, unsigned char* imgData, int* x, int* y, int* w, int* h) {
    //const string& dbPath = "defaultdb.xml";
   
	if (counter == 0) {
        pvlFD = FaceDetector::create();

        if (pvlFD.empty()){
            cerr << "Error: fail to create PVL face detector" << endl;
            return -1;
        }
        pvlFR = FaceRecognizer::create();

        if (pvlFR.empty()){
            cerr << "Error: fail to create PVL face recognizer" << endl;
            return -2;
        }
        bool bTracking = true;// ?
        pvlFD->setTrackingModeEnabled(bTracking);// ?
        pvlFR->setTrackingModeEnabled(bTracking);// ?
        
        if (std::ifstream(dbPath)){
            pvlFR = Algorithm::load<FaceRecognizer>(dbPath);
            isOpen = true;
        }
    }

    if (std::ifstream(dbPath) && isOpen == false)
        pvlFR = Algorithm::load<FaceRecognizer>(dbPath);
    else
        isOpen = true;

    Mat img(rows, cols, CV_8UC3, imgData);
    if (img.empty()){
        cerr << "Error: no input image" << endl;
        return -3;
    }

    Mat imgGray;
    cvtColor(img, imgGray, COLOR_BGR2GRAY);
    if (imgGray.empty()){
        cerr << "Error: no gray image()" << endl;
        return -4;
    }

    int keyDelay = 0;
    int personID = FACE_RECOGNIZER_UNKNOWN_PERSON_ID;
    
    vector<Face> faces;
    vector<int>  personIDs;
    vector<int>  confidence;

    faces.clear();
    personIDs.clear();
    confidence.clear();

    pvlFD->detectFaceRect(imgGray, faces);
    if (faces.size() == 1)
    {
        pvlFR->recognize(imgGray, faces, personIDs, confidence);
        if (personIDs.size() > 0) {
            personID = personIDs[0];
        }
        Face& face = faces[0];
        Rect faceRect = face.get<Rect>(Face::FACE_RECT);
        *x = faceRect.x;
        *y = faceRect.y;
        *w = faceRect.width;
        *h = faceRect.height;
    }
    counter++;
    return personID;
}


int UnknownID()
{
    return FACE_RECOGNIZER_UNKNOWN_PERSON_ID;
}
