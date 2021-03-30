from django.shortcuts import render, redirect

from django.views.generic import View

from .models import URL

from random_url.generate import generate_random_url

from django.http import JsonResponse
import json


class Index(View):
    def get(self, request):
        recent_urls = URL.objects.all().order_by('-date')[:15]
        return render(request, 'index.html', {
            "recent_urls":recent_urls
        })

    def post(self, request):
        try:
            url_to_shorten = json.loads(request.body)['url']
            #ignoring wihtespaces.
            custom_url = json.loads(request.body)['custom_url']
        except:
            return JsonResponse({
                "msg": "Missing credentials",
                "url": "missing-credentials"
            })
        
        raw_urls = []

        if url_to_shorten:
            urls = URL.objects.all()

            for url in urls:
                raw_urls.append(url.raw_url)

            """URL ALREADY EXISTS"""
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
                """USE CUSTOM URL IF EXISTS"""
                if custom_url:
                    if custom_url in raw_urls:
                        existing_custom_url = URL.objects.get(
                        raw_url=url_to_shorten).shortened_url
                        return JsonResponse(
                            {
                                "msg": "This url already exists.",
                                "url": existing_custom_url
                            }
                        )
                    else:
                        URL.objects.create(raw_url=url_to_shorten, shortened_url=custom_url)
                        return JsonResponse(
                            {
                                "msg": "URL has been successfully shortened. ",
                                "url": custom_url
                            }
                        )
                        
                """IF NO CUSTOM URL"""
                url = generate_random_url(10)

                URL.objects.create(raw_url=url_to_shorten, shortened_url=url)

                return JsonResponse(
                    {
                        "msg": "URL has been successfully shortened. ",
                        "url": url
                    }
                )

class Redirect(View):
    def get(self, request, url):
        try:
            url_to_redirect_to = URL.objects.get(shortened_url=url).raw_url
            return redirect(url_to_redirect_to)
        except:
            return render(request, 'error.html')
