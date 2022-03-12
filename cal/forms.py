from django import forms
from django.forms import DateInput

from cal.models import Event


class DateInput(DateInput):
    input_type = 'date'


class NewEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('title', 'description', 'date_event',)
        widgets = {
            'date_event': DateInput()
        }

    def __init__(self, *args, **kwargs):
        super(NewEventForm, self).__init__(*args, **kwargs)

        self.fields['title'].widget.attrs['placeholder'] = 'Введите название'
        self.fields['description'].widget.attrs['placeholder'] = 'Введите описание'
        self.fields['date_event'].widget.attrs['placeholder'] = 'Введите дату события'

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'
