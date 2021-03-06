#
# Copyright 2013 - Tom Alessi
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Form and Form Field classes for the Quinico Pagespeed application

   All fields should be defined first, with forms to follow.  Form fields
   have basic validation rules and DJango takes care of escaping anything
   dangerous automatically.

"""


import re
from django import forms


class FormatField(forms.Field):
    """A format field

       Requirements:
          - Not required to be present
          - Only certain values are accepted (csv, db, json)

    """

    def validate(self, value):
        if value and not re.match(r'^(csv|db|db1|db2|json|json1|json2)$', value):
            raise forms.ValidationError('Improperly formatted format:%s' % (value))


class StrategyField(forms.Field):
    """A strategy field

    Requirements:
       - Must not be empty
       - Must only be mobile or desktop

    """

    def validate(self, value):
        if value is None or value == '':
            raise forms.ValidationError('No strategy selected')
        if not re.match(r'^(mobile|desktop)$', value):
            raise forms.ValidationError('Improperly formatted strategy:%s' % (value))


### FORMS ###


class PagespeedTrendForm(forms.Form):
    """Form for querying Pagespeed trends"""

    date_from = forms.DateField(required=False,input_formats=['%Y-%m-%d'])
    date_to = forms.DateField(required=False,input_formats=['%Y-%m-%d'])
    domain = forms.CharField()
    url = forms.CharField()
    metric = forms.CharField()
    strategy = StrategyField()
    format = FormatField()
    width = forms.IntegerField(required=False)
    height = forms.IntegerField(required=False)
    step = forms.IntegerField(required=False)

    # Override the form clean method - there is some special logic to validate 

    def clean(self):
        cleaned_data = super(PagespeedTrendForm, self).clean()
        width = cleaned_data.get('width')
        height = cleaned_data.get('height')

        if width and not height:
            self._errors["height"] = self.error_class(['You must define a width and height'])
        
        if height and not width:
            self._errors["width"] = self.error_class(['You must define a width and height'])
        
        # Return the full collection of cleaned data
        return cleaned_data

class PagespeedBreakdownForm(forms.Form):
    """Form for querying Pagespeed page breakdown"""

    date = forms.DateField(required=False,input_formats=['%Y-%m-%d'])
    domain = forms.CharField()
    url = forms.CharField()
    strategy = StrategyField()
    format = FormatField()
    width = forms.IntegerField(required=False)
    height = forms.IntegerField(required=False)

    # Override the form clean method - there is some special logic to validate 

    def clean(self):
        cleaned_data = super(PagespeedBreakdownForm, self).clean()
        width = cleaned_data.get('width')
        height = cleaned_data.get('height')

        if width and not height:
            self._errors["height"] = self.error_class(['You must define a width and height'])
        
        if height and not width:
            self._errors["width"] = self.error_class(['You must define a width and height'])
        
        # Return the full collection of cleaned data
        return cleaned_data
        

class PagespeedHistoryForm(forms.Form):
    """Form for querying Pagespeed history"""

    date_from = forms.DateField(required=False,input_formats=['%Y-%m-%d'])
    date_to = forms.DateField(required=False,input_formats=['%Y-%m-%d'])
    domain = forms.CharField()
    url = forms.CharField()
    strategy = StrategyField()
    format = FormatField()


class PagespeedReportForm(forms.Form):
    """Form for querying the entire Pagespeed report"""

    id = forms.IntegerField(min_value=1)
