# cnprep

## Chinese text preprocess

You can extract numbers, email, website, emoji, tex, and delete spaces, punctuations.

## Install

```
pip install cnprep
```

## Usage

```Python
from cnprep import Extractor
ext = Extractor(delete=True, args=['email', 'number'], blur=True, limit=5)
ext.extract(message)
```

```
delete: delete the found info (except blur)
args: option
    e.g. ['email', 'number'] or 'email, number'
blur: convert Chinese to pinyin and extract useful numbers
limit: parameter for get_number
```

Also, you can use `ext.reset_param()` to reset the parameters.