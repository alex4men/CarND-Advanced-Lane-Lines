## Writeup
---
**Advanced Lane Finding Project**

The goals / steps of this project are the following:

* Compute the camera calibration matrix and distortion coefficients given a set of chessboard images.
* Apply a distortion correction to raw images.
* Use color transforms, gradients, etc., to create a thresholded binary image.
* Apply a perspective transform to rectify binary image ("birds-eye view").
* Detect lane pixels and fit to find the lane boundary.
* Determine the curvature of the lane and vehicle position with respect to center.
* Warp the detected lane boundaries back onto the original image.
* Output visual display of the lane boundaries and numerical estimation of lane curvature and vehicle position.

[//]: # (Image References)

[image1]: ./output_images/undistort_output.png "Undistorted"
[image2]: ./output_images/straight_lines1_undist.png "Road Transformed"
[image3]: ./output_images/straight_lines1_binary.png "Binary Example"
[image4]: ./output_images/straight_lines1_warped.png "Warp Example"
[image5]: ./output_images/lane_lines_found_resub.png "Fit Visual"
[image6]: ./output_images/result.png "Output"
[image7]: ./output_images/straight_lines1_binary_bad_frame.png "Binary Example"
[image8]: ./output_images/straight_lines1_binary_bad_frame_corr.png "Binary Example"
[image9]: ./output_images/straight_lines1_binary_resub.png "Binary Example"
[image10]: ./output_images/lane_lines_found_bad_frame_corr.png "Fit Visual"

[video1]: ./test_videos_output/project_video.mp4 "Video"

## [Rubric](https://review.udacity.com/#!/rubrics/571/view) Points

### Here I will consider the rubric points individually and describe how I addressed each point in my implementation.  

---

### Writeup / README

#### 1. Provide a Writeup / README that includes all the rubric points and how you addressed each one.  You can submit your writeup as markdown or pdf.  [Here](https://github.com/udacity/CarND-Advanced-Lane-Lines/blob/master/writeup_template.md) is a template writeup for this project you can use as a guide and a starting point.  

You're reading it!

### Camera Calibration

#### 1. Briefly state how you computed the camera matrix and distortion coefficients. Provide an example of a distortion corrected calibration image.

The code for this step is contained in code cells 2-8 of the IPython notebook located in "./Advanced_Lane_Finding.ipynb".  

In the function generateImgPoints() I start by preparing "object points" which will be the (x, y, z) coordinates of the chessboard corners in the world. Here I am assuming the chessboard is fixed on the (x, y) plane at z=0, such that the object points are the same for each calibration image.  Thus, `objp` is just a replicated array of coordinates, and `objpoints` will be appended with a copy of it every time I successfully detect all chessboard corners in a test image.  `imgpoints` will be appended with the (x, y) pixel position of each of the corners in the image plane with each successful chessboard detection.  

I then used the output `objpoints` and `imgpoints` to compute the camera calibration and distortion coefficients using the `cv2.calibrateCamera()` function.  I applied this distortion correction to the test image using the `cv2.undistort()` function and obtained this result:

![alt text][image1]

### Pipeline (single images)

#### 1. Provide an example of a distortion-corrected image.

I applied distortion correction like in the previous case (11th IPython cell). For convenience, I made the function `distortionCorrection(img, K, D)`, which is a simple shortcut to `cv2.undistort()`. Here is the result:
![alt text][image2]

#### 2. Describe how (and identify where in your code) you used color transforms, gradients or other methods to create a thresholded binary image.  Provide an example of a binary image result.

On the first submission I used the combination of saturation, gradient direction and X-gradient magnitude thresholds to generate a binary image (code cells 12 and 14). Here's an example of my output for this step on first submission:

![alt text][image3]

Looks good, but on some frames (with contrast shadows) this filter gave me a lot of wrong activations. Like in this frame:

![alt text][image7]

To improve the quality of lane lines filtering I added filtering in red channel using automatic OTSU thresholding.

![alt text][image8]

The new filter applied to initial frame:

![alt text][image9]

#### 3. Describe how (and identify where in your code) you performed a perspective transform and provide an example of a transformed image.

The code for my perspective transform include code cells 16,17 of the IPython notebook. I chose the hardcode the source and destination points by looking at the lane lines' coordinates in the image and assuming they are straight and parallel. Specially for that I wrote a simple script (`findSrcPts.py`) which opens up the image in matplotlib window and it lets me to see the coordinates of the image under the cursor.

This resulted in the following source and destination points:

| Source        | Destination   |
|:-------------:|:-------------:|
| 594.7, 448.5     | 360.6, 0        |
| 684.8, 448.5     | 944.95, 0      |
| 1074.95, 692.3     | 944.95, 720      |
| 230.6, 692.3      | 360.6, 720       |

I verified that my perspective transform was working as expected by drawing the `src` and `dst` points onto a test image and its warped counterpart to verify that the lines appear parallel in the warped image.

![alt text][image4]

#### 4. Describe how (and identify where in your code) you identified lane-line pixels and fit their positions with a polynomial?

In code cells 19, 20 and 21 I find lane lines in the binary warped image using the function `find_lane_pixels()` and then I fit my lane lines with a 2nd order polynomial using the function `fit_polynomial()` (which implements sliding window approach) kinda like this:

![alt text][image5]

The lane detection applied to the problematic frame.

![alt text][image10]

#### 5. Describe how (and identify where in your code) you calculated the radius of curvature of the lane and the position of the vehicle with respect to center.

I did this in code cells 22, 23 using the function `measure_curvature_real()` I calculate the radius of curvature. This function is similar to `fit_polynomial()`, but it calls the `np.polyfit()` with first two arguments scaled by ym_per_pix = 28/720 and xm_per_pix = 3.7/584 respectively. These coefficients were calculated assuming the lane width is 3.7 meters and each dash and interval between dashes is 3 meters and I had about 9.3*3 = 28 meters of the road in my warped image.

Car position was calculated in the cell 23 by subtracting the absolute image center (640 px) from average lane lines position in the bottom of an image. After multiplying this value by xm_per_pix I got car's offset in meters.

#### 6. Provide an example image of your result plotted back down onto the road such that the lane area is identified clearly.

I implemented this step in code cells 24 through 26 in my code in IPython notebook in the function `project_back()`. Here is an example of my result on the test image with the average curvature and offset printed:

![alt text][image6]

---

### Pipeline (video)

#### 1. Provide a link to your final video output.  Your pipeline should perform reasonably well on the entire project video (wobbly lines are ok but no catastrophic failures that would cause the car to drive off the road!).

Here's a [link to my video result](./test_videos_output/project_video.mp4)

![alt text][video1]

---

### Discussion

#### 1. Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?

To binarize the image I used combination of X-gradient magnitude threshold, gradient direction threshold, saturation and red channel threshold. The first two thresholds finds contrast lane lines edges, close to vertical. And the last threshold finds only high-saturated colors, like white and yellow lane lines. It is hard to tune all the threshold values by hand, filtering quality depends on the scene. Neural networks can help in detecting lane lines better.

To find lane lines I am using sliding window approach. It can fail in situations of multiple contrast lines on the road parallel to the lane lines, and when the lane lines are not so contrast and clear (i.e. under bright sunlight).

If I were going to pursue this project further, I would definitely refactor the code and create the `Line()` class and add some filtration to the algorithm (to make it more robust) and switch to more efficient lane lines search, rather than blindly use sliding window approach.
