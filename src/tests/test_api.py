import os
from .utils import get_token, get, post_files


HOME = os.environ['HOME']
IMG_DIR = '{}/data/l3autoseg/test_files'.format(HOME)


def test_user_can_get_token():
    token = get_token('ralph', 'arturo4ever')
    print(token)


def test_user_can_create_dataset_by_uploading_images():
    token = get_token('ralph', 'arturo4ever')
    files = []
    for f in os.listdir(IMG_DIR):
        f_path = os.path.join(IMG_DIR, f)
        # files.append((f, open(f_path, 'rb')))
        files.append(('files', (f, open(f_path, 'rb'), 'image/png')))
    print(files)
    result, status_code = post_files('api/datasets/', token, files=files, raw_result=False)
    assert status_code == 201
    assert 'dataset_id' in result.keys()
    dataset_id = result['dataset_id']
    # Check that dataset IDs present in list of datasets
    result, status_code = get('api/datasets/', token)
    assert status_code == 200
    assert dataset_id in result['dataset_ids']
