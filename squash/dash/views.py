import os
import requests

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from bokeh.embed import server_document

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

    server_down_msg = "<h3>Error: Could not load SQUASH " \
                      "<mark>{}</mark> app. Bokeh server is" \
                      " down.</h3>".format(bokeh_app)

    not_implemented_msg = "<h3>Could not load SQUASH " \
                          "<mark>{}</mark>, this app is" \
                          " not implemented.</h3>".format(bokeh_app)

    # url args are passed to the bokeh document
    args = request.GET.dict()

    bokeh_script = server_down_msg

    if is_server_up(SQUASH_BOKEH_URL):
        bokeh_script = not_implemented_msg

        if bokeh_app == 'monitor' or bokeh_app == 'AMx':
            # https://bokeh.pydata.org/en/latest/docs/user_guide/embed.html#server-data
            bokeh_script = server_document(url="{}/{}".format(SQUASH_BOKEH_URL,
                                                              bokeh_app),
                                           arguments=args)

    template = loader.get_template('dash/embed_bokeh.html')

    context = {'bokeh_script': bokeh_script,
               'bokeh_app': bokeh_app,
               'squash_api_url': SQUASH_API_URL}

    response = HttpResponse(template.render(context, request))

    return response


def api(request):
    """Render the API page"""
    return HttpResponseRedirect(SQUASH_API_URL)


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
