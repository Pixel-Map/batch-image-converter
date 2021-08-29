"""

Python3 recommended.

"""

import os
import fnmatch
import warnings

from PIL import Image

import imageDataTools
from imageDataTools import assert_equals


def get_image_int8rgb_pixels(filename):
    try:
        image = Image.open(filename) #image is now of type PngImageFile, not Image.
        imageData = image.getdata() #imageData is now of type ImagingCore, not list.
        ARGBPixels = [item for item in imageData] #these may be rgb already, depending on the input image.
        try:
            RGBPixels = [item[:3] for item in ARGBPixels]
        except TypeError:
            #this is because Pillow returns data in different formats depending on which file it is reading.
            raise IOError("File could not be properly read by Pillow.")
    finally:
        image.close()
    return RGBPixels


def save_int8rgb_tuples_as_half_hex(data, output_filename=None, mode=None, decoration="{output_filename} = \"{result}\"", **other_kwargs):
    #does not save when output_filename is None.
    warnings.warn("save_int8rgb_tuples_as_half_hex is deprecated. Use imageDataTools.int8rgb_pixels_to_hex and/or save_text_to_file instead.")
    if decoration is None:
        decoration = "{result}"
    if output_filename is not None:
        if mode is None:
            raise ValueError("mode not specified")
    result = imageDataTools.int8rgb_pixels_to_hex(data, chars_per_channel=1, **other_kwargs)
    if output_filename is None:
        return result
    else:
        with open(output_filename, mode) as output_file:
            #assert "{output_filename}" in decoration
            assert "{result}" in decoration
            decorated_result = decoration.replace("{output_filename}", output_filename).replace("{result}", result)
            output_file.write(decorated_result)
        return result

    
def save_text_to_file(text, output_filename, mode):
    
    with open(output_filename, mode) as output_file:
        output_file.write(text)
        

def gen_matching_file_names(folder_name, file_name_pattern):

    for testFileName in os.listdir(folder_name):
        if fnmatch.fnmatch(testFileName, file_name_pattern):
            yield testFileName
    

def gen_matching_png_file_names_and_pixels(
        folder_name, file_name_pattern,
        skip_errors=True, supress_warnings=False,
    ):
    
    for scanFileName in gen_matching_file_names(folder_name, file_name_pattern):
        scanFullFileName = folder_name + "/" + scanFileName
        try:
            scanFilePixels = get_image_int8rgb_pixels(scanFullFileName)
        except IOError as ioe:
            if skip_errors:
                if not supress_warnings:
                    print("Skipping file {} because it couldn't be read using the current Pillow settings.".format(scanFullFileName))
            else:
                raise ioe
            continue
        yield scanFileName, scanFilePixels
    

