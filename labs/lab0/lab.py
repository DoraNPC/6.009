# No Imports Allowed!


def backwards(sound):
    result = {}
    result['rate'] = sound['rate']
    result['left'] = [sample for sample in reversed(sound['left'])]
    result['right'] = [sample for sample in reversed(sound['right'])]

    for key in sound:
        result[key] = (sound[key] if key == 'rate'
            else [sample for sample in reversed(sound[key])])
    return result


def mix(sound1, sound2, p):
    result = {}
    result['right'] = []
    result['left'] = []
    if sound1['rate'] != sound2['rate']:
        return None
    result['rate'] = sound1['rate']
    length = min(len(sound1['right']), len(sound2['right']))
    for i in range(length):
        result['right'].append(sound1['right'][i] * p + sound2['right'][i] * (1-p))
        result['left'].append(sound1['left'][i] * p + sound2['left'][i] * (1-p))
    return result


def echo(sound, num_echos, delay, scale):
    raise NotImplementedError


def pan(sound):
    result = {}
    result['rate'] = sound['rate']
    result['right'] = []
    result['left'] = []
    length = len(sound['right'])
    for i in range(length):
        result['right'].append(i/(length - 1) * sound['right'][i])
        result['left'].append((1 -i/(length - 1)) * sound['left'][i])
    return result


def remove_vocals(sound):
    result = {}
    result['rate'] = sound['rate']
    result['right'] = []
    result['left'] = []
    for i in range(len(sound['right'])):
        result['right'].append(sound['left'][i] - sound['right'][i])
        result['left'].append(sound['left'][i] - sound['right'][i])
    return result


# below are helper functions for converting back-and-forth between WAV files
# and our internal dictionary representation for sounds

import io
import wave
import struct

def load_wav(filename):
    """
    Given the filename of a WAV file, load the data from that file and return a
    Python dictionary representing that sound
    """
    f = wave.open(filename, 'r')
    chan, bd, sr, count, _, _ = f.getparams()

    assert bd == 2, "only 16-bit WAV files are supported"

    left = []
    right = []
    for i in range(count):
        frame = f.readframes(1)
        if chan == 2:
            left.append(struct.unpack('<h', frame[:2])[0])
            right.append(struct.unpack('<h', frame[2:])[0])
        else:
            datum = struct.unpack('<h', frame)[0]
            left.append(datum)
            right.append(datum)

    left = [i/(2**15) for i in left]
    right = [i/(2**15) for i in right]

    return {'rate': sr, 'left': left, 'right': right}


def write_wav(sound, filename):
    """
    Given a dictionary representing a sound, and a filename, convert the given
    sound into WAV format and save it as a file with the given filename (which
    can then be opened by most audio players)
    """
    outfile = wave.open(filename, 'w')
    outfile.setparams((2, 2, sound['rate'], 0, 'NONE', 'not compressed'))

    out = []
    for l, r in zip(sound['left'], sound['right']):
        l = int(max(-1, min(1, l)) * (2**15-1))
        r = int(max(-1, min(1, r)) * (2**15-1))
        out.append(l)
        out.append(r)

    outfile.writeframes(b''.join(struct.pack('<h', frame) for frame in out))
    outfile.close()


if __name__ == '__main__':
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place to put your
    # code for generating and saving sounds, or any other code you write for
    # testing, etc.

    # here is an example of loading a file (note that this is specified as
    # sounds/hello.wav, rather than just as hello.wav, to account for the
    # sound files being in a different directory than this file)
    hello = load_wav('sounds/hello.wav')

    # write_wav(backwards(hello), 'hello_reversed.wav')

    mystery = load_wav("sounds/mystery.wav")
    mystery_rev = backwards(mystery)
    write_wav(mystery_rev, "result_outputs/mystery_rev.wav")
