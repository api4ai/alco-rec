#!/usr/bin/env python3

"""Example of using API4AI Alcohol Label Recognition."""

import os
import sys

import requests


# Use 'demo' mode just to try api4ai for free. Free demo is rate limited.
# For more details visit:
#   https://api4.ai
#
# Use 'rapidapi' if you want to try api4ai via RapidAPI marketplace.
# For more details visit:
#   https://rapidapi.com/api4ai-api4ai-default/api/alcohol-label-recognition/details
MODE = 'demo'


# Your RapidAPI key. Fill this variable with the proper value if you want
# to try api4ai via RapidAPI marketplace.
RAPIDAPI_KEY = ''


OPTIONS = {
    'demo': {
        'url': 'https://demo.api4ai.cloud/alco-rec/v1/results',
        'headers': {'A4A-CLIENT-APP-ID': 'sample'}
    },
    'rapidapi': {
        'url': 'https://alcohol-label-recognition.p.rapidapi.com/v1/results',
        'headers': {'X-RapidAPI-Key': RAPIDAPI_KEY}
    }
}


if __name__ == '__main__':
    # Parse args.
    if len(sys.argv) > 1:
        image = sys.argv[1]
    else:
        image = 'https://storage.googleapis.com/api4ai-static/samples/alco-rec-1.jpg'

    if '://' in image:
        # POST image via URL.
        response = requests.post(
            OPTIONS[MODE]['url'],
            headers=OPTIONS[MODE]['headers'],
            data={'url': image})
    else:
        # POST image as file.
        with open(image, 'rb') as image_file:
            response = requests.post(
                OPTIONS[MODE]['url'],
                headers=OPTIONS[MODE]['headers'],
                files={'image': (os.path.basename(image), image_file)}
            )

    # Print raw response.
    print(f'💬 Raw response:\n{response.text}\n')

    # Parse response and print labels.
    text = ''
    labels = response.json()['results'][0]['entities'][0]['array']
    for i, label in enumerate(labels):
        if i > 0:
            text += '\n\n'
        text += f'{label["drink"]}:'
        for prop in label:
            if prop != 'drink':
                text += f'\n  👉 {prop}: {label[prop]}'
    print(f'💬 Labels:\n{text}')
