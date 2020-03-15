from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic import TemplateView
from core.forms import DataForm
from datetime import date, timedelta
import dateutil.parser as dparser
import numpy as np
import pandas as pd
import dload
import io
import socket
import urllib.request, urllib.error
from django.views.decorators.csrf import csrf_exempt

# import requests


class DownloadData:
    matrix = []
    endmatrix = []
    completelinks = []
    respon_links = []

    def __init__(self, link, days):
        self.link = link
        self.days = days

    def append_matrix(self):
        link1 = self.link.split("/")
        for i in range(self.days):
            self.matrix.append(link1)
        return self.matrix

    def append_end_matrix(self):
        matrix = self.append_matrix()
        for i in range(self.days):
            matrix[i][6] = (date.today() - timedelta(days=i + 1)).strftime("%Y")
            matrix[i][7] = (date.today() - timedelta(days=i + 1)).strftime("%b").upper()
            date1 = dparser.parse(matrix[i][8], fuzzy=True).strftime("%d%b%Y")
            string1 = matrix[i][8]
            string2 = string1.split(date1.upper())
            year = (date.today() - timedelta(days=i + 1)).strftime("%d%b%Y")
            string2.insert(1, year.upper())
            string3 = "".join(string2)
            self.endmatrix.append(string3)
        return self.endmatrix

    def using_numpy(self):
        matrix = self.append_matrix()
        endmatrix = self.append_end_matrix()
        a = np.array(matrix)
        for ele in range(self.days):
            a[ele][8] = "".join(endmatrix[ele])
        finallist = a.tolist()
        for i in range(self.days):
            # print("/".join(finallist[i]))
            self.completelinks.append("/".join(finallist[i]))
        return self.completelinks

    # def url_response(self, link):

    def res_links(self):
        var = self.respon_links

        def url_response(link):
            url = link
            try:
                try:
                    conn = urllib.request.urlopen(url, timeout=5)
                    var.append(url)
                except socket.timeout:
                    pass
            except urllib.error.HTTPError as e:
                # Return code error (e.g. 404, 501, ...)
                print("HTTPError: {}".format(e.code))
            except urllib.error.URLError as e:
                # Not an HTTP-specific error (e.g. connection refused)
                print("URLError: {}".format(e.reason))
            else:
                # 200
                # ...
                print("good")

            # return respon_links

        completelinks = self.using_numpy()
        for link in completelinks:
            url_response(link)
            # print(url_response(link))
        return var

    def copying_data(self):
        # print(path)
        mydataframe = pd.DataFrame()
        respon_link = self.res_links()
        print(respon_link)
        for li in respon_link:
            print(li)
            print("something")
            c = pd.read_csv(li)
            mydataframe = mydataframe.append(c, ignore_index=True)
        # mydataframe =
        print(mydataframe.shape)
        # mydataframe.to_csv(r"{0}".format(path), index=False)
        print(mydataframe.shape)
        return mydataframe
        # return mydataframe

    # def down1


# final_data.to_csv(index=False)


def sample_lead_file(request, days):
    link = "https://archives.nseindia.com/content/historical/EQUITIES/2020/FEB/cm27FEB2020bhav.csv.zip"
    # days = 5
    # path = "/home/madhu/Madhu/django_projects/datalore/files1/data3.csv"
    obj = DownloadData(link, days)
    mydataframe1 = obj.copying_data()
    my_data = mydataframe1.to_csv(index=False)
    sample_data = [my_data]
    response = HttpResponse(sample_data, content_type="text/plain")
    response["Content-Disposition"] = "attachment; filename={}".format(
        "sample_data.csv"
    )
    return response


@csrf_exempt
def data_view(request):
    form = DataForm()
    if request.method == "POST":
        days = request.POST.get("days")
        link = "https://archives.nseindia.com/content/historical/EQUITIES/2020/FEB/cm27FEB2020bhav.csv.zip"
        # days = 5
        # path = "/home/madhu/Madhu/django_projects/datalore/files1/data3.csv"
        obj = DownloadData(link, int(days))
        mydataframe1 = obj.copying_data()
        my_data = mydataframe1.to_csv(index=False)
        sample_data = [my_data]
        response = HttpResponse(sample_data, content_type="text/plain")
        response["Content-Disposition"] = "attachment; filename={}".format(
            "sample_data.csv"
        )
        return response
    data = {"form": form}
    return render(request, "home.html", data)
