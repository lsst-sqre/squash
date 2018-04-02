import os
import requests

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from bokeh.embed import server_document

# if not specified use the local url for development
SQUASH_BOKEH_URL = os.environ.get('SQUASH_BOKEH_URL', 'http://localhost:5006')
SQUASH_API_URL = os.environ.get('SQUASH_API_URL', 'http://localhost:5000')
SQUASH_GRAPHQL_URL = os.environ.get('SQUASH_GRAPHQL_URL', None)


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

        if bokeh_app == 'monitor' or bokeh_app == 'AMx':
            # https://bokeh.pydata.org/en/latest/docs/user_guide/embed.html#server-data
            bokeh_script = server_document(url="{}/{}".format(SQUASH_BOKEH_URL,
                                                              bokeh_app),
                                           arguments=args)

    template = loader.get_template('dash/embed_bokeh.html')

    context = {'bokeh_script': bokeh_script,
               'bokeh_app': bokeh_app}

    response = HttpResponse(template.render(context, request))

    return response


def api(request):
    """Render the API page"""
    return HttpResponseRedirect(SQUASH_API_URL)

def graphql(request):
    """Redirect to the GraphQL service"""
    return HttpResponseRedirect(SQUASH_GRAPHQL_URL)

def admin(request):
    """Redirect to the django admin interface"""
    admin_url = "{}/admin/".format(SQUASH_API_URL)
    return HttpResponseRedirect(admin_url)

def home(request):
    """Render the initial page, including statistics"""


    context = {"datasets": None, "latest_job_date": None,
               "number_of_jobs": None, "number_of_packages": None,
               "number_of_metrics": None, "number_of_measurements": None}

    try:
        context = requests.get("{}/stats".format(SQUASH_API_URL)).json()
    except Exception:
        print("Could not reach {}".format(SQUASH_API_URL))


    return render(request, 'dash/index.html', context)
