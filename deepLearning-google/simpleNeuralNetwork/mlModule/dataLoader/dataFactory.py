from .a1a_dataSet import *
from .a1b_dataPreprocessing import *
from .a1c_divideDatasets import *
from .a2a_dataSet_reformatting import *


def getNotMNIST():
    """Download, extract and reformat the dataset"""
    # Define some globals for the scripts
    url = 'https://commondatastorage.googleapis.com/books1000/'
    prefix = "dataSet"
    num_classes = 10

    imageSize = 28
    pixelDepth = 255.0

    # Download data
    train_filename = downloadDataToFile('notMNIST_large.tar.gz', 247336696, prefix, url)
    test_filename = downloadDataToFile('notMNIST_small.tar.gz', 8458043, prefix, url)

    # Unpack data
    train_folders = maybe_extract(train_filename, prefix, num_classes)
    test_folders = maybe_extract(test_filename, prefix, num_classes)

    # Load and pickle dataSet
    train_datasets = loadAndPickleDataSet(
        "dataSet/notMNIST_large", 45000, imageSize, pixelDepth, force=True)
    test_datasets = loadAndPickleDataSet(
        "dataSet/notMNIST_small", 1700, imageSize, pixelDepth, force=True)

    # Define test sizes
    train_size = 200000
    valid_size = 10000
    test_size = 10000

    # Divide and pickle datasets as tensors
    valid_dataset, valid_labels, train_dataset, train_labels = merge_datasets(
        train_datasets, train_size, valid_size, imageSize)
    _, _, test_dataset, test_labels = merge_datasets(test_datasets, test_size, 0, imageSize)

    print('Training:', train_dataset.shape, train_labels.shape)
    print('Validation:', valid_dataset.shape, valid_labels.shape)
    print('Testing:', test_dataset.shape, test_labels.shape)

    train_dataset, train_labels = randomize(train_dataset, train_labels)
    test_dataset, test_labels = randomize(test_dataset, test_labels)
    valid_dataset, valid_labels = randomize(valid_dataset, valid_labels)

    pickle_file = os.path.join(prefix, 'notMNIST.pickle')
    try:
        f = open(pickle_file, 'wb')
        save = {
            'train_dataset': train_dataset,
            'train_labels': train_labels,
            'valid_dataset': valid_dataset,
            'valid_labels': valid_labels,
            'test_dataset': test_dataset,
            'test_labels': test_labels,
        }
        pickle.dump(save, f, pickle.HIGHEST_PROTOCOL)
        f.close()
    except Exception as e:
        print('Unable to save data to', pickle_file, ':', e)
        raise

    statinfo = os.stat(pickle_file)
    print('Compressed pickle size:', statinfo.st_size)

    # Reformat dataset
    pickleFilename = "dataSet/notMNIST.pickle"
    with open(pickleFilename, "rb") as fp:
        allDatasets = pickle.load(fp)

    testDataset = allDatasets["test_dataset"]
    testLabels = allDatasets["test_labels"]

    reformTestDataset, reformTestLabels = reformatDataSet(testDataset, testLabels)
    validDataset = allDatasets["valid_dataset"]
    validLabels = allDatasets["valid_labels"]

    reformvalidDataset, reformvalidLabels = reformatDataSet(validDataset, validLabels)
    trainDataset = allDatasets["train_dataset"]
    trainLabels = allDatasets["train_labels"]

    reformtrainDataset, reformtrainLabels = reformatDataSet(trainDataset, trainLabels)
    pickleFilenameReformed = "dataSet/notMNISTreformatted.pkl"

    try:
        f = open(pickleFilenameReformed, 'wb')
        save = {
            'trainDataset': reformtrainDataset,
            'trainLabels': reformtrainLabels,
            'validDataset': reformvalidDataset,
            'validLabels': reformvalidLabels,
            'testDataset': reformTestDataset,
            'testLabels': reformTestLabels,
        }
        pickle.dump(save, f, pickle.HIGHEST_PROTOCOL)
        f.close()
    except Exception as e:
        print('Unable to save data to', pickleFilenameReformed, ':', e)
        raise


if __name__ == "__main__":
    getNotMNIST()
