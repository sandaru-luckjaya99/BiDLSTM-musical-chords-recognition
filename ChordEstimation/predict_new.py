import torch
import xml.etree.ElementTree as ET
from utils.util import NOTES_TO_INT


from utils.util import get_instance
import model.model as module_model
from data_loader.dataset import MidiDataset
from utils.util import convert_chord_int_to_str, convert_note_to_int

class Predict:
    def __init__(self, data_path='/content/BiDLSTM-musical-chords-recognition/ChordEstimation/data/out/out.pkl', resume='/content/drive/MyDrive/trined/Chord_Only_BiLSTM_512_2_4/0627_065406/model_best.pth'):
        """
        Initialize the predict class
        """
        self.dataset = MidiDataset(data_path)

        # Load checkpoint
        if torch.cuda.is_available():
            checkpoint = torch.load(resume)
        else:
            checkpoint = torch.load(resume, map_location=lambda storage, loc: storage)
        
        # Load model
        self.model = get_instance(module_model, 'model', checkpoint['config'])
        self.model.load_state_dict(checkpoint['state_dict'])
        self.model.eval()

    def extract_notes_from_musicxml(self, file_path):
            tree = ET.parse(file_path)
            root = tree.getroot()

            notes = []
            for note in root.iter('note'):
                if note.find('rest') is not None:
                    notes.append(('Rest', 0))  # Use a duration of 0 for rests
                    continue
                step = note.find('pitch/step').text
                octave = note.find('pitch/octave').text
                duration = float(note.find('duration').text)  # Extract the duration of the note
                note_name = f'{step}{octave}'
                # Convert the note name to an integer using the NOTES_TO_INT dictionary
                note_int = NOTES_TO_INT.get(step, 1)  # Use 1 (empty note) as the default value
                notes.append((note_int, duration))

            return notes


    def generateOutput(self, input, extra=None):
        """
        Parameters
        ----------
        input: dict
            input into the model
        extra: dict
            extra information for the input

        Returns
        -------
        pred_ouput: list
            list of the chords to return
        """
        pred_output = []
        with torch.no_grad():
            output = self.model(input, extra=extra)

        output_chords = output['chord_out'].squeeze()

        for chord in output_chords:
            c_idx = int(torch.argmax(chord))
            chordstr = convert_chord_int_to_str(c_idx)
            pred_output.append(chordstr)

        return pred_output

    def process(self, melody):
        """ Preprocess the melody for prediction
        Parameters
        ----------
        melody: list
            list of notes

        Returns
        -------
        Input: dict
            dict of inputs to model
        Extra: dict
            dict of extra inputs to model
        """
        x = melody  # The melody already contains integers representing the notes
        durations = [1 for _ in melody]  # Use a default duration of 1 for all notes
        seq_lengths = [len(x)]

        # convert to torch tensor
        x = torch.LongTensor(x).unsqueeze(0)
        durations = torch.FloatTensor(durations).unsqueeze(0)  # Convert durations to a FloatTensor
        seq_lengths = torch.LongTensor(seq_lengths)

        # store in output
        input = {'melody_x':x, 'durations': durations}
        extra = {'seq_lengths': seq_lengths}
        return input, extra


    def get_prediction(self, input_):
        """
        Parameters
        ----------
        input_: list of strings
            List of notes

        Returns
        -------
        list of chords
            list of chords to play
        """
        x, extra = self.process(input_)
        return self.generateOutput(x, extra=extra)

if __name__ == "__main__":
    predict = Predict()
    file_path = "/content/Untitled 56789.musicxml"  # Replace with your actual file path
    input_notes = predict.extract_notes_from_musicxml(file_path)
    input_notes = [note[0] for note in input_notes]  # Extract only the note names, ignore durations
    output = predict.get_prediction(input_notes)
    print(input_notes)
    print(output)

