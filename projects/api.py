"""
This module contains views specific to the API.  This is not named
according to any specific naming-convention, but seemed most logical
in this situation
"""

from rest_framework import viewsets
from .models import Tracker, Contact, Keyword, Status
from .serializers import FullTrackerSerializer, ContactSerializer, KeywordSerializer, StatusSerializer


class TrackerViewSet(viewsets.ModelViewSet):
	"""
	This ViewSet adds API view actions for the following:

	* listing all trackers,
	* getting a single tracker by ID,
	* Updating a tracker,
	* Deleting a tracker,
	"""
	serializer_class = FullTrackerSerializer
	queryset = Tracker.objects.all()


class ContactViewSet(viewsets.ModelViewSet):
	"""
	This ViewSet adds API view actions for the following:

	* listing all contacts,
	* getting a single contact by ID,
	* Updating a contact,
	* Deleting a contact,
	"""
	serializer_class = ContactSerializer
	queryset = Contact.objects.all()

class KeywordViewSet(viewsets.ModelViewSet):
	"""
	This ViewSet adds API view actions for the following:

	* listing all keywords
	* getting a single keyword by ID,
	* Updating a keyword,
	* Deleting a keyword,
	"""
	serializer_class = KeywordSerializer
	queryset = Keyword.objects.all()

class StatusViewSet(viewsets.ModelViewSet):
	"""
	This ViewSet adds API view actions for the following:

	* listing all status,
	* getting a single status by ID,
	* Updating a status,
	* Deleting a status,
	"""
	serializer_class = StatusSerializer
	queryset = Status.objects.all()