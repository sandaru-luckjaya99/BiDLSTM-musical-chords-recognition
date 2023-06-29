from utils.util import convert_chord_to_onehot, convert_note_to_int, \
                        NOTES_TO_INT, INT_TO_NOTES, CHORD_TO_INT, INT_TO_CHORD, CHORD_TO_NOTES, NOTES_TO_CHORD
import os
import pandas as pd
import pickle
from torch.utils.data import Dataset
import xml.etree.ElementTree as ET

class MidiDataset(Dataset):
    """MIDI Music Dataset"""

    NUM_NOTES = max(NOTES_TO_INT.values()) + 1
    NOTES_TO_INT = NOTES_TO_INT
    INT_TO_NOTES = INT_TO_NOTES
    CHORD_TO_INT = CHORD_TO_INT
    INT_TO_CHORD = INT_TO_CHORD
    CHORD_TO_NOTES = CHORD_TO_NOTES
    NOTES_TO_CHORD = NOTES_TO_CHORD

    NUM_CHORDS = max(CHORD_TO_INT.values()) + 1

    def __init__(self, data_path):
        """
        Args:
            data_path (string): Path to MusicXML files
        """

        assert os.path.exists(data_path), "{} does not exist".format(data_path)

        self.data_path = data_path
        self.files = os.listdir(data_path)

    def __len__(self):
        return len(self.files)

    def __getitem__(self, idx):
        """
        Args:
            idx (int): idx of data entry to get
        Returns:
            sample : melody_x, melody_y, chord_y
        """
        filepath = os.path.join(self.data_path, self.files[idx])
        tree = ET.parse(filepath)
        root = tree.getroot()

        melody_x = []
        melody_y = []
        chord_y = []

        for part in root.findall('.//part'):
            for measure in part.findall('.//measure'):
                for note in measure.findall('.//note'):
                    if note.find('.//rest') is None:
                        step = note.find('.//step').text
                        alter = note.find('.//alter')
                        alter = alter.text if alter is not None else ''
                        octave = note.find('.//octave').text
                        note_text = f'{step}{alter}{octave}'
                        melody_x.append(convert_note_to_int(note_text))
                        melody_y.append(convert_note_to_int(note_text))

                harmony = measure.find('.//harmony')
                if harmony is not None:
                    root_step = harmony.find('.//root-step').text
                    root_alter = harmony.find('.//root-alter')
                    root_alter = root_alter.text if root_alter is not None else ''
                    kind = harmony.find('.//kind').text
                    chord_text = f'{root_step}{root_alter} {kind}'
                    chord_y.append(convert_chord_to_onehot(chord_text))

        return melody_x, melody_y, chord_y


if __name__ == '__main__':
    data_path = 'data/out.pkl'
    dataset = MidiDataset(data_path)
