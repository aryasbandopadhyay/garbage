from django.shortcuts import render,redirect
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import TextOperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import TextRecognitionMode
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time
def index(request,id,image,imgloc):
    
    
    subscription_key = 'ffe34b77508440fcb2882aec460f27b4'
    endpoint = 'https://centralindia.api.cognitive.microsoft.com/'

    computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
    remote_image_url = "http://akshatkhanna.co/upload/"+image
    ######## list to store keywords for each label

    stray = ['cow', 'mammal', 'buffalo', 'cattle', 'herd', 'donkey', 'horse']
    garbage = ['litter', 'garbage', 'dirt', 'trash', 'plastic', 'waste container', 'dustbin']
    potholes = ['hole', 'water', 'rock']
    others=['cow', 'mammal', 'buffalo', 'cattle', 'herd', 'donkey', 'horse','litter', 'garbage', 'dirt', 'trash', 'plastic', 'waste container', 'dustbin','hole', 'water', 'rock']

    classes = []
    tags_result_remote = computervision_client.tag_image(remote_image_url )

    if (len(tags_result_remote.tags) == 0):
        classes.append(3)
    else:
        for tag in tags_result_remote.tags:
            #print(tag.name, tag.confidence)
            if tag.name in potholes:
                classes.append(1)
    
            if tag.name in garbage:
                classes.append(0)
        
            if tag.name in stray:
                classes.append(2)
            
            if tag.name not in others:
                classes.append(3)


    c=list(set(classes))
    if 3 in c and len(c) > 1:
        c.remove(3)
    #print(c)
    s=str(c[0])
    for item in c[1:]:
        s=s+','+str(item)
    



    



    
    return redirect('http://akshatkhanna.pythonanywhere.com/post/'+id+'/'+image+'/'+imgloc+'/'+s)