

import numpy as np
import cv2
from mss import mss

# Parameters
bounding_box = {'top': 44, 'left': 0, 'width': 300, 'height': 500}
filterTolerance = 100
sct = mss()

while True:
  frame = np.array(sct.grab(bounding_box))
  grey = cv2.cvtColor(frame, cv2.COLOR_BGRA2GRAY)
  edges = cv2.Canny(grey, 150, 350, 5)

  # # Detect points that form a line
  # lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=1, maxLineGap=250)
  # # Draw lines on the image
  # if lines is not None:
  #   for line in lines:
  #       x1, y1, x2, y2 = line[0]
  #       cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)

  raw_lines = cv2.HoughLines(edges,1,np.pi/180,65)
  lines = []
  if raw_lines is not None:
      for raw_line in raw_lines:
          rho,theta = raw_line[0]
          a = np.cos(theta)
          b = np.sin(theta)
          x0 = a*rho
          y0 = b*rho
          x1 = int(x0 + 1000*(-b))
          y1 = int(y0 + 1000*(a))
          x2 = int(x0 - 1000*(-b))
          y2 = int(y0 - 1000*(a))

          if abs(x1-x2) < abs(y1-y2):
            cv2.line(frame,(x1,y1),(x2,y2),(0,0,255),2)

            insert = True
            for line in lines:
              print(line[0] + line[1] + line[2] + line[3], x1+y1+x2+y2, (line[0] + line[1] + line[2] + line[3]) - (x1+y1+x2+y2))
              if abs((line[0] + line[1] + line[2] + line[3]) - (x1+y1+x2+y2)) < filterTolerance:
                insert = False
            
            if insert:
              lines.append((x1,y1,x2,y2))

  cv2.imshow('screen', frame)
  # cv2.imshow('edges', edges)

  if (cv2.waitKey(1) & 0xFF) == ord('q'):
      cv2.destroyAllWindows()
      break