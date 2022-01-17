# Eulerian Video Magnification 
This repository contains a reproduction of [Eulerian Video Magnification for Revealing Subtle Changes in the World](http://people.csail.mit.edu/mrub/evm/#code). It is meant as an accessible implementation with low complexity that can be used as an aid for studying the algorithm.

## How to run 
Video files are not included in this repository due to licensing. 
If you want to reproduce the paper with `reproduce_paper.py`, you will need to download the videos from the [author's website](https://people.csail.mit.edu/mrub/evm/#code). 
 
Install the dependencies by running `pip install -r requirements.txt`.     
Then, run `python reproduce_paper.py`.

Magnifying a 10-second video can take up to a minute on an average laptop.
If you cannot view the video output file, try opening it with [VLC media player](http://www.videolan.org/vlc/).

## File structure 
| Name                    | Purpose                                                                           |
|-------------------------|-----------------------------------------------------------------------------------|
| filters.py              | Ideal, Buttersworth and author's IIR signal filters                               |
| pyramids.py             | Image dimension agnostic Laplacian and Guassian pyramid building functions        |
| motion_magnify.py       | The main function used to create a motion or color magnified video.               |
| reproduce_paper.py      | Runs experiments for the video files hosted on the paper's website                |

## Results
| Subject | Authors results | This repo results|
| ---------------| --------------- | ---------------- |
| Baby breathing | ![](gifs/output_authors/baby1.gif) | ![](gifs/output/baby1.gif)  |
| Shadow on a house | ![](gifs/output_authors/shadow.gif)  | ![](gifs/output/shadow.gif)  |
| Guitar A string | ![](gifs/output_authors/guitar_a.gif)  | ![](gifs/output/guitar_a.gif)  |
| Human pusle (speed difference due to fps conversion)| ![](gifs/output_authors/face1.gif)  | ![](gifs/output/face1.gif)  |
