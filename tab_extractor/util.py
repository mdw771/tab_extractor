def apply_bounding_box(img, bbox):
    img = img[bbox[0]:bbox[2], bbox[1]:bbox[3]]
    return img