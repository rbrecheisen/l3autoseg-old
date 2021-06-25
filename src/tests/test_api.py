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
        f = os.path.join(IMG_DIR, f)
        files.append(open(f, 'rb'))
    dataset_id = post_files('/datasets/', token, files={'files': files})
    assert dataset_id is not None
    for f in files:
        f.close()
