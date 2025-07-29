# C:\DMP\DMP\distribution_demo\views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt # Important for external calls, but be cautious in production!
from django.utils import timezone
import json
import os
import requests # You might need to install this: pip install requests
import logging

from .models import SimulatedRelease

logger = logging.getLogger(__name__)

# This is a placeholder for your home page
def home(request):
    return HttpResponse("Welcome to the DSP Distribution Demo! Go to /admin/ to manage releases.")

@csrf_exempt # For simplicity in demo, but review CSRF for production APIs
def distribute_release(request, release_id):
    """
    Simulates the distribution of a release to a DSP.
    In a real scenario, this would involve complex logic to
    format data and send it via an API to a real DSP or aggregator.
    """
    release = get_object_or_404(SimulatedRelease, pk=release_id)

    if request.method == 'POST':
        # --- SIMULATION START ---

        # Prepare data that would be sent to a DSP
        # In reality, this would be highly structured (e.g., DDEX XML, JSON specific to DSP)
        distribution_data = {
            'release_id': release.id,
            'title': release.title,
            'artist': release.artist_name,
            'release_date': str(release.release_date),
            'metadata_version': '1.0', # Example
            'source_system': 'DjangoMusicPublisher', # Example
            # Add more relevant fields from DMP's Release/Recording models
        }

        # Simulate sending data to a "DSP endpoint"
        # This could be a local dummy server or just a log entry
        simulated_dsp_endpoint = os.getenv('SIMULATED_DSP_ENDPOINT', 'http://127.0.0.1:8001/receive_distribution/')

        try:
            # In a real scenario, you'd use requests.post() to send to a real API
            # For this demo, we'll try sending to a local dummy receiver
            response = requests.post(
                simulated_dsp_endpoint,
                json=distribution_data,
                timeout=5 # Timeout for the request
            )
            response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)

            # If successful
            release.is_distributed = True
            release.last_distribution_attempt = timezone.now()
            release.distribution_status = 'Sent to Simulated DSP'
            release.save()

            logger.info(f"Successfully simulated distribution for release {release.id}: {release.title}")
            return JsonResponse({'status': 'success', 'message': f'Release {release.id} distributed to simulated DSP.'})

        except requests.exceptions.ConnectionError as e:
            release.distribution_status = 'Failed: Connection Error'
            release.save()
            logger.error(f"Failed to connect to simulated DSP for release {release.id}: {e}")
            return JsonResponse({'status': 'error', 'message': f'Failed to connect to simulated DSP: {e}'}, status=500)
        except requests.exceptions.Timeout as e:
            release.distribution_status = 'Failed: Timeout'
            release.save()
            logger.error(f"Simulated DSP request timed out for release {release.id}: {e}")
            return JsonResponse({'status': 'error', 'message': f'Simulated DSP request timed out: {e}'}, status=500)
        except requests.exceptions.RequestException as e:
            release.distribution_status = 'Failed: Request Error'
            release.save()
            logger.error(f"Error during simulated DSP request for release {release.id}: {e}")
            return JsonResponse({'status': 'error', 'message': f'Error during simulated DSP request: {e}'}, status=500)
        except Exception as e:
            release.distribution_status = 'Failed: Internal Error'
            release.save()
            logger.error(f"An unexpected error occurred during distribution for release {release.id}: {e}")
            return JsonResponse({'status': 'error', 'message': f'An unexpected error occurred: {e}'}, status=500)

        # --- SIMULATION END ---

    else:
        return JsonResponse({'status': 'error', 'message': 'Only POST requests are allowed for distribution.'}, status=405)