# Code written by Mohammed Abbas Ansari for OCR Internship Assignment (IIT Bombay)
# Github: m-abbas-ansari

import cv2
import os
import numpy as np
import json
from pdf2image import convert_from_path

path_to_pdf = 'Sanskrit_Text.pdf'
pages = convert_from_path(path_to_pdf, 500) # reading pdf pages as images
json_dict = {}
count_box = 1
for i, page in enumerate(pages):
	os.makedirs(f'page_{i+1}', exist_ok=True)
	page = np.array(page) # allowing the page to be read for opencv
	gray = cv2.cvtColor(page, cv2.COLOR_RGB2GRAY) # converting page img to grayscale
	ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV) # otsu thresholding
	rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (80, 2)) 
	# the rectangle size will determine the area of bounding box to detect text

	# Applying dilation on the threshold image
	dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)
	 
	# Finding contours
	contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
	for cnt in contours:
	    x, y, w, h = cv2.boundingRect(cnt)
	    if w < 400 or h < 70: # reject bounding boxes that are too small 
	    	continue
	    
	    json_dict[f'box{count_box}'] = {'top_left': [x,y], 'top_right': [x+w, y], 'bottom_left': [x, y+h], 'bottom_right': [x+h, y+h]} 
	   	
	    cropped_line = page[y: y+h, x: x+w]

	    # saving jpg
	    cv2.imwrite(f'page_{i+1}/box_{count_box}.jpg', cv2.cvtColor(cropped_line, cv2.COLOR_RGB2BGR))
	    count_box += 1
	    
	    # # Drawing a rectangle on page on detected text
	    # page = cv2.rectangle(page, (x, y), (x + w, y + h), (0, 255, 0), 2)
	
# saving json dictionary as file
with open('result.json', 'w') as fp:
    json.dump(json_dict, fp)