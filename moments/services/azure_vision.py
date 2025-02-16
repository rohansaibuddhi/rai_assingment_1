from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.core.credentials import AzureKeyCredential
import os
from dotenv import load_dotenv
load_dotenv()
from flask import current_app

def connect_azure() -> ImageAnalysisClient:
    try:
        endpoint = os.environ["AZURE_ENDPOINT"]
        key = os.environ["AZURE_KEY"]
    except:
        print("Missing environment variable 'VISION_ENDPOINT' or 'VISION_KEY'")
        exit()

    client = ImageAnalysisClient(
        endpoint=endpoint,
        credential = AzureKeyCredential(key)
    )

    return client

def generate_image_description(image_data):

    client = connect_azure()

    try:
        result = client.analyze(
            image_data=image_data,
            visual_features=["CAPTION"],
            language="en"
        )

        if result.caption is not None:
            return result.caption.text
        return None

    except Exception as e:
        current_app.logger.error(f"Azure Vision API error: {str(e)}")
        return None

def generate_tags(image_data):
    client = connect_azure()

    try:
        result = client.analyze(
            image_data=image_data,
            visual_features=["TAGS"],
            language="en"
        )

        tags = []
        if result.tags is not None:
            for tag in result.tags.list:
                tags.append(tag.name)
            return tags

        return None

    except Exception as e:
        current_app.logger.error(f"Azure Vision API error: {str(e)}")
        return None