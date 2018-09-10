#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Gionata Mettifogo

Grab photos from Flickr for a set of keywords.  Considers only those photos
with a CC non-commercial license, or more relaxed license (license ids 1,2,4,5
at https://www.flickr.com/services/api/flickr.photos.licenses.getInfo.html)

See README.md for details.
"""

import sys
import json
import os
import glob
import random
from pprint import pprint

import times
import requests
import flickr_api

config = json.load(open('./config.json'))

API_KEY = config['flickr_api_key']
API_SECRET = config['flickr_api_secret']
REST_ENDPOINT = 'https://api.flickr.com/services/rest/'
IMAGE_URL = 'http://farm%s.staticflickr.com/%s/%s_%s_z.jpg'
flickr_api.set_keys(api_key=API_KEY, api_secret=API_SECRET)

IMAGE_FILENAME = '%s-%s.jpg'  # keyword-id.jpg'
TRAINING_DIRECTORY = './data/train/%s/'  # keyword
VALIDATION_DIRECTORY = './data/valid/%s/'  # keyword
TEST_DIRECTORY = './data/test/%s/' 

NUMBER_OF_TRAINING_IMAGES = config['number_of_training_images']
NUMBER_OF_VALIDATION_IMAGES = config['number_of_validation_images']
NUMBER_OF_TEST_IMAGES = config['number_of_test_images'] 


def unjsonpify(jsonp):
    return jsonp[14:-1]  # totally hacky strip off jsonp func


def save_image(url, image_filename):
    r = requests.get(url, stream=True)
    with open(image_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            f.write(chunk)
        return True
    return False


def download_image(photo, image_filename):
    image_dir = os.path.dirname(image_filename)
    if not os.path.isdir(image_dir):
        os.makedirs(image_dir)
    image_url = IMAGE_URL % (photo['farm'], photo['server'], photo['id'], photo['secret'])
    return save_image(image_url, image_filename)


def search_images(keyword, page):
    """ Download flickr metadata for photos in the given category (items are paged) """
    params = {'api_key': API_KEY,
              'safe_search': '1',  # safest
              'media': 'photos',  # just photos
              'content_type': '1',  # just photos
              'privacy_filter': '1',  # public photos
              'license': '1,2,4,5',  # see README.md
              'per_page': '100',  # max=500
              'page': page,
              'sort': 'relevance',
              'method': 'flickr.photos.search',
              'format': 'json'}
    query_dict = {'text': keyword}
    response = requests.get(REST_ENDPOINT, params=dict(params, **query_dict))
    return json.loads(unjsonpify(response.text))


def move_images(from_directory, to_directory, number_of_images):
    """ Move a number of randomly choosen files from a directory to another """
    if not os.path.isdir(to_directory):
        os.makedirs(to_directory)
    while number_of_images > 0:
        from_files = os.listdir(from_directory)
        from_filename = from_files[random.randint(0, len(from_files)-1)]
        to_filename = os.path.join(to_directory, from_filename)
        os.rename(os.path.join(from_directory, from_filename), to_filename)
        number_of_images -= 1
        

def search_and_download_images(keyword):
    directory = TRAINING_DIRECTORY % (keyword)
    requested_images = NUMBER_OF_TRAINING_IMAGES + NUMBER_OF_VALIDATION_IMAGES + NUMBER_OF_TEST_IMAGES
    downloaded_images = 0
    current_page = 1

    # download all images in the same directory
    while downloaded_images < requested_images:
        images = search_images(keyword, current_page)
        current_page += 1

        if int(images['photos']['total']) < (requested_images - downloaded_images):
            print('there are not enough photos of \'%s\'' % keyword)
            return False

        for i, photo in enumerate(images['photos']['photo']):
            image_filename = os.path.join(directory, IMAGE_FILENAME % (keyword, photo['id']))
            if download_image(photo, image_filename):
                sys.stdout.write('\rdownloaded photo %d/%d (%s)' % 
                    (downloaded_images + 1, requested_images, keyword))
                sys.stdout.flush()
                downloaded_images += 1
                if downloaded_images >= requested_images:
                    break

    # move random images from the main set to the validation and test sets
    if NUMBER_OF_VALIDATION_IMAGES > 0:
        move_images(directory, VALIDATION_DIRECTORY % keyword, NUMBER_OF_VALIDATION_IMAGES)
    if NUMBER_OF_TEST_IMAGES > 0:
        move_images(directory, TEST_DIRECTORY % keyword, NUMBER_OF_TEST_IMAGES)
    return True



if __name__ == '__main__':
    import argparse

    # populate and parse command line options
    desc = 'Grab photos from Flickr.'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-c', '--create', dest='create', action='store_true')
    args = parser.parse_args()

    if args.create:
        keywords = []
        with open('keywords.txt') as f:
            keywords = [e.strip() for e in f.readlines()]
            for i, keyword in enumerate(keywords):
                search_and_download_images(keyword)
                print('')
        print('done')

    else:
        pprint(config)
        print(parser.print_help())
