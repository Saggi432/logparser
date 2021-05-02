import os


import re
import os
import logging
import subprocess
import fileinput

# import defaults
import sys
import time
import argparse
import datetime
import apache_log_parser
import json
from flask import jsonify
from collections import OrderedDict
import itertools


logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')





from flask import Flask
app = Flask(__name__)

@app.route("/stats")
def main():
    logging.info("Received a request")
    logListDic = []
    finalResponse = {"numberOfIp": "0", "ipMap": "", "httpCodeMap": "", "refererMap": ""}
    requestDistribution={"GET": 0,"PUT": 0, "DELETE": 0, "POST": 0}
    finalResponse = parseLogFile(logListDic,finalResponse,requestDistribution)

    logging.info("Returning the response back to browser")

    #logging.debug("The final response i am sending is", finalResponse)
    return jsonify(finalResponse)


def parseLogFile(logListDic,finalResponse,requestDistribution):
    totalIp=set()
    totalRef = set()
    ipToRequest={}

    with open("/mnt/access_log_20190520-125058.log", 'r') as f:
        lines = [line.rstrip() for line in f]
        #logging.debug("Lines list            : %r " % (lines))
    for line in lines:
        line_parser = apache_log_parser.make_parser("%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-agent}i\"")
        #logging.debug("The line parser output is",line_parser(line))


        logListDic.append(line_parser(line))

    logging.info("Loading logs in the dictionary complete now")


    for eachReq in logListDic:
        totalIp.add(eachReq["remote_host"])
        if eachReq["request_method"] == "GET":
            totalRef.add(eachReq["request_header_referer"])


    for eachReq in logListDic:
        if eachReq["request_method"] == "GET":
            requestDistribution["GET"] += 1
        if eachReq["request_method"] == "PUT":
            requestDistribution["PUT"] += 1
        if eachReq["request_method"] == "DELETE":
            requestDistribution["DELETE"] += 1
        if eachReq["request_method"] == "POST":
            requestDistribution["POST"] += 1



    ipDictionary = { i : 0 for i in totalIp }
    refDictionary = {i : 0 for i in totalRef }

    #logging.debug(refDictionary)



    #loggine.trace("Total number of IPS", len(ipDictionary))
    finalResponse["numberOfIp"] = len(ipDictionary)
    print("Total number of requests", requestDistribution)
    finalResponse["httpCodeMap"] = requestDistribution



    for eachReq in logListDic:
        #if eachReq["remote_host"] == "192.88.98.206":
            #print(eachReq)
        hostName = eachReq["remote_host"]
        referer = eachReq["request_header_referer"]

        ipDictionary[hostName] += 1
        if eachReq["request_method"] == "GET":
            #logging.debug("Referrer is", referer)

            refDictionary[referer] += 1


    #refererDict = dict(itertools.islice(sorted(refDictionary.items(), key=lambda x: x[1], reverse=True),5))

    sortedRef = sorted(refDictionary.items(), key=lambda x: x[1], reverse=True)
    top5Ref = sortedRef[:5]

    #logging.debug("referer dictionary", refererDict)

    finalResponse["refererMap"] = top5Ref

    finalResponse["ipMap"] = sorted(ipDictionary.items(), key=lambda x: x[1], reverse=True)


    # Final logging

    logging.info("The final topRef map is %s",top5Ref)
    logging.info("The final request distribution %s", requestDistribution)
    logging.info("The final number of unique Ips %d", len(ipDictionary))
    logging.info("For ipList, enable debug mode as its too verbose")


    logging.debug("The ip final list %s", ipDictionary)


    return finalResponse


@app.route("/")
def testHome():
    return("You can see some useful info at localhost:8080/stats")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
