import os
from pathlib import Path
from typing import IO, Generator
from django.shortcuts import get_object_or_404

from djangoProject9.settings import VIDEOS_DIR
from video.models import Video


def ranged(
        file: IO[bytes],
        start: int = 0,
        end: int = None,
        block_size: int = 32
) -> Generator[bytes, None, None]:
    consumed = 0

    file.seek(start)
    while True:
        data_length = min(block_size, end - start - consumed) if end else block_size
        if data_length <= 0:
            break
        data = file.read(data_length)
        if not data:
            break
        consumed += data_length
        yield data

    if hasattr(file, 'close'):
        file.close()


def open_file(request, slug: str) -> tuple:
    try :
        path = Path(os.path.join(VIDEOS_DIR, slug))
        filename = ''
        for f in os.listdir(path):
            filename = f

        path = Path(os.path.join(path, filename))
        print(path)
        file = path.open('rb')
        file_size = path.stat().st_size
    except:
        path = Path(os.path.join(VIDEOS_DIR, 'default'))
        filename = ''
        for f in os.listdir(path):
            filename = f

        path = Path(os.path.join(path, filename))
        print(path)
        file = path.open('rb')
        file_size = path.stat().st_size


    content_length = file_size
    status_code = 200
    content_range = request.headers.get('range')

    if content_range is not None:
        content_ranges = content_range.strip().lower().split('=')[-1]
        range_start, range_end, *_ = map(str.strip, (content_ranges + '-').split('-'))
        range_start = max(0, int(range_start)) if range_start else 0
        range_end = min(file_size - 1, int(range_end)) if range_end else file_size - 1
        content_length = (range_end - range_start) + 1
        file = ranged(file, start=range_start, end=range_end + 1)
        status_code = 206
        content_range = f'bytes {range_start}-{range_end}/{file_size}'

    return file, status_code, content_length, content_range