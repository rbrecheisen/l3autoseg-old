import os
from .utils import get_token, post_files


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
        files.append((f, open(f_path, 'rb')))
    result, status_code = post_files('/datasets/', token, files=files, raw_result=True)
    assert status_code == 201
