from django import forms
from cal.models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('title', 'description', 'date_event',)

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)

        self.fields['title'].widget.attrs['placeholder'] = 'Введите название'
        self.fields['description'].widget.attrs['placeholder'] = 'Введите описание'
        self.fields['date_event'].widget = forms.DateInput(attrs={'type': 'date'}, format="%Y-%m-%d")

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'
