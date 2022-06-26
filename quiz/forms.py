from django import forms
from django.core.exceptions import ValidationError

from .models import Choice


class QuestionInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        cnt = 0
        if not (self.instance.QUESTION_MIN_LIMIT <= len(self.forms) <= self.instance.QUESTION_MAX_LIMIT):
            raise ValidationError(
                f'The number of questions must be in the range '
                f'from {self.instance.QUESTION_MIN_LIMIT} '
                f'before {self.instance.QUESTION_MAX_LIMIT}'
            )

        for form in self.forms:
            value = form.cleaned_data['order_num']
            if not (value <= self.instance.QUESTION_MAX_LIMIT):
                raise ValidationError(
                    f'{value} exceeds the maximum number of questions: '
                    f'maximum number of questions =  {self.instance.QUESTION_MAX_LIMIT}'
                )
        for form in self.forms:
            value = form.cleaned_data['order_num']
            cnt += 1
            if cnt != value:
                raise ValidationError(f'Wrong number = {value} !!! next number = {cnt}')


class ChoiceInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        num_correct_answers = sum(form.cleaned_data['is_correct'] for form in self.forms)

        if num_correct_answers == 0:
            raise ValidationError('You must select at least 1 option')

        if num_correct_answers == len(self.forms):
            raise ValidationError('NOT allowed to select all options')


class ChoiceForm(forms.ModelForm):
    is_selected = forms.BooleanField(required=False)

    class Meta:
        model = Choice
        fields = ['text']


ChoicesFormSet = forms.modelformset_factory(
    model=Choice,
    form=ChoiceForm,
    extra=0
)
