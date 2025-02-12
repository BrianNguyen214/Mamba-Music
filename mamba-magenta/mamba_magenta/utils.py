import argparse
import magenta.music as mm
from magenta.music.protobuf import music_pb2
import numpy as np
import pretty_midi

from midi2audio import FluidSynth
import os

from upload import upload_blob

# from https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
def print_progress_bar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()

def parse_arguments():
    parser = argparse.ArgumentParser(description='Argument Parse for Mamba Magenta Models.')
    parser.add_argument('-m', '--model', type=str, default='melody-rnn',
                        help='Available networks. Choose from:')
    parser.add_argument('-n', '--notes', type=str, default='60 61 62 63',
                        help='Please provide a list of midi notes.')
    parser.add_argument('-lc', '--load_config', type=bool, default=False,
                        help='Whether the config is desired to be used.')
    parser.add_argument('-cfd', '--config_dir', type=str, default='config',
                        help='Config directory')
    parser.add_argument('-cff', '--config_file', type=str, default='sequence.yaml',
                        help='Config file for a note sequence.')

    return parser.parse_args()


def generated_sequence_2_mp3(seq, filename, request_dict,
                             dirs="songs", use_salamander=False):
    """
    generates note sequence `seq` to an mp3 file, with the name
    `filename` in directory(ies) `dir`.
    """
    os.makedirs('songs/', exist_ok=True)
    song_path = os.path.join(dirs, filename)
    # convert from note sequence to midi file.
    mm.sequence_proto_to_midi_file(seq, f'{song_path}.mid')
    if use_salamander:
        fs = FluidSynth('~/.fluidsynth/salamander.sf2')
    else:
        fs = FluidSynth()

    # we can change instrumentation here.
    # if we want to change anything, we can do it here

    fs.midi_to_audio(f'{song_path}.mid', f'{song_path}.mp3')
    # remove midi file for bookkeeping.
    os.remove(f'{song_path}.mid')

    # upload code to google cloud storage
    upload_blob(f'{filename}.mp3', request_dict)


def create_chords(chord_list):
    nums = []
    all_keys = np.zeros((12, len(chord_list)))
    for i, chord in enumerate(chord_list):
        chord_root = chord.split()[0][0]
        nums.append(chord_root)
        num = pretty_midi.key_name_to_key_number(chord_root)
        all_keys[0, i] = num

        for i in range(1, 12):
            all_keys[i] = (all_keys[i-1] + 1) % 12
    all_transposes = [] 
    for i in range(all_keys.shape[0]):
        progression = []
        for j in range(all_keys.shape[1]):
            root = pretty_midi.key_number_to_key_name(int(all_keys[i, j]))
            if root[1] == 'b':
                take = root[:2]
            else:
                take = root[0]
            chord_type = chord_list[j][1:]
            progression.append(f'{take}{chord_type}')
        all_transposes.append(progression)
    return all_transposes


def construct_all_from_chord_progressions(chord_progressions):
    all_chord_progressions = []
    for chord_progression in chord_progressions:
        all_chord_progressions.extend(create_chords(chord_progression))
    return all_chord_progressions
