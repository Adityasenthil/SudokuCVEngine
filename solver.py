import cv2
import numpy as np
import json
from tensorflow.keras.models import load_model

model = load_model('model.keras')


def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    puzzle = [[0 for _ in range(9)] for _ in range(9)]
    num_stableframes = 0
    error_margin = 20
    prev_input_pts = np.array([0, 0, 0, 0], dtype=np.float32)
    out = 0
    cell_width = 0
    cell_height = 0

    while True:
        ret, frame = cap.read()
        gray_scale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray_scale, (5,5), 0)
        thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


        maxArea = 0
        sudokuGrid = None
        for cont in contours:
            area = cv2.contourArea(cont)
            height, width = frame.shape[:2]
            minArea = width * height * 0.02
            x,y,w,h = cv2.boundingRect(cont)
            aspect_ratio = float(w)/h
            perimeter = cv2.arcLength(cont, True)
            approx = cv2.approxPolyDP(cont, 0.02 * perimeter, True)
            if area > max(maxArea, minArea) and len(approx) == 4 and aspect_ratio < 1.3:
                maxArea = area
                sudokuGrid = approx

        cv2.drawContours(frame , [sudokuGrid], -1, (255, 255, 0), 5)

        cv2.imshow('frame', frame)

        if sudokuGrid is not None and sudokuGrid.shape[0] == 4:
            pts = sudokuGrid.reshape(4, 2)
            add = pts.sum(axis = 1)
            diff = np.diff(pts, axis = 1)

            top_left = pts[np.argmin(add)]
            bottom_right = pts[np.argmax(add)]
            top_right = pts[np.argmin(diff)]
            bottom_left = pts[np.argmax(diff)]

            height = int(max(np.linalg.norm(top_left - bottom_left), np.linalg.norm(top_right - bottom_right)))
            width = int(max(np.linalg.norm(top_left - top_right), np.linalg.norm(bottom_left - bottom_right)))

            cell_height = height / 9
            cell_width = width / 9

            input_pts = np.array([top_left, top_right, bottom_right, bottom_left], dtype=np.float32)
            
            if (num_stableframes == 0):
                prev_input_pts = input_pts
                num_stableframes += 1
            else:
                error = np.linalg.norm(input_pts - prev_input_pts, axis = 1)
                max_error = np.max(error)  # maxi   

                if max_error < error_margin:
                    num_stableframes += 1
                else:
                    num_stableframes = 1
                    prev_input_pts = input_pts
            
            output_pts = np.array([[0,0], [width, 0], [width, height], [0, height]], dtype = np.float32)
            
            M = cv2.getPerspectiveTransform(input_pts,output_pts)

            out = cv2.warpPerspective(frame, M, (width, height),flags=cv2.INTER_LINEAR)

            if (num_stableframes == 10):
                cap.release()
                cv2.destroyAllWindows()

                break

                
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    for row in range(9):
        for col in range(9): 
            xMin = int(col * cell_width)
            xMax = int(xMin + cell_width)
            yMin = int(row * cell_height)
            yMax = int(yMin + cell_height)
            cell_img = out[yMin:yMax, xMin:xMax]

            gray_cell = cv2.cvtColor(cell_img, cv2.COLOR_BGR2GRAY)
            blur_cell = cv2.GaussianBlur(gray_cell, (3,3), 0)
            _, thresh_cell = cv2.threshold(blur_cell, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))

            clean_cell = cv2.morphologyEx(thresh_cell, cv2.MORPH_OPEN, kernel)
            clean_cell = cv2.resize(clean_cell, (28,28))
            clean_cell = clean_cell.astype("float32") / 255.0

            clean_cell = clean_cell.reshape(1, 28, 28, 1)

            prediction = np.argmax(model.predict(clean_cell))

            puzzle[row][col] = str(prediction)


    with open("last_puzzle.json", "w") as f:
        json.dump(puzzle, f)  

    
        
if __name__ == "__main__":
    main()
