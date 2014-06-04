from django.forms import ModelForm,Textarea,DateInput
from datetime import datetime 
from leave.models import Application,Employee
from django.forms.extras.widgets import SelectDateWidget


class ApplicationForm(ModelForm):

	
	def __init__(self, dept,*args, **kwargs):
	    super(ApplicationForm, self).__init__(*args, **kwargs)
	    self.fields['attachment1'].label = "Attachment 1"
	    self.fields['attachment2'].label = "Attachment 2"
	    self.fields['attachment3'].label = "Attachment 3"
	    self.fields["employee"].queryset=Employee.objects.filter(dept=dept)

	class Meta:
   		model = Application
   		fields = ['employee', 'leave_type', 'date_from', 'date_to','reason','attachment1','attachment2','attachment3']
   		widgets={'reason': Textarea(attrs={'cols': 10, 'rows': 5})}

	
	def is_valid(self):
		valid=super(ApplicationForm,self).is_valid()
		
		if not valid:
			return valid
		print self.errors
		date_from=self.cleaned_data['date_from']
		date_to=self.cleaned_data['date_to']
		leave_balance=self.cleaned_data['employee'].leave_balance
		

		if date_from<datetime.now().date():
			self.errors['date_from']=['Aha?']
			return False

		if(date_to<date_from):
			self.errors['date_to']=["Seriously? :P"]

			return False

		
		

		if((date_to-date_from).days+1>leave_balance):
			self.errors['date_to']=["Insufficient leave balance"]
			return False


		return True






