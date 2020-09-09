import requests

print('Beginning file download with requests')

path = 'src/infrastructure/Resources/'
baseUrl = 'https://download.01.org/opencv/2020/openvinotoolkit/2020.4/open_model_zoo/models_bin/1/'
fd = 'face-detection-retail-0004'
lm = 'landmarks-regression-retail-0009'
rd = 'face-reidentification-retail-0095'
fd_model = baseUrl + 'face-detection-retail-0004/FP32/' + fd
lm_model = baseUrl + 'landmarks-regression-retail-0009/FP32/' + lm
rd_model = baseUrl + 'face-reidentification-retail-0095/FP32/' + rd

# face detection model
r = requests.get(fd_model + '.bin')
with open(path + fd + '.bin', 'wb') as f:
    f.write(r.content)
r = requests.get(fd_model + '.xml')
with open(path + fd + '.xml', 'wb') as f:
    f.write(r.content)

# landmarks regression model
r = requests.get(lm_model + '.bin')
with open(path + lm + '.bin', 'wb') as f:
    f.write(r.content)
r = requests.get(lm_model + '.xml')
with open(path + lm + '.xml', 'wb') as f:
    f.write(r.content)

# face reindetification model
r = requests.get(rd_model + '.bin')
with open(path + rd + '.bin', 'wb') as f:
    f.write(r.content)
r = requests.get(rd_model + '.xml')
with open(path + rd + '.xml', 'wb') as f:
    f.write(r.content)