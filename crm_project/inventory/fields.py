from django.db.models import FileField
from django.forms import forms
from django.utils.translation import ugettext_lazy as _


class PdfField(FileField):

    def __init__(self, *args, **kwargs):
        self.pdf_type = "application/pdf"
        
        super().__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = super().clean(*args, **kwargs)
        file_data = data.file

        content_type = file_data.content_type

        if content_type != self.pdf_type:
            raise forms.ValidationError(_('فایل توسط این فیلد پشتیبانی نمی شود'))

        return data