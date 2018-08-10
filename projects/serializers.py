"""
This module contains serializer (input/output format)
specifications for all models served by Django REST Framework
"""
from .models import (
	Status,
	Task,
	DTContact,
	Contact,
	Alignment,
	Keyword,
	MaturityModel,
	Comment,
	Update,
	Tracker,
)

from rest_framework import serializers


class StatusSerializer(serializers.ModelSerializer):
	"""Serializer for the projects.models.Status model"""

	class Meta:
		model = Status
		fields = ['status_text']


class SimpleTrackerSerializer(serializers.ModelSerializer):
	"""
	Simple Serializer for the projects.models.Tracker model
	which does not follow nested relationships
	"""
	status = StatusSerializer()

	class Meta:
		model = Tracker
		fields = [
			'title',
			'status',
			'create_date',
			'start_date',
			'end_date',
		]


class ContactSerializer(serializers.ModelSerializer):
	"""Serializer for the projects.models.Contact model"""
	trackers = SimpleTrackerSerializer(source='tracker_set', many=True, read_only=True)

	class Meta:
		model = Contact
		fields = '__all__'


class RelatedContactSerializer(serializers.ModelSerializer):
	"""
	Serializer for the projects.models.Contact model for use when
	referencing from another model
	"""

	class Meta:
		model = Contact
		read_only_fields = ['pk']  # Include primary key, but do not allow editing
		fields = [
			'contact_fname',
			'contact_lname',
			'contact_phone',
		]


class FullTrackerSerializer(serializers.ModelSerializer):
	"""Serializer for listing all details of a projects.models.Tracker model"""
	contact = RelatedContactSerializer()

	def create(self, validated_data):
		"""
		This method is needed because we want to create data across foreign key
		relationships, which cannot be done automatically by Django REST Framework
		"""
		# This removes the RelatedContactSerializer data from the FullTrackerSerializer
		print(validated_data)
		contact_data = validated_data.pop('contact')

		# This checks if contact_data was included, and if so handles it
		if contact_data:
			# This either retrieves the contact defined by contact_data,
			# or creates a row in the Contact table with contact_data
			contact, was_new_contact_created = Contact.objects.get_or_create(**contact_data)
		else:
			# If contact_data was not included, set contact to None
			contact = None

		# This creates a row in the Tracker table (which can now be done because
		# contact data was removed from the validated_data dictionary with validated_data.pop('contact')
		tracker, was_new_tracker_created = Tracker.objects.update_or_create(contact=contact, **validated_data)
		tracker

		return tracker

	def update(self, instance, validated_data):
		"""TODO: This should be very similar to the FullTrackerSerialzier#create method"""
		pass

	class Meta:
		model = Tracker
		depth = 2  # This says include up to 2 levels of foreign keys
		fields = '__all__'
