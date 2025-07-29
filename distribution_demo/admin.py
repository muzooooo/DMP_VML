# C:\DMP\DMP\distribution_demo\admin.py
from django.contrib import admin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings
import requests # Make sure 'requests' is installed in your venv!
import json
import logging

from .models import SimulatedRelease
from music_publisher.admin import admin_site # Import the custom admin_site

logger = logging.getLogger(__name__)

class SimulatedReleaseAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist_name', 'release_date', 'is_distributed', 'distribution_status', 'id') # Added 'id' for easy reference
    list_filter = ('is_distributed', 'distribution_status')
    search_fields = ('title', 'artist_name')
    actions = ['distribute_selected_releases'] # <--- ADD THIS LINE

    def distribute_selected_releases(self, request, queryset):
        # This is the URL to your distribute_release view in distribution_demo/views.py
        # We'll use the current host and port to construct the URL
        # In a real setup, this might be a more robust URL generation or config value

        host = request.get_host() # e.g., 127.0.0.1:8000

        results = []
        for release in queryset:
            distribute_url = f"http://{host}{reverse('distribute_release', args=[release.id])}"

            try:
                # Send a POST request to your distribute_release view
                response = requests.post(distribute_url, timeout=10) # 10-second timeout
                response_data = response.json() # Assume JSON response from your view

                if response.status_code == 200 and response_data.get('status') == 'success':
                    self.message_user(request, f"Release '{release.title}' (ID: {release.id}) distributed successfully.")
                    logger.info(f"Admin action: Successfully triggered distribution for release {release.id}")
                else:
                    error_message = response_data.get('message', 'Unknown error')
                    self.message_user(request, f"Failed to distribute '{release.title}' (ID: {release.id}): {error_message}", level='error')
                    logger.error(f"Admin action: Failed to trigger distribution for release {release.id}: {error_message}")

            except requests.exceptions.RequestException as e:
                self.message_user(request, f"Network error distributing '{release.title}' (ID: {release.id}): {e}", level='error')
                logger.critical(f"Admin action: Network error during distribution for release {release.id}: {e}")
            except json.JSONDecodeError:
                self.message_user(request, f"Invalid JSON response from distribution endpoint for '{release.title}' (ID: {release.id})", level='error')
                logger.error(f"Admin action: Invalid JSON response for release {release.id}")
            except Exception as e:
                self.message_user(request, f"An unexpected error occurred distributing '{release.title}' (ID: {release.id}): {e}", level='error')
                logger.critical(f"Admin action: Unexpected error for release {release.id}: {e}")

        # This is important to refresh the page after the action
        return redirect(request.get_full_path())

    distribute_selected_releases.short_description = "Distribute selected releases to DSPs" # <--- ADD THIS LINE

# Register your model with the CUSTOM admin_site
admin_site.register(SimulatedRelease, SimulatedReleaseAdmin)