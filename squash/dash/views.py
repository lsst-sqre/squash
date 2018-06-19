import os
import requests
import urllib

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from bokeh.embed import server_document

# default values are for local development
SQUASH_BOKEH_URL = os.environ.get('SQUASH_BOKEH_URL', 'http://localhost:5006')
SQUASH_API_URL = os.environ.get('SQUASH_API_URL', 'http://localhost:5000')
SQUASH_GRAPHQL_URL = os.environ.get('SQUASH_GRAPHQL_URL', None)

# list of allowed bokeh apps
SQUASH_BOKEH_APPS = os.environ.get('SQUASH_BOKEH_APPS',
                                   'monitor code_changes AMx')
# code_changes is the default monitor app
SQUASH_MONITOR_APP = os.environ.get('SQUASH_MONITOR_APP', 'code_changes')


def is_server_up(url):
    """"""
    server_up = True
    try:
        requests.head(url)
    except Exception:
        server_up = False

    return server_up


def embed_bokeh(request, bokeh_app):
    """Render the requested app from the bokeh server"""

    server_down_msg = "<h3>Error: Could not load SQUASH " \
                      "<mark>{}</mark> app. Bokeh server is unreachable." \
                      "</h3>".format(bokeh_app)

    not_implemented_msg = "<h3>Could not load SQUASH " \
                          "<mark>{}</mark>, this app is" \
                          " not implemented.</h3>".format(bokeh_app)

    # url args are passed to the bokeh document
    args = request.GET.dict()

    bokeh_script = server_down_msg

    if is_server_up(SQUASH_BOKEH_URL):
        bokeh_script = not_implemented_msg

        bokeh_apps = SQUASH_BOKEH_APPS.split(" ")

        if bokeh_app in bokeh_apps:
            # https://bokeh.pydata.org/en/latest/docs/user_guide/embed.html#server-data
            bokeh_script = server_document(url="{}/{}".format(SQUASH_BOKEH_URL,
                                                              bokeh_app),
                                           arguments=args)

    template = loader.get_template('dash/embed_bokeh.html')

    context = {'bokeh_script': bokeh_script,
               'bokeh_app': bokeh_app,
               'monitor_app': SQUASH_MONITOR_APP}

    response = HttpResponse(template.render(context, request))

    return response


def api(request):
    """Render the API page"""
    url = urllib.parse.urljoin(SQUASH_API_URL, "/apidocs")
    return HttpResponseRedirect(url)


def graphql(request):
    """Redirect to the GraphQL service"""
    return HttpResponseRedirect(SQUASH_GRAPHQL_URL)


def home(request):
    """Render the initial page, including statistics"""

    context = {"last_job_date": None,
               "number_of_jobs": None,
               "number_of_metrics": None,
               "number_of_measurements": None}
    try:
        context = requests.get("{}/stats".format(SQUASH_API_URL))\
            .json()['stats']
    except Exception:
        print("Could not reach {}/stats".format(SQUASH_API_URL))

    context['monitor_app'] = SQUASH_MONITOR_APP

    return render(request, 'dash/index.html', context)
