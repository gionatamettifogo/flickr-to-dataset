flickr-to-dataset
==================

Given a set of keywords, search the Flickr API, and download the images. 
Organize them into training, validation and test sets so they can be used 
for machine learning.

1. Edit `config.json.default` to include your [Flickr API](https://www.flickr.com/services/api/) key/secret
2. Edit `keywords.txt` to choose what you want to download (eg: cats, dogs)
3. Run via `python flickr_to_dataset.py --create`

Images will be stored under `/data/`


Example: `/data/train/dogs/`

<img src="/examples/cats-dogs/train/dogs/dogs-10193910886.jpg" height="100" title="Dog"> <img src="/examples/cats-dogs/train/dogs/dogs-125320524.jpg" height="100" title="Dog"> <img src="/examples/cats-dogs/train/dogs/dogs-20318271389.jpg" height="100" title="Dog"> <img src="/examples/cats-dogs/train/dogs/dogs-15096900534.jpg" height="100" title="Dog">


Example: `/data/train/bees/`

<img src="/examples/bees-wasps/train/bees/bees-10444381654.jpg" height="100" title="Bee"> <img src="/examples/bees-wasps/train/bees/bees-14212550492.jpg" height="100" title="Bee"> <img src="/examples/bees-wasps/train/bees/bees-15179150740.jpg" height="100" title="Bee"> <img src="/examples/bees-wasps/train/bees/bees-205635100.jpg" height="100" title="Bee"> <img src="/examples/bees-wasps/train/bees/bees-3168822965.jpg" height="100" title="Bee">




Thanks Phil Adams for the [original flickr code](https://github.com/philadams/flickr-images-grab)
