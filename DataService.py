import ffmpeg
import youtube_dl
import exifread
import logging
import uuid

from models import Location, Metadata

def getMetadata(url: str):
    fileName = f'vids/{uuid.uuid4()}'
    options = {'outtmpl': fileName}
    youtubeDl = youtube_dl.YoutubeDL(options)

    youtubeDl.extract_info(url)
    ffmpegMetadata = ffmpeg.probe(fileName)

    exifInfoMetadata = _getExif(fileName)
    if exifInfoMetadata is not None:
        return exifInfoMetadata
    
    return Metadata(createDate=ffmpegMetadata['streams'][0]['tags']['creation_time'])

def _getExif(path):
    from pyexiftool.exiftool import ExifTool
    exif_Executable="Image-ExifTool-12.40/exiftool"    

    with ExifTool(executable_=exif_Executable) as et:
        metadata = et.get_metadata_batch([path])
    if metadata is None:
        return None
    metadataObject = metadata[0]
    
    location = None if 'Composite:GPSLatitude' not in metadataObject else Location(
            latitude=metadataObject['Composite:GPSLatitude'],
            longitude=metadataObject['Composite:GPSLongitude']
        )
    return Metadata(
        createDate=_convertToIsoTimeFormat(metadataObject['QuickTime:CreateDate']),
        location=location
    )

def _convertToIsoTimeFormat(unparsed):
    # from 2022:02:13 14:42:28 to 2022-02-26T11:34:30.000000Z
    from dateutil import parser
    time = parser.parse(unparsed)
    return time.strftime("%Y-%m-%dT%H:%M:%SZ") 
