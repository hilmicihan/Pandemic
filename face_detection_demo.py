import glob
import os
import cv2
import time
import face_detection


def draw_faces(im, bboxes):
    for bbox in bboxes:
        x0, y0, x1, y1 = [int(_) for _ in bbox]
        cv2.rectangle(im, (x0, y0), (x1, y1), (0, 0, 255), 2)

def extract_faces(im, bboxes,impath):
    index =1
    for bbox in bboxes:
        x0, y0, x1, y1 = [int(_) for _ in bbox]
        face_im=im[y0:y1,x0:x1]
        imname = os.path.basename(impath).split(".")[0]
        output_path = os.path.join(
            os.path.dirname(impath),
            f"{imname,index}_face.jpg"
        )
        cv2.imwrite(output_path, face_im)
        index+=1


if __name__ == "__main__":
    impaths = "images"
    impaths = glob.glob(os.path.join(impaths, "*.jpg"))
    detector = face_detection.build_detector(
        "DSFDDetector",
        max_resolution=2080
    )
    for impath in impaths:
        if impath.endswith("out.jpg"): continue
        if impath.endswith("face.jpg"): continue
        im = cv2.imread(impath)
        print("Processing:", impath)
        t = time.time()
        dets = detector.detect(
            im[:, :, ::-1]
        )[:, :4]
        print(f"Detection time: {time.time()- t:.3f}")
        extract_faces(im,dets,impath) #records faces as single images
	draw_faces(im,dets,impath)    #records images with detected faces
        imname = os.path.basename(impath).split(".")[0]
        output_path = os.path.join(
            os.path.dirname(impath),
            f"{imname}_out.jpg"
        )

        cv2.imwrite(output_path, im)
        