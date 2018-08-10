"""
This module contains views specific to the API.  This is not named
according to any specific naming-convention, but seemed most logical
in this situation
"""

from rest_framework import viewsets
from .models import Tracker, Contact
from .serializers import FullTrackerSerializer, ContactSerializer


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
