import skvideo.io

from filters import *
from pyramids import *
from utils import *


def motion_magnify(video_path: str,
                   output_path: str,
                   motion: bool,
                   alpha: float,
                   filter_type: str,
                   low: float = None,
                   high: float = None,
                   r_low: float = None,
                   r_high: float = None,
                   lambda_c: float = None,
                   fps: float = None,
                   max_layer: int = 5):
    """ Applies motion or color magnification to a video and writes the output to disk.

        Args:
            video_path: Path to read input video from.
            output_path: Path to write magnified output to.
            motion: Whether to magnify motion. When `False`, color is magnified.
            alpha: The amount of amplification of the filtered signal.
            filter_type: 'butter' or 'ideal'. The type of bandpass filter to apply to a pixel sequences.
            low: The low cutoff point of the bandpass filter.
            high: The high cutoff point of the bandpass filter.
            r_low: The iir filter low. (Note, not an absolute cutoff)
            r_high: The iir filter high. (Note, not an absolute cutoff)
            lambda_c: Increase to increase alpha scaling.
            fps: Frames per second of the video, used only for high speed videos.
            max_layer: The number of layers in Guassian and Laplacian pyramids.
    """

    vid = skvideo.io.vread(video_path)

    if fps is None:
        fps = get_fps(video_path)

    # Create pyramid layer stacks
    if motion:
        pyramid_seq = video_to_laplace_pyramid_seq(vid, max_layer=max_layer)
        stacks = pyramid_seq_to_stacks(pyramid_seq)
    else:
        stacks = [video_to_gauss_stack(vid, pick_layer=max_layer)]

    # Filter stacks
    if filter_type == 'butter':
        stacks_filtered = [butter_filter_stack(stack, lowcut=low, highcut=high, fs=fps) for stack in stacks]
    elif filter_type == 'ideal':
        stacks_filtered = [ideal_filter_stack(stack, lowcut=low, highcut=high, fs=fps) for stack in stacks]
    else:
        stacks_filtered = [iir_filter_stack(stack, r1=r_high, r2=r_low) for stack in stacks]

    # Reconstruct video
    if motion:
        stacks_amplified = variable_amplify_stacks(stacks_filtered, alpha=alpha, lambda_c=lambda_c, vid=vid)
        pyramid_seq_filtered = stacks_to_pyramid_seq(stacks_amplified)
        vid_filtered = pyramid_seq_to_vid(pyramid_seq_filtered)
    else:
        vid_filtered = gauss_stack_to_vid(stacks_filtered[0], pick_layer=max_layer, ref=vid)
        vid_filtered = vid_filtered * alpha

    vid_result = vid + vid_filtered
    skvideo.io.vwrite(output_path, vid_result)