import numpy as np
import scipy.fftpack as fftpack
from scipy.signal import butter, lfilter


def butter_filter_stack(stack, coefs):
    """ Applies a digital filter to stack of pyramid layers. """
    stack = stack.copy()
    for i in range(3):
        stack[:, :, :, i] = np.apply_along_axis(func1d=butter_filter_seq, axis=0, arr=stack[:, :, :, i], coefs=coefs)
    return stack


def butter_lowpass(lowcut, fs, order=5):
    """ Computes the coefficients of a Butterworth bandpass filter. """
    nyq = 0.5 * fs
    low = lowcut / nyq
    b, a = butter(N=order, Wn=low, btype='low')
    return b, a


def butter_filter_seq(seq, coefs):
    """ Apply a butterworth bandpass filter to a sequence. """
    b, a = coefs
    y = lfilter(b, a, seq)
    return y


def butter_filter_stack(stack, lowcut, highcut, fs):
    low_a, low_b = butter_lowpass(lowcut, fs, order=1)
    high_a, high_b = butter_lowpass(highcut, fs, order=1)

    stack_filtered = list()
    lowpass1 = stack[0]
    lowpass2 = stack[0]
    stack_filtered.append(stack[0])
    prev_frame = stack[0]

    for frame in stack[1:]:
        lowpass1 = (-high_b[1] * lowpass1 + high_a[0] * frame + high_a[1] * prev_frame) / high_b[0]
        lowpass2 = (-low_b[1] * lowpass2 + low_a[0] * frame + low_a[1] * prev_frame) / low_b[0]

        frame_filtered = (lowpass1 - lowpass2)
        stack_filtered.append(frame_filtered)
        prev_frame = frame

    stack_filtered = np.array(stack_filtered)

    return stack_filtered


def ideal_filter_stack(stack, lowcut, highcut, fs):
    """ Applies a Fourier transform to a signal and extracts
        frequencies between low and high cutoffs. Taken from
        github user flyingzhao at https://bit.ly/3lArgUp.
    """
    fft = fftpack.fft(stack, axis=0)
    frequencies = fftpack.fftfreq(stack.shape[0], d=1 / fs)
    bound_low = (np.abs(frequencies - lowcut)).argmin()
    bound_high = (np.abs(frequencies - highcut)).argmin()
    fft[:bound_low] = 0
    fft[bound_high:-bound_high] = 0
    fft[-bound_low:] = 0
    iff = fftpack.ifft(fft, axis=0)
    return np.abs(iff)


def iir_filter_stack(stack, r1, r2):
    """ Applies temporal filtering of the form:

        y1[n] = r1*x[n] + (1-r1)*y1[n-1]
        y2[n] = r2*x[n] + (1-r2)*y2[n-1]
        where (r1 > r2) and
        y[n] = y1[n] - y2[n].
    """
    stack_filtered = list()
    lowpass1 = stack[0]
    lowpass2 = stack[0]
    stack_filtered.append(stack[0])

    for frame in stack[1:]:
        lowpass1 = (1 - r1) * lowpass1 + r1 * frame
        lowpass2 = (1 - r2) * lowpass2 + r2 * frame
        frame_filtered = (lowpass1 - lowpass2)
        stack_filtered.append(frame_filtered)

    stack_filtered = np.array(stack_filtered)

    return stack_filtered


def variable_amplify_stacks(stacks, alpha, lambda_c, vid):
    """ Instead of amplifying each pyramid layer by the same amount,
        apply an intelligent weighting scheme that prevents creating
        images with distortion and channel overshooting.
    """
    stacks_amplified = list()
    _, height, width, _ = vid.shape
    delta = lambda_c / 8 / (1 + alpha)
    lambda_amp = (height ** 2 + width ** 2) ** 0.5 / 3
    exaggeration_factor = 2

    for stack_idx in range(len(stacks)):
        stack = stacks[stack_idx]
        alpha_mod = lambda_amp / delta / 8 - 1
        alpha_mod = alpha_mod * exaggeration_factor

        if stack_idx == len(stacks) - 1 or stack_idx == 0:
            stack = np.zeros(stack.shape)

        elif alpha_mod > alpha:
            stack = alpha * stack

        else:
            stack = alpha_mod * stack

        lambda_amp = lambda_amp / 2
        stacks_amplified.append(stack)

    return stacks_amplified
