import os
from cvzone.HandTrackingModule import HandDetector
import cv2

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 360)

inst = cv2.imread("Resources/instruct/inst.png")
cv2.imshow("Instructions", inst)
print("Enter key")
while True:

    # Wait for the user to press a key
    key = cv2.waitKey(1) & 0xFF
    if key == 13:
        cv2.destroyAllWindows()
        imgBackground = cv2.imread("Resources/mcd.png")

        # importing all the mode images to the list
        folderPathModes = "Resources/Modes"
        listImgModesPath = os.listdir(folderPathModes)
        listImgModes = []
        for imgModePath in listImgModesPath:
            listImgModes.append(cv2.imread(os.path.join(folderPathModes, imgModePath)))

        print(listImgModes)

        # importing all the icons to the list
        folderPathIcons = "Resources/Icons"
        listImgIconsPath = os.listdir(folderPathIcons)
        listImgIcons = []
        for imgIconsPath in listImgIconsPath:
            listImgIcons.append(cv2.imread(os.path.join(folderPathIcons, imgIconsPath)))

        # for changing selection mode
        modeType = 0
        selection = -1
        counter = 0
        selectionSpeed = 5

        # Detecting hand
        detector = HandDetector(detectionCon=0.8, maxHands=1)
        modePositions = [(1242, 196), (990, 365), (1242, 535)]
        counterPause = 0
        selectionList = [-1, -1, -1]

        while True:
            success, img = cap.read()
            # Find the hand and its landmarks
            hands, img = detector.findHands(img)  # with draw

            # overlaying the webcam feed on the background image
            imgBackground[142:142+360, 68:68+640] = img

            imgBackground[0:661, 865:1365] = listImgModes[modeType]

            if hands and counterPause == 0 and modeType < 3:

                # Hand 1
                hand1 = hands[0]
                fingers1 = detector.fingersUp(hand1)
                print(fingers1)

                if fingers1 == [0, 1, 0, 0, 0]:
                    if selection != 1:
                        counter = 1
                    selection = 1
                elif fingers1 == [0, 1, 1, 0, 0]:
                    if selection != 2:
                        counter = 1
                    selection = 2
                elif fingers1 == [0, 1, 1, 1, 0]:
                    if selection != 3:
                        counter = 1
                    selection = 3
                else:
                    selection = -1
                    counter = 0
                    print("wrong finger")

                if counter > 0:
                    counter += 1

                    cv2.ellipse(imgBackground, modePositions[selection-1], (100, 100), 0, 0,
                                counter * selectionSpeed, (100, 255, 0, 20), 20)
                    if counter*selectionSpeed > 360:
                        selectionList[modeType] = selection
                        modeType += 1
                        counter = 0
                        selection = -1
                        counterPause = 1

            # to pause after each selection is made
            if counterPause > 0:
                counterPause += 1
                if counterPause > 60:
                    counterPause = 0

            # add selection icon at the bottom
            if selectionList[0] != -1:
                imgBackground[575:575+50, 107:107+50] = (listImgIcons[selectionList[0] - 1])

            if selectionList[1] != -1:
                imgBackground[575:575 + 50, 360:360 + 50] = (listImgIcons[selectionList[1] + 2])

            if selectionList[2] != -1:
                imgBackground[575:575 + 50, 610:610 + 50] = listImgIcons[selectionList[2] + 5]

            # Displaying
            cv2.imshow("image", img)
            cv2.imshow("Background", imgBackground)
            cv2.waitKey(1)

