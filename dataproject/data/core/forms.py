import json
import re
import csv
from django import forms


class DataForm(forms.Form):
    days = forms.IntegerField(min_value=0)
