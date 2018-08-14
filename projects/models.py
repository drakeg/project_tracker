from django.db import models

class Status(models.Model):
	status_text = models.CharField(max_length=50)
	def __str__(self):
		return self.status_text

class Task(models.Model):
	task_text = models.CharField(max_length=25)
	def __str__(self):
		return self.task_text

class DTContact(models.Model):
        dtcontact_fname = models.CharField(max_length=50)
        dtcontact_lname = models.CharField(max_length=50)
        dtcontact_phone = models.CharField(max_length=50)
        def __str__(self):
                return self.dtcontact_lname

class Contact(models.Model):
	contact_fname = models.CharField(max_length=50)
	contact_lname = models.CharField(max_length=50)
	contact_email = models.EmailField(null=True)
	contact_username = models.CharField(max_length=50, null=True)
	contact_phone = models.CharField(max_length=50)
	def __str__(self):
		# This instead returns lastname (first {}), firstname (second {}).
		#     * The '{}, {}' creates 2 placeholders to be populated by .format()
		# return '{}, {}'.format(self.contact_lname, self.contact_fname)
		# TODO: This may show as a bunch of nulls (because username is not required)
		return self.contact_username


class Alignment(models.Model):
	alignment_text = models.CharField(max_length=50)
	def __str__(self):
		return self.alignment_text

class Keyword(models.Model):
        keyword_text = models.CharField(max_length=50)
        def __str__(self):
                return self.keyword_text

class MaturityModel(models.Model):
	maturitymodel_text = models.CharField(max_length=100)
	def __str__(self):
		return self.maturitymodel_text

class Tracker(models.Model):
	task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True)
	title = models.CharField(max_length=100)
	contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True)
	dtcontact = models.ForeignKey(DTContact, on_delete=models.SET_NULL, null=True, blank=True)
	status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)
	alignment = models.ForeignKey(Alignment, on_delete=models.SET_NULL, null=True)
	keywords = models.ManyToManyField(Keyword, blank=True)
	maturitymodel = models.ForeignKey(MaturityModel, on_delete=models.SET_NULL, null=True, blank=True)
	start_date = models.DateField('date_started', null=True, blank=True)
	end_date = models.DateField('date_ended', null=True, blank=True)
	create_date = models.DateField(auto_now_add=True)  # Automatically set this date when added
	def __str__(self):
		return self.title

class Comment(models.Model):
	comment_date = models.DateField()
	comment_text = models.CharField(max_length=200)
	comment_user = models.ForeignKey(Contact, on_delete=models.CASCADE)
	comment_tracker = models.ForeignKey(Tracker, on_delete=models.SET_NULL, null=True, blank=True)
	def __str__(self):
		return self.comment_text

class Update(models.Model):
	update_date = models.DateField()
	update_text = models.CharField(max_length=150)
	update_user = models.ForeignKey(Contact, on_delete=models.CASCADE)
	update_tracker = models.ForeignKey(Tracker, on_delete=models.SET_NULL, null=True, blank=True)
	def __str__(self):
		return self.update_text