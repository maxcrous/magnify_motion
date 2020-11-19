# Eulerian Video Magnification 
This repository contains a reproduction of [Eulerian Video Magnification for Revealing Subtle Changes in the World](http://people.csail.mit.edu/mrub/evm/#code). It is meant as an accessible implementation with low complexity that can be used as an aid for studying the algorithm.

## File structure 
| Name                    | Purpose                                                                           |
|-------------------------|-----------------------------------------------------------------------------------|
| filters.py              | Ideal, Buttersworth and iir signal filters                                        |
| pyramids.py             | Image dimension agnostic Laplacian and Guassian pyramid building functions        |
| motion_magnify.py       | The main function used to create a motion or color magnified video.               |
| reproduce_paper.py      | Runs experiments for the video files hosted on the paper's website                |

## Results
| Authors results | This repo results|
| --------------- | ---------------- |
| ![](gifs/output_authors/baby1.gif) | ![](gifs/output/baby1.gif)  |
| ![](gifs/output_authors/shadow.gif)  | ![](gifs/output/shadow.gif)  |
| ![](gifs/output_authors/face1.gif)  | ![](gifs/output/face1.gif)  |