def process_png_files(
        folder_name,
        file_name_pattern="*.png",
        do_console_output=True, do_file_output=False,
        common_output_filename=None, mode="w",
        output_filename_prefix="outputs/", output_filename_suffix=".txt",
        console_line_length=48, file_line_length=None,
        console_output_delimiter="\n---\n", console_output_decoration="{name}:\n{content}",
        file_output_delimiter="", file_output_decoration="\n{name} = \"{content}\"\n",
        skip_errors=True, supress_warnings=False,
    ):
    """
    folder_name - folder to search for input files, without trailing slash.
    file_name_pattern - bash-like, e.g. "*.png" or "*x*.png".
    do_console_output - controls whether all processed files will be printed.
    do_file_output - controls whether any files will be created or modified.
    common_output_filename - when not None, this option forces all file\
        outputs to be added to the same output file in append mode.
    output_filename_prefix, output_filename_suffix - prefix and suffix to be\
        added to the base name, which is either the name of the input image\
        file or the provided common output filename.
    console_line_length - custom line wrapping length for console output, or\
        None for unmodified output.
    file_line_length - custom line wrapping length for writing to files, or\
        None for unmodified output.
    """
        
    useSingleOutputFile = (common_output_filename is not None)
    
    fileNamesAndPixelsGen = gen_matching_png_file_names_and_pixels(
        folder_name, file_name_pattern,
        skip_errors=skip_errors, supress_warnings=supress_warnings
    )
    
    for scanFileIndex, scanFileNameAndPixels in enumerate(fileNamesAndPixelsGen):
        scanFileName, scanFilePixels = scanFileNameAndPixels
        scanFilePixelsAsHalfHex = imageDataTools.int8rgb_pixels_to_hex(scanFilePixels, chars_per_channel=1)
        
        if do_file_output:
            outputFileNameBase = common_output_filename if useSingleOutputFile else scanFileName
            outputFileName = output_filename_prefix + outputFileNameBase + output_filename_suffix
            
            stringToSave = file_output_decoration.replace("{name}", scanFileName).replace("{content}", scanFilePixelsAsHalfHex)
            
            if scanFileIndex != 0 and useSingleOutputFile:
                stringToSave = file_output_delimiter + stringToSave
            if file_line_length is not None:
                stringToSave = wrap_text(stringToSave, line_length=file_line_length)
                
            modeForCurrentWrite = ("a" if (useSingleOutputFile and scanFileIndex > 0) else mode)
            save_text_to_file(stringToSave, output_filename=outputFileName, mode=modeForCurrentWrite)
        
        if do_console_output:
            stringToPrint = console_output_decoration.replace("{name}", scanFileName).replace("{content}", scanFilePixelsAsHalfHex)
            
            if scanFileIndex != 0:
                stringToPrint = console_output_delimiter + stringToPrint
            if console_line_length is not None:
                stringToPrint = wrap_text(stringToPrint, line_length=console_line_length)
                
            print(stringToPrint)


def gen_short_lines(text, line_length):
    if line_length < 1:
        raise ValueError("line length must be at least 1.")
    for line in text.split("\n"):
        i = 0
        while i < len(line):
            yield line[i:i+line_length]
            i += line_length


def wrap_text(text, line_length=80):
    return "\n".join(gen_short_lines(text, line_length))
    
    
def print_wrapped(text, line_length=80):
    for line in gen_short_lines(text, line_length):
        print(line)



SAMPLE_IMAGE_HALF_HEX="\
390390390390390390390000000390390390390390390390\
390390390390390390000ff0ff0000390390390390390390\
390390390390390390000ff0ff0000390390390390390390\
390390390390390000ff0ff0ff0ff0000390390390390390\
000000000000000000ff0ff0ff0ff0000000000000000000\
000ff0ff0ff0ff0ff0ff0ff0ff0ff0ff0ff0ff0ff0ff0000\
390000ff0ff0ff0ff0000ff0ff0000ff0ff0ff0ff0000390\
390390000ff0ff0ff0000ff0ff0000ff0ff0ff0000390390\
390390390000ff0ff0000ff0ff0000ff0ff0000390390390\
390390390000ff0ff0ff0ff0ff0ff0ff0ff0000390390390\
390390000ff0ff0ff0ff0ff0ff0ff0ff0ff0ff0000390390\
390390000ff0ff0ff0ff0ff0ff0ff0ff0ff0ff0000390390\
390000ff0ff0ff0ff0ff0000000ff0ff0ff0ff0ff0000390\
390000ff0ff0ff0000000390390000000ff0ff0ff0000390\
000ff0ff0000000390390390390390390000000ff0ff0000\
000000000390390390390390390390390390390000000000"

def test():
    assert_equals(save_int8rgb_tuples_as_half_hex(get_image_int8rgb_pixels("images/SAMPLE.png"), pixel_header=""), SAMPLE_IMAGE_HALF_HEX)
    assert_equals(wrap_text("abcdefg\n1234567", line_length=3), "abc\ndef\ng\n123\n456\n7")
    
    
test()





