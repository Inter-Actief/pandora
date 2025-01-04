from django.forms import Form, FileField


class ArchiveUploadForm(Form):
    file = FileField()
