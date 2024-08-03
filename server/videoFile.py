import queryImages


def getVideoFile(jsonData):
    imageUrls = []
    for item in jsonData:
        print(item)
        imageUrls.append(queryImages.FindImages(item["QueryImage"]))

    return ""

    # temporary_file_name = f"temp_file_{uuid.uuid4().hex}.tmp"

    # create_video(jsonData, imageUrls, temporary_file_name)
    # return temporary_file_name
