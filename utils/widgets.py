from django import forms
from django.utils.encoding import force_unicode
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from utils.formatters import format_rut


class RutInput(forms.TextInput):
    def _format_value(self, value):
        return format_rut(value)


class BootstrapRadioInput(forms.widgets.RadioInput):
    def __unicode__(self):
        if 'id' in self.attrs:
            label_for = ' for="%s_%s"' % (self.attrs['id'], self.index)
        else:
            label_for = ''
        choice_label = conditional_escape(force_unicode(self.choice_label))
        txtClass = "radio"
        if 'class' in self.attrs:
            txtClass += ' ' + self.attrs['class']
        return mark_safe(u'<label class="%s" %s>%s %s</label>' % (txtClass, label_for, self.tag(), choice_label))


class VerticalRadio(forms.widgets.RadioFieldRenderer):
    def __iter__(self):
        for i, choice in enumerate(self.choices):
            yield BootstrapRadioInput(self.name, self.value, self.attrs.copy(), choice, i)

    def __getitem__(self, idx):
        choice = self.choices[idx]
        return BootstrapRadioInput(self.name, self.value, self.attrs.copy(), choice, idx)

    def render(self):
        return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))


class HorizontalRadio(forms.widgets.RadioFieldRenderer):
    def __iter__(self):
        self.attrs['class'] = 'inline'
        for i, choice in enumerate(self.choices):
            yield BootstrapRadioInput(self.name, self.value, self.attrs.copy(), choice, i)

    def __getitem__(self, idx):
        choice = self.choices[idx]
        return BootstrapRadioInput(self.name, self.value, self.attrs.copy(), choice, idx)

    def render(self):
        return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))
