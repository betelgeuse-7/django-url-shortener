from django.shortcuts import render, redirect

from django.views.generic import View

from .models import URL

from random_url.generate import generate_random_url

from django.http import JsonResponse
import json


class Index(View):
    def get(self, request):
        return render(request, 'index.html')

    def post(self, request):
        url_to_shorten = json.loads(request.body)['url']

        if url_to_shorten:
            urls = URL.objects.all()
            raw_urls = []

            for url in urls:
                raw_urls.append(url.raw_url)

            if url_to_shorten in raw_urls:

                try:
                    existing_short_url = URL.objects.get(
                        raw_url=url_to_shorten).shortened_url

                    return JsonResponse(
                        {
                            "msg": "This url already exists.",
                            "url": existing_short_url
                        }
                    )
                except:
                    return JsonResponse(
                        {
                            "msg": "An error occured."
                        }
                    )
            else:
                url = generate_random_url(10)

                URL.objects.create(raw_url=url_to_shorten, shortened_url=url)

                return JsonResponse(
                    {
                        "msg": "URL has been successfully shortened. ",
                        "url": url
                    }
                )

        else:
            return render(request, 'error.html')


class Redirect(View):
    def get(self, request, url):
        try:
            url_to_redirect_to = URL.objects.get(shortened_url=url).raw_url
            return redirect(url_to_redirect_to)
        except:
            return render(request, 'error.html')
