import os, string, random, cv2, requests

BASE_PATH = os.path.abspath(os.path.dirname("."))
VID_UPLOAD_PATH = os.path.join(BASE_PATH, "uploads/inmates_videos")
FACE_SAMPLE_PATH = os.path.join(BASE_PATH, "assets/faces/")
PRETRAINED_PATH = os.path.join(BASE_PATH, "assets/pretrained/", "haarcascade_frontalface_alt2.xml")

def randomword(length):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))

def split_from_videos(videos, sampledirname):
    capture = cv2.VideoCapture(videos)
    SAMPLE_DIR = os.path.join(FACE_SAMPLE_PATH, sampledirname)
    if not os.path.exists(SAMPLE_DIR):
        os.makedirs(SAMPLE_DIR)
    r = requests.get("https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_alt2.xml")
    f = open(PRETRAINED_PATH, 'w')
    f.write(r.text)
    frameNr = 0
    while (True):
        success, frame = capture.read()
        if success:
            original = f'{SAMPLE_DIR}/{sampledirname}_{frameNr}.jpg'
            if not os.path.exists(original):
                cv2.imwrite(original, frame)
                img = cv2.imread(original)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                face_cascade = cv2.CascadeClassifier(PRETRAINED_PATH)
                faces = face_cascade.detectMultiScale(gray, 1.1, 4)
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
                    faces = img[y:y + h, x:x + w]
                    cv2.imwrite(original, faces)
                print(f"{sampledirname}_{frameNr}.jpg berhasil di simpan!")
        else:
            break
        frameNr = frameNr+1
    capture.release()
    print(f"{frameNr}, files berhasil di split!")
    return frameNr