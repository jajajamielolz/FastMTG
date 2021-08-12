class DoublePublishDatasetError(Exception):
    def __init__(self, dataset_version):
        self.message = f"Cannot publish {dataset_version.dataset.name} version {dataset_version.version_id}. This dataset version already exists."
        super(DoublePublishDatasetError, self).__init__()
