import matplotlib.pyplot as plt
import skvideo.io


def plot_slice(vid, output_path):
    """ Save a spatiotemporal slice of a video to disk. """
    frames, height, width, channels = vid.shape
    patch_seq = vid[:, :, width//2, :]
    plt.imshow(patch_seq.swapaxes(0, 1))
    plt.savefig(output_path)


def get_fps(vid_path):
    """ Get the frames per second of a video. """
    metadata = skvideo.io.ffprobe(vid_path)
    fps = metadata['video']['@r_frame_rate'].split('/')[0]
    fps = float(fps)
    return fps

