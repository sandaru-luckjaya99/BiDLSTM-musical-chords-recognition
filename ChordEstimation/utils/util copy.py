import os

'''
Constants for the dataset
'''

# NOTES = ['C', 'C#', 'D-', 'D', 'D#', 'E-', 'E', 'E#', 'F-', 'F', 'F#',
#             'G-', 'G', 'G#', 'A-', 'A', 'A#', 'B-', 'B', 'B#', 'C-']
# NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
# NOTE_TO_INT = {k:v for v, k in enumerate(NOTES)}
NOTES_TO_INT = {
    'PAD': 0, # padding
    '': 1, # empty note
    'Rest': 2, # rest
    'C0': 3, 'C#0': 4, 'D0': 5, 'D#0': 6, 'E0': 7, 'F0': 8, 'F#0': 9, 'G0': 10, 'G#0': 11, 'A0': 12, 'A#0': 13, 'B0': 14,
    'C1': 15, 'C#1': 16, 'D1': 17, 'D#1': 18, 'E1': 19, 'F1': 20, 'F#1': 21, 'G1': 22, 'G#1': 23, 'A1': 24, 'A#1': 25, 'B1': 26,
    'C2': 27, 'C#2': 28, 'D2': 29, 'D#2': 30, 'E2': 31, 'F2': 32, 'F#2': 33, 'G2': 34, 'G#2': 35, 'A2': 36, 'A#2': 37, 'B2': 38,
    'C3': 39, 'C#3': 40, 'D3': 41, 'D#3': 42, 'E3': 43, 'F3': 44, 'F#3': 45, 'G3': 46, 'G#3': 47, 'A3': 48, 'A#3': 49, 'B3': 50,
    'C4': 51, 'C#4': 52, 'D4': 53, 'D#4': 54, 'E4': 55, 'F4': 56, 'F#4': 57, 'G4': 58, 'G#4': 59, 'A4': 60, 'A#4': 61, 'B4': 62,
    'C5': 63, 'C#5': 64, 'D5': 65, 'D#5': 66, 'E5': 67, 'F5': 68, 'F#5': 69, 'G5': 70, 'G#5': 71, 'A5': 72, 'A#5': 73, 'B5': 74,
    'C6': 75, 'C#6': 76, 'D6': 77, 'D#6': 78, 'E6': 79, 'F6': 80, 'F#6': 81, 'G6': 82, 'G#6': 83, 'A6': 84, 'A#6': 85, 'B6': 86,
    'C7': 87, 'C#7': 88, 'D7': 89, 'D#7': 90, 'E7': 91, 'F7': 92, 'F#7': 93, 'G7': 94, 'G#7': 95, 'A7': 96, 'A#7': 97, 'B7': 98,
    'C8': 99
}

INT_TO_NOTES = {v:k for k,v in NOTES_TO_INT.items()}

CHORD_TO_INT = {
    'PAD':0,
    'EMPTY':1,
    'A':2,
    'Am':3,
    'A#':4,     'B-':4,
    'A#m':5,    'B-m':5,
    'B':6,      'C-':6,
    'Bm':7,     'C-m':7,
    'B#':8,     'C':8,
    'B#m':9,    'Cm':9,
    'C#':10,    'D-':10,
    'C#m':11,   'D-m':11,
    'D':12,
    'Dm':13,
    'D#':14,    'E-':14,
    'D#m':15,   'E-m':15,
    'E':16,     'F-':16,
    'Em':17,    'F-m':17,
    'E#':18,    'F':18,
    'E#m':19,   'Fm':19,
    'F#':20,    'G-':20,
    'F#m':21,   'G-m':21,
    'G':22,
    'Gm':23,
    'G#':24,    'A-':24,
    'G#m':25,   'A-m':25,
}

INT_TO_CHORD = {v:k for k,v in CHORD_TO_INT.items()}


CHORD_TO_NOTES = {
    'PAD':'',
    'EMPTY':'',
    'A':'A.C#.E',
    'Am':'A.C.E',
    'A#':'A#.C#.E#',    'B-':'B-.D-.F',
    'A#m':'A#.C.E#',    'B-m':'B-.C.F',
    'B':'B.D#.F#',      'C-':'C-.E-.G-',
    'Bm':'B.D.F#',      'C-m':'C-.D.G-',
    'B#':'B#.E.G',      'C':'C.E.G',
    'B#m':'B#.E-.G',    'Cm':'C.E-.G',
    'C#':'C#.E#.G#',    'D-':'D-.F.A-',
    'C#m':'C#.E.G#',    'D-m':'D-.F-.A-',
    'D':'D.F#.A',
    'Dm':'D.F.A',
    'D#':'D#.G.A#',     'E-':'E-.G.B-',
    'D#m':'D#.G-.A#',   'E-m':'E-.G-.B-',
    'E':'E.G#.B',       'F-':'F-.A-.B',
    'Em':'E.G.B',       'F-m':'F-.G.B',
    'E#':'E#.A.B#',     'F':'F.A.C',
    'E#m':'E#.G#.B#',   'Fm':'F.A-.C',
    'F#':'F#.A#.C#',    'G-':'G-.B-.D-',
    'F#m':'F#.A.C#',    'G-m':'G-.A.D-',
    'G':'G.B.D',
    'Gm':'G.B-.D',
    'G#':'G#.B#.D#',    'A-':'A-.C-.E-',
    'G#m':'G#.B.D#',    'A-m':'A-.B.E-',
}

INTERSECT_THRESH = 2 # Number of notes to intersect to count as a chord


# SORT NOTES IN CHORDS ALPHABETICALLY
for k, v in CHORD_TO_NOTES.items():
    CHORD_TO_NOTES[k] = '.'.join(sorted(v.split('.')))

NOTES_TO_CHORD = {v:k for k,v in CHORD_TO_NOTES.items()}


def get_instance(module, name, config, *args, **kwargs):
    """Get instance from a certain module using the args and kwargs
    """
    print(name)
    return getattr(module, config[name]['name'])(*args, **kwargs, **config[name]['args'])

def convert_chord_int_to_str(chord_int):
    """"Convert chord to string"""
    return CHORD_TO_NOTES[INT_TO_CHORD[chord_int]]

def convert_chord_to_onehot(chord):
    """"Convert chord to onehot list"""
    chord_name = 'EMPTY'
    for k,v in NOTES_TO_CHORD.items():
        if len(set(chord.split('.')).intersection(set(k.split('.')))) >= INTERSECT_THRESH:
            chord_name = v
            break

    # offset by 1 to remove pad
    return CHORD_TO_INT[chord_name]

def convert_note_to_int(note):
    return NOTES_TO_INT[note]

def convert_chord_to_int(chord):
    """
    converts chord into list of ints
    Parameters
    ----------
    chord : str
        notes in chord
    Returns
    -------
    note_list : list
        list of ints for each note in chord
    """
    note_list = []
    notes = chord.split('.')

    for n in notes:
        note_list.append(convert_note_to_int(n))

    return note_list