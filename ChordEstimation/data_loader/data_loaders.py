import numpy as np
from data_loader.dataset import MusicXMLDataset  # Import the new dataset class
from torch.utils.data import DataLoader
from torch.utils.data.sampler import SubsetRandomSampler

class MusicXMLDataLoader(DataLoader):
    """
    MusicXML Dataloader class
    """
    def __init__(self, data_path='data/out.pkl', batch_size=64, shuffle=True, validation_split=0.1, num_workers=1, **kwargs):
        self.validation_split = validation_split
        self.shuffle = shuffle

        self.dataset = MusicXMLDataset(data_path)  # Use the new dataset class

        self.batch_idx = 0
        self.n_samples = len(self.dataset)

        self.sampler, self.valid_sampler = self._split_sampler(self.validation_split)

        self.init_kwargs = {
            'dataset': self.dataset,
            'batch_size': batch_size,
            'shuffle': self.shuffle,
            'num_workers': num_workers,
            'collate_fn': midi_collate_fn  # You might need to adjust this function to handle your data format
            }
        super(MusicXMLDataLoader, self).__init__(sampler=self.sampler, **self.init_kwargs)

    def _split_sampler(self, split):
        if split == 0.0:
            return None, None

        idx_full = np.arange(self.n_samples)

        np.random.seed(0)
        np.random.shuffle(idx_full)

        len_valid = int(self.n_samples * split)

        valid_idx = idx_full[0:len_valid]
        train_idx = np.delete(idx_full, np.arange(0, len_valid))

        train_sampler = SubsetRandomSampler(train_idx)
        valid_sampler = SubsetRandomSampler(valid_idx)

        self.shuffle = False
        self.n_samples = len(train_idx)

        return train_sampler, valid_sampler

    def split_validation(self):
        if self.valid_sampler is None:
            return None
        else:
            return DataLoader(sampler=self.valid_sampler, **self.init_kwargs)

class TestMusicXMLDataLoader(MusicXMLDataLoader):
    def __init__(self, data_path='data/out.pkl', shuffle=False, validation_split=0.0):
        init_kwargs = {
            'data_path': data_path,
            'shuffle': shuffle,
            'validation_split': validation_split
            }
        super(TestMusicXMLDataLoader, self).__init__(**init_kwargs)


# class MusicXMLDataset(Dataset):
#     def __init__(self, data_path):
#         self.data = pd.read_pickle(data_path)

#     def __len__(self):
#         return len(self.data)

#     def __getitem__(self, idx):
#         melody_x = torch.tensor(self.data.iloc[idx]['melody_x'])
#         chord_y = torch.tensor(self.data.iloc[idx]['chord_y'])
#         seq_length = torch.tensor(self.data.iloc[idx]['seq_length'])
#         return {'melody_x': melody_x, 'chord_y': chord_y, 'seq_length': seq_length}
