flickr-to-dataset
==================

Given a set of keywords, search the Flickr API, and download the images. 
Organize them into training, validation and test sets so they can be used 
for machine learning.

1. Edit `config.json.default` to include your [Flickr API](https://www.flickr.com/services/api/) key/secret
2. Edit `keywords.txt` to choose what you want to download (eg: cats, dogs)
3. Run via `python flickr_to_dataset.py --create`

Images will be stored under `/data/`


Thanks Phil Adams for the [original flickr code](https://github.com/philadams/flickr-images-grab)
