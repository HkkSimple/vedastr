from vedastr.dataloaders import build_dataloader
from vedastr.dataloaders.samplers import build_sampler
from vedastr.datasets import build_datasets
from vedastr.transforms import build_transform


def main():
    size = (32, 100)
    mean, std = 0.5, 0.5

    train_sensitive = False
    train_character = '0123456789abcdefghijklmnopqrstuvwxyz'
    test_sensitive = False
    test_character = '0123456789abcdefghijklmnopqrstuvwxyz'
    batch_size = 192
    batch_max_length = 25
    data_filter_off = False
    test_dataset_params = dict(
        batch_max_length=batch_max_length,
        data_filter_off=data_filter_off,
        character=test_character,
    )

    trans_cfg = transform = [
        dict(type='Sensitive', sensitive=train_sensitive),
        dict(type='ColorToGray'),
        dict(type='Resize', size=size),
        dict(type='ToTensor'),
        dict(type='Normalize', mean=mean, std=std),
    ]
    base_cfg = dict(type='LmdbDataset', root=r'D:\DATA_ALL\STR\lmdb\CUTE80',
                    **test_dataset_params)
    base_cfg2 = dict(type='LmdbDataset', root=r'D:\DATA_ALL\STR\MJ_test',
                     **test_dataset_params)
    data_cfg = dict(
        type='ConcatDatasets',
        datasets=[
            base_cfg,
            base_cfg2
        ],
        **test_dataset_params,
        batch_ratio=[0.5, 0.5]
    )

    sampler_cfg = dict(
        type='BalanceSampler',
        batch_size=batch_size,
        shuffle=False,
        oversample=True,
        downsample=True,
    )
    loader_cfg = dict(
        type='DataLoader',
        num_workers=0,
        drop_last=True,
        batch_size=batch_size,
    )

    # build trans
    transform = build_transform(trans_cfg)
    datasets = build_datasets(data_cfg, dict(transform=transform))
    sampler = build_sampler(sampler_cfg, dict(dataset=datasets))
    print(len(sampler))
    # dataloader = build_dataloader(loader_cfg, dict(dataset=datasets, sampler=sampler))
    # for img in dataloader:
    #     print('yes')


if __name__ == '__main__':
    main()
