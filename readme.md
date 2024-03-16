# Tab extractor

Ever encountered a video of instrument play with single-line scores/tabs
at the bottom, but can't find the full score anywhere? This simple tool
extract the scores/tabs from videos and stitch them into a multi-page
PDF. 

## Installation

```commandline
git clone https://github.com/mdw771/tab_extractor.git
cd tab_extractor
pip install -e .
```

## How it works

The tool takes frames from a video with the user-specified time range, 
time step, and spatial bounding box. It then finds the frames that
are sufficiently different from the previous one, and add it to the buffer.
Finally, the frames are stitched and paginated into a PDF.  

## How to use

See `demos/extract.py` for an example. 

Currently, it only works with videos where tabs/scores are displayed
in a "slide-show" manner. Constantly rolling ones are not supported yet.
