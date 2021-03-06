# Copyright 2022 Netherlands eScience Center and Vrije Universiteit Amsterdam
# Licensed under the Apache License, version 2.0. See LICENSE for details.

import os
import urllib.request
import pdftotext


def preprocess_pdf(infile, r_blankline=', ', r_eol=' ', r_par=''):
    with open(infile, 'rb') as f:
        pdf = pdftotext.PDF(f)
    text = "\n".join(pdf)
    text = text.replace('\n\n', r_blankline).replace('\r\n\r\n', r_blankline).replace('\n', r_eol)
    text = text.replace('\r', ' ').replace('\t', ' ')
    text = text.replace('(', r_par).replace(')', r_par).replace(';', ',')
    text = text.replace('\x0c', ' ').replace('\x07', ' ').replace('\x08', ' ').replace('\xad', ' ')
    text = text.replace('•', ', ').replace('', ', ').replace('◼', ', ').replace('\uf0b7', ' ')
    text = text.replace('/', ' / ')
    while ':.' in text:
        text = text.replace(':.', ':')
    text = text.replace(':', ', ')
    while '  ' in text:
        text = text.replace('  ', ' ')
    while ', ,' in text:
        text = text.replace(', ,', ',')
    while ',,' in text:
        text = text.replace(',,', ',')
    while(' ,') in text:
        text = text.replace(' ,', ',')
    text = text.replace('.,', '.')
    while '. .' in text:
        text = text.replace('. .', '.')
    while '..' in text:
        text = text.replace('..', '.')
    while(' .') in text:
        text = text.replace(' .', '.')
    return text


def download_pdf(url):
    """ Download a pdf file from a url and safe it in the cwd """
    with urllib.request.urlopen(url) as urlfile:
        filename = os.path.join(os.getcwd(), "downloaded.pdf")
        with open(filename, 'wb') as file:
            file.write(urlfile.read())
    return filename


def delete_downloaded_pdf():
    """ Delete the file that is downloaded with the function download_pdf and saved as
    downloaded.pdf from the cwd."""
    os.remove(os.path.join(os.getcwd(), "downloaded.pdf"))
