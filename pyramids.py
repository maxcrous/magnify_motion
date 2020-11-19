import cv2
import numpy as np


def resize_to_even(im):
    """ Resizes an image to have even spatial dimensions. """
    shape = np.array(im.shape)
    shape[shape % 2 == 1] += 1
    height, width, _ = shape
    im = cv2.resize(im, (width, height))
    return im


def build_gauss_pyramid(im, max_layer=None):
    """ Builds a gaussian pyramid up until a certain depth. """
    gauss_pyramid = [im]

    for i in range(max_layer):
        im = cv2.pyrDown(im)
        im = resize_to_even(im)
        gauss_pyramid.append(im)

    return gauss_pyramid


def build_laplace_pyramid(gauss_pyramid):
    """ Builds a Laplacian pyramid from a gaussian pyramid. """
    gauss_pyramid = list(reversed(gauss_pyramid))  # Put smallest layer first
    laplace_pyramid = [gauss_pyramid[0]]

    for idx, layer in enumerate(gauss_pyramid[:-1]):
        layer = cv2.pyrUp(layer)
        next_layer = gauss_pyramid[idx + 1]
        height, width, _ = next_layer.shape
        layer = cv2.resize(layer, (width, height))
        diff_of_gauss = cv2.subtract(next_layer, layer)
        laplace_pyramid.append(diff_of_gauss)

    return laplace_pyramid


def collapse_laplace_pyramid(laplace_pyramid):
    """ Collapses a Laplacian pyramid into an image resembling the original. """
    im = laplace_pyramid[0]

    for idx, _ in enumerate(laplace_pyramid[:-1]):
        im = cv2.pyrUp(im)
        next_image = laplace_pyramid[idx + 1]
        next_shape = tuple(reversed(next_image.shape[:2]))
        im = cv2.resize(im, next_shape)
        im = im + next_image

    return im


def video_to_laplace_pyramid_seq(vid, max_layer):
    """ Creates a list containing Laplacian pyramids of all video frames. """
    pyramid_seq = list()

    for frame in vid:
        pyramid = build_gauss_pyramid(frame, max_layer=max_layer)
        pyramid = build_laplace_pyramid(pyramid)
        pyramid_seq.append(pyramid)

    return pyramid_seq


def video_to_gauss_stack(vid, pick_layer):
    """ Creates a list containing a specific Gaussian pyramid layer of all video frames. """
    gauss_stack = list()

    for frame in vid:
        pyramid = build_gauss_pyramid(frame, max_layer=pick_layer)
        layer = pyramid[pick_layer]
        gauss_stack.append(layer)

    gauss_stack = np.array(gauss_stack)
    return gauss_stack


def gauss_stack_to_vid(stack, pick_layer, ref):
    """ Creates a video from a Gaussian pyramid layer stack. """
    vid = list()
    ref_frame = ref[0]
    height, width, _ = ref_frame.shape

    for frame in stack:
        for _ in range(pick_layer):
            frame = cv2.pyrUp(frame)
        frame = cv2.resize(frame, (width, height))
        vid.append(frame)

    vid = np.array(vid)
    return vid


def stacks_to_pyramid_seq(stacks):
    """ Converts a list of stacked layers to a list of Laplacina pyramids. """
    pyramid_seq = list()
    nr_frames = len(stacks[0])

    for frame_idx in range(nr_frames):
        pyramid = list()

        for stack in stacks:
            pyramid.append(stack[frame_idx])

        pyramid_seq.append(pyramid)

    return pyramid_seq


def pyramid_seq_to_stacks(pyramid_seq):
    """ Converts a list of Laplacian pyramids to a list of stacked layers.
        I.e., the same pyramid layer of each frame gets stacked.
    """
    stacks = list()
    nr_layers = len(pyramid_seq[0])

    for layer_idx in range(nr_layers):
        layers = list()

        for pyramid in pyramid_seq:
            layers.append(pyramid[layer_idx])

        stack = np.stack(layers)
        stacks.append(stack)

    return stacks


def pyramid_seq_to_vid(pyramid_seq):
    """ Creates a video from a list of Laplacian pyramids. """
    vid = list()

    for pyramid in pyramid_seq:
        img = collapse_laplace_pyramid(pyramid)
        vid.append(img)

    return np.array(vid)


