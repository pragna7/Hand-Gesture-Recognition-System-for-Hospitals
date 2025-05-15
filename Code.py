import cv2
import numpy as np
import math

def calculate_distance(pt1, pt2):
    return math.sqrt((pt2[0] - pt1[0]) * 2 + (pt2[1] - pt1[1]) * 2)

def process_frame(frame):
    kernel = np.ones((3, 3), np.uint8)
    
    # Define larger region of interest
    roi = frame[50:350, 50:350]

    cv2.rectangle(frame, (50, 50), (350, 350), (0, 255, 0), 2)
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    # Define range of skin color in HSV
    lower_skin = np.array([0, 20, 70], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)

    # Extract skin color image
    mask = cv2.inRange(hsv, lower_skin, upper_skin)

    # Apply morphological operations to remove noise
    mask = cv2.dilate(mask, kernel, iterations=4)
    mask = cv2.GaussianBlur(mask, (5, 5), 100)

    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Sort contours by area and find the largest one (hand)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:1]

        for cnt in contours:
            # Approximate the contour a little
            epsilon = 0.0005 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)

            # Make convex hull around hand
            hull = cv2.convexHull(cnt)

            # Define area of hull and area of hand
            areahull = cv2.contourArea(hull)
            areacnt = cv2.contourArea(cnt)

            # Find the percentage of area not covered by hand in convex hull
            arearatio = ((areahull - areacnt) / areacnt) * 100

            # Find the defects in convex hull with respect to hand
            hull = cv2.convexHull(approx, returnPoints=False)
            defects = cv2.convexityDefects(approx, hull)

            # l = no. of defects
            l = 0

            if defects is not None:
                # Code for finding no. of defects due to fingers
                for i in range(defects.shape[0]):
                    s, e, f, _ = defects[i, 0]
                    start = tuple(approx[s][0])
                    end = tuple(approx[e][0])
                    far = tuple(approx[f][0])

                    # Find length of all sides of triangle
                    a = calculate_distance(start, end)
                    b = calculate_distance(far, start)
                    c = calculate_distance(end, far)

                    # Calculate the area of triangle using Heron's formula
                    s = (a + b + c) / 2
                    ar = math.sqrt(s * (s - a) * (s - b) * (s - c))

                    # Distance between point and convex hull
                    d = (2 * ar) / a

                    # Apply cosine rule here
                    angle = math.acos((b * 2 + c * 2 - a ** 2) / (2 * b * c)) * 57

                    # Ignore angles > 90 and ignore points very close to convex hull (generally come due to noise)
                    if angle <= 90 and d > 30:
                        l += 1
                        cv2.circle(roi, far, 3, [255, 0, 0], -1)

                    # Draw lines around hand
                    cv2.line(roi, start, end, [0, 255, 0], 2)

            l += 1

            # Print corresponding gestures which are in their ranges
            font = cv2.FONT_HERSHEY_SIMPLEX
            if l == 1:
                if areacnt < 2000:
                    cv2.putText(frame, 'Put hand in the box', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
                else:
                    if arearatio < 12:
                        cv2.putText(frame, '0', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
                    elif arearatio < 17.5:
                        cv2.putText(frame, 'Best of luck', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
                    else:
                        cv2.putText(frame, '1: Call nurse', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
                        print("Gesture: 1 - Call nurse")
            elif l == 2:
                cv2.putText(frame, '2: Need water', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
                print("Gesture: 2 - Need water")
            elif l == 3:
                if arearatio < 27:
                    cv2.putText(frame, '3: Pain relief', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
                    print("Gesture: 3 - Pain relief")
                else:
                    cv2.putText(frame, '3: OK', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
                    print("Gesture: 3 - OK")
            elif l == 4:
                cv2.putText(frame, '4: Call doctor', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
                print("Gesture: 4 - Call doctor")
            elif l == 5:
                cv2.putText(frame, '5: Need help', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
                print("Gesture: 5 - Need help")
            elif l == 6:
                cv2.putText(frame, '6: Turn off light', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
                print("Gesture: 6 - Turn off light")
            elif l == 7:
                cv2.putText(frame, '7: Turn on TV', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
                print("Gesture: 7 - Turn on TV")
            elif l == 8:
                cv2.putText(frame, '8: Turn off TV', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
                print("Gesture: 8 - Turn off TV")
            elif l == 9:
                cv2.putText(frame, '9: Need blanket', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
                print("Gesture: 9 - Need blanket")
            elif l == 10:
                cv2.putText(frame, '10: Need food', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
                print("Gesture: 10 - Need food")
            else:
                cv2.putText(frame, 'reposition', (10, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)

    return mask, frame

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)

    mask, processed_frame = process_frame(frame)

    # Show the windows
    cv2.imshow('mask', mask)
    cv2.imshow('frame', processed_frame)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()
