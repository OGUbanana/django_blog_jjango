from django.conf import settings
from datetime import datetime
import os
import warnings

def get_upload_filename(upload_name, request):


    # Complete upload path (upload_path + date_path).
    upload_path = os.path.join(settings.CKEDITOR_UPLOAD_PATH, date_path)

    if getattr(settings, "CKEDITOR_UPLOAD_SLUGIFY_FILENAME", True) and not hasattr(
        settings, "CKEDITOR_FILENAME_GENERATOR"
    ):
        upload_name = utils.slugify_filename(upload_name)

    if hasattr(settings, "CKEDITOR_FILENAME_GENERATOR"):
        generator = import_string(settings.CKEDITOR_FILENAME_GENERATOR)
        # Does the generator accept a request argument?
        try:
            inspect.signature(generator).bind(upload_name, request)
        except TypeError:
            # Does the generator accept only an upload_name argument?
            try:
                inspect.signature(generator).bind(upload_name)
            except TypeError:
                warnings.warn(
                    "Update %s() to accept the arguments `filename, request`."
                    % settings.CKEDITOR_FILENAME_GENERATOR
                )
            else:
                warnings.warn(
                    "Update %s() to accept a second `request` argument."
                    % settings.CKEDITOR_FILENAME_GENERATOR,
                    PendingDeprecationWarning,
                )
                upload_name = generator(upload_name)
        else:
            upload_name = generator(upload_name, request)

    return storage.get_available_name(os.path.join(upload_path, upload_name))