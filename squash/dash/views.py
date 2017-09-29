import os
import requests

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from bokeh.embed import autoload_server

# if not specified use the local url for development
SQUASH_BOKEH_URL = os.environ.get('SQUASH_BOKEH_URL', 'http://localhost:5006')
SQUASH_API_URL = os.environ.get('SQUASH_API_URL', 'http://localhost:8000/api')


def is_server_up(url):

    server_up = True
    try:
        requests.head(url)
    except:
        server_up = False

    return server_up


def embed_bokeh(request, bokeh_app):
    """Render the requested app from the bokeh server"""
    # http://bokeh.pydata.org/en/0.12.6/docs/reference/embed.html
    bokeh_script = "<h3>Error: Could not load SQUASH " \
                   "<mark>{}</mark> app.</h3>".format(bokeh_app)

    if is_server_up(SQUASH_BOKEH_URL):
        bokeh_script = autoload_server(None, app_path="/{}".format(bokeh_app),
                                       url=SQUASH_BOKEH_URL)

    template = loader.get_template('dash/embed_bokeh.html')

    context = {'bokeh_script': bokeh_script,
               'bokeh_app': bokeh_app,
               'squash_api_url': SQUASH_API_URL}

    response = HttpResponse(template.render(context, request))

    # Save full url path in the HTTP response, so that the bokeh
    # app can parse the parameters, e.g:
    # http://localhost:8000/dash/AMx/?metric=AM1&ci_dataset=cfht&ci_id=452
    response.set_cookie('squash_dash_full_path', request.get_full_path())

    return response


def home(request):
    """Render the home page"""

    # TODO: get statistics from the SQUASH API

    n_metrics = None
    n_packages = None
    n_jobs = None
    n_meas = None

    datasets = None
    last = None

    context = {"n_metrics": n_metrics,
               "n_packages": n_packages,
               "n_jobs": n_jobs,
               "n_meas": n_meas,
               "datasets": datasets,
               "last": last}

    return render(request, 'dash/index.html', context)
