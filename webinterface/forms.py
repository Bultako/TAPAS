from django import forms
from archive.webinterface.models import *

from django.utils.encoding import force_unicode
from django.conf import settings
import datetime, time, re

# DATETIMEWIDGET
calbtn = u"""&nbsp;<img src="%scalendar/calbutton.gif" alt="calendar" id="%s_btn" style="cursor: pointer; border: 0px"
title="Select date"/>
<script type="text/javascript">
    Calendar.setup({
        inputField     :    "%s",
        ifFormat       :    "%s",
        button         :    "%s_btn",
        singleClick    :    true
    });
</script>"""

class DateTimeWidget(forms.widgets.TextInput):
    dformat = '%d/%m/%Y'
    def render(self, name, value, attrs=None):
        if value is None: value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '': 
            try:
                final_attrs['value'] = \
                                   force_unicode(value.strftime(self.dformat))
            except:
                final_attrs['value'] = \
                                   force_unicode(value)
        if not final_attrs.has_key('id'):
            final_attrs['id'] = u'%s_id' % (name)
        id = final_attrs['id']
        
        jsdformat = self.dformat #.replace('%', '%%')
        cal = calbtn % (settings.MEDIA_URL, id, id, jsdformat, id)
        a = u'<input%s />%s' % (forms.util.flatatt(final_attrs), cal)
        return a

    def value_from_datadict(self, data, files, name):
            dtf = forms.fields.DEFAULT_DATETIME_INPUT_FORMATS
            empty_values = forms.fields.EMPTY_VALUES

            value = data.get(name, None)
            if value in empty_values:
                return None
            if isinstance(value, datetime.datetime):
                return value
            if isinstance(value, datetime.date):
                return datetime.datetime(value.year, value.month, value.day)
            for format in dtf:
                try:
                    return datetime.date(*time.strptime(value, self.dformat)[:3])
                except ValueError:
                    return value
            return None
# DATETIMEWIDGET


# Get Choices from BDD
choix = []
receivs = SourceSearch_Receivers.objects.all().order_by('id')
for rx in receivs:
    choix.extend([(rx.id, rx.field_label)])

#RECEIVERS_CHOICES = (
#(1, 'Bolometer 1.2mm'),
#(2, 'Rx 1mm'),
#(3, 'Rx 2mm'),
#(4, 'Rx 3mm'),
#(5, 'HERA'),
#) 
RECEIVERS_CHOICES = choix

class SourceSearchForm(forms.ModelForm):

    receivers = forms.MultipleChoiceField(required=False, choices=RECEIVERS_CHOICES, widget=forms.CheckboxSelectMultiple())
    date_from = forms.DateField(required=False, widget=DateTimeWidget)
    date_to = forms.DateField(required=False, widget=DateTimeWidget)
    exact_line = forms.ChoiceField(choices=[(0,'Including '),(1,'Exact')])
    resolver = forms.ChoiceField(choices=[(1,'IRAM Name'), (2,'SIMBAD/NED Name')])

    # validation: text/plain file
    def clean_batchfile(self):
        
        cleaned_data = self.cleaned_data
        batchfile = cleaned_data.get('batchfile')
 
        if batchfile:
          if not self.files['batchfile'].content_type == 'text/plain':
             raise forms.ValidationError('Please, only text/plain files allowed. ')
          else:
             return self.cleaned_data['batchfile']

    # form validation
    def clean(self):

        # flags
        errormsg = ''
        conesearch = 0
        frequency = 0
        velocity = 0
        block = 0
        
        # conesearch empty
        if 'ra' in self.cleaned_data:
            if self.cleaned_data['ra']!='':
                conesearch = conesearch+1
        if 'dec' in self.cleaned_data:
            if self.cleaned_data['dec']!='':
                conesearch = conesearch+1
        if 'size' in self.cleaned_data:
            if self.cleaned_data['size']!=None:
                conesearch = conesearch+1
        if conesearch>0 and conesearch<3:
            errormsg += 'Please, enter all coordinates. '

        # RA format
        if 'ra' in self.cleaned_data:
            if self.cleaned_data['ra']!='':
                mRA = re.match("^([0-9]{2}):([0-9]{2}):([0-9]{2})\.?([0-9]+)?$", self.cleaned_data['ra'])
                try:
                    HA = int(mRA.group(1))<24
                    HA = int(mRA.group(2))<59
                    HA = int(mRA.group(3))<59
                except:
                    HA = 0
                if not mRA:
                    errormsg += 'Please, enter a valid format for RA value. '
                if not HA:
                    errormsg += 'RA coordinates must be given in hourly degrees. '
        		
        # DEC format
        if 'dec' in self.cleaned_data:
            if self.cleaned_data['dec']!='':
                mDEC = re.match("^\-?([0-9]{2}):([0-9]{2}):([0-9]{2})\.?([0-9]+)?$", self.cleaned_data['dec'])
                try:
                    DEC = int(mDEC.group(1))<90
                except:
                    DEC = 0
                if not DEC or not mDEC:
                    errormsg += 'Please, enter a valid format for DEC value. '

    	# size > 30 
        if 'size' in self.cleaned_data:
            if self.cleaned_data['size']>30:
                errormsg += 'Please, enter a size value lower than 30. '
        
        # source name / position
        if ('source_name' in self.cleaned_data and conesearch>0):
            if self.cleaned_data['source_name']!='':
                errormsg += 'Please, only one field in Source Name / Position block. '

        # frequency empty 
        if 'frequency_from' in self.cleaned_data:
            if self.cleaned_data['frequency_from']!=None:
                frequency = frequency+1
                block = block + 1
        if 'frequency_to' in self.cleaned_data:
            if self.cleaned_data['frequency_to']!=None:
                frequency = frequency+1
                block = block + 1
        if frequency>0 and frequency<2:
            errormsg += 'Please, enter frequency range. '
        if frequency==2:
            if (self.cleaned_data['frequency_from']>self.cleaned_data['frequency_to']):
                errormsg += 'Frequencies do not follow. '
		
        # velocity empty
        if 'velocity_from' in self.cleaned_data:
            if self.cleaned_data['velocity_from']!=None:
                velocity = velocity+1
                block = block + 1
        if 'velocity_to' in self.cleaned_data:
            if self.cleaned_data['velocity_to']!=None:
                velocity = velocity+1
                block = block + 1
        if velocity>0 and velocity<2:
            errormsg += 'Please, enter velocity range. '
        if velocity==2:
            if (self.cleaned_data['velocity_from']>self.cleaned_data['velocity_to']):
                errormsg += 'Velocities do not follow. '

        # frequency / velocity / Line Name
        if (block>0 and 'line_name' in self.cleaned_data):
            if self.cleaned_data['line_name']!='':
                errormsg += 'Please, only one field in Frequency/Velocity/Line Name block. '

        # dates empty
        if ('date_from' in self.cleaned_data and 'date_to' in self.cleaned_data):
            if (self.cleaned_data['date_from']!=None and self.cleaned_data['date_to']==None):
                errormsg += 'Please enter Observation Date To. '
            if (self.cleaned_data['date_to']!=None and self.cleaned_data['date_from']==None):
                errormsg += 'Please enter Observation Date From. '
            if (self.cleaned_data['date_to']!=None and self.cleaned_data['date_from']!=None):
                gap = self.cleaned_data['date_to']-self.cleaned_data['date_from']
                if (gap.days<0):
                    errormsg += 'Dates do not follow. '
        # errors found
        if errormsg:
            raise forms.ValidationError(errormsg)
        # ok
        return self.cleaned_data

    class Meta:
        model = SourceSearch 
