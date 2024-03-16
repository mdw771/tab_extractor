import logging

import tab_extractor


logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Use bounding_box to specify the location of slide-showing scores/tabs in your video.
loader = tab_extractor.loader.VideoLoader('video.mov', bounding_box=None)
loader.load(start_s=4, end_s=None, step_s=1)

processor = tab_extractor.processor.Processor(loader)
processor.run()
processor.save_pages('tab.pdf')
