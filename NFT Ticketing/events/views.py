from django.http import HttpResponse
from django.shortcuts import render
from .models import *
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import cv2
import threading
######
import json
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Events
from django.contrib import messages
import os
from web3 import Web3
from events.pinata_upload import create_pinata
import time

def home(request):
    EventsData = Events.objects.all()
    data = {'EventsData':EventsData}

    return render(request,"events/events.html",data)
    

#########3######## START  EVENT ###########################

def create_event(request):
    if request.method=='POST':  
        event_name        = request.POST['event_name'] 
        event_description = request.POST['event_description']
        max_tickets       = request.POST['max_tickets']
        start_date        = request.POST['start_date']
        end_date          = request.POST['end_date']   
        image               = request.FILES['image_upload']
        account_id        = request.user.email
        request.session['event_name'] = event_name
        contract_response = create_event_contract(event_name,max_tickets)
        contract_status = contract_response[0]
        
        if contract_status:
            event_object = Events(event_name=event_name,event_description=event_description,max_tickets=max_tickets,start_date=start_date,end_date=end_date,image_path=image, account_id=account_id, abi="False",contract_hash="False")     
            event_object.save()                        
            messages.success(request,"Your Event has been compiled Successfully")
            return redirect('deploy_Event')
        else:            
            messages.success(request,"Your Event Compilation has Encounted some Error")
            return redirect('home')

    return(render(request,"events/create_event.html"))

def create_event_contract(event_name,max_tickets):
    with open("../event.sol") as f:
        contents = f.read()
    contents = contents.replace("event_name",event_name)
    contents = contents.replace("max_tickets",max_tickets)    
    
    f = open("../../NFT/react-node-connect/server/contracts/ticket.sol", "w")
    f.write(contents)
    f.close()
    return compile()         

def compile():
    current_directory = os.getcwd()
    os.chdir('../../NFT/react-node-connect/server/contracts')
    import subprocess
    output = subprocess.getoutput("truffle compile")
    print(output)
    os.chdir(current_directory)    
    try:
        address = output[output.index('Compiled successfully'):]        
        return(True,address)
    except Exception as e:
        return(False,e)


def deploy_event(request):
    if request.method=='POST':  
        print("In Deploy Event")
        account_id     = request.user.email
        contract_hash  = request.POST['contract_hash']
        abi            = request.POST['abi']
        event_objs = Events.objects.filter(account_id=account_id)
        
        for event_obj in event_objs:
            if event_obj.contract_hash == "False":
                event_obj.contract_hash = contract_hash
                event_obj.abi           = str(abi)
                event_obj.save()
                break
        return redirect('home')

    import json
    account_id     = request.user.email
    event_name = request.session['event_name']    

    event_objs = Events.objects.filter(account_id=account_id)
    f = open('../../NFT/react-node-connect/server/build/contracts/{}.json'.format('Tickets'))#event_name))        
    data = json.load(f)        
    abi = data['abi']
    bytecode = data['bytecode']
    f.close()
    data = {"abi":abi,"bytecode":bytecode}    
    return render(request,"events/deploy_events.html",{'abi':abi,'bytecode':bytecode})

###################################### END CREATE EVENT #############################

def event_page(request):
    if request.method=='GET':  
        event_id            = request.GET['id']
        print("Event iD ",event_id)
        event_objs = Events.objects.filter(id=event_id)
        event_objs = event_objs[0]
        event_name = event_objs.event_name        
        event_description = event_objs.event_description
        abi               = event_objs.abi
        contract_hash  = event_objs.contract_hash   
        image_path     = event_objs.image_path 
        ipfs_file      = event_objs.nft_metadata 
        contract_address = event_objs.contract_address
        if contract_address == "False":
            try:                                                                           
                web3 = Web3(Web3.HTTPProvider("https://rpc-mumbai.maticvigil.com/"))            
                contract_address = web3.eth.get_transaction_receipt(contract_hash)
                contract_address = contract_address['contractAddress']            
                event_objs.contract_address = contract_address.lower()                
                ipfs_file = create_pinata(event_name,image_path,event_description)                
                event_objs.nft_metadata = ipfs_file
                event_objs.save()                
            except Exception as e:            
                print("Except: ",e)
                pass
        
        return render(request,"events/event_page.html",{'event_name':event_name,'event_description':event_description,'abi':abi,'contract_address':contract_hash,'image_path':image_path,'nft_metadata':ipfs_file,'real_contract_address':contract_address})










def your_events(request):
    if request.method=='GET':  
        contract_address  = request.GET['contract_address']
        abi               = request.GET['abi']
        user_account      = request.user.email
    return render(request,"events/your_events.html",{'abi':abi ,'contract_address':contract_address,'user_account':user_account}) 























####################################################### TICKETS ###############################################

def your_tickets(request):    
    import requests
    import json
    user_account = request.user
    print(user_account)
    print("User Account")
    url = 'https://polygon-mumbai.g.alchemy.com/nft/v2/h_ITS8wdWU0T3YCRCFRmsORX4e0_j2Cb/getNFTs?owner={}'.format(user_account)
    x = requests.get(url) 
    x = json.loads(x.text)
    x = x['ownedNfts']    
    return render(request,"tickets/your_tickets.html",{'data':x,'user_account':user_account})
        

def ticket_page(request):
    import qrcode  

    if request.method=='GET':  
        contract_address            = request.GET['address']
        tokenId                     = request.GET['tokenId']
        image_url                   = request.GET['image_url']
        user_account                = request.user.email
        
        qr_img = qrcode.make(user_account+"####"+tokenId)  
        qr_img.save('static/qr_images/qr-img.jpg')

        print("Address is:")
        print(contract_address)
        event_objs = Events.objects.filter(contract_address=contract_address) 
        print(event_objs)
        event_objs = event_objs[0]


        abi = event_objs.abi
        event_name = event_objs.event_name
        user_account = request.user
        print("User Acccount: ",user_account)
    return render(request,"tickets/ticket_page.html",{'event_name':event_name,'contract_address':contract_address,'tokenId':tokenId,'user_account':user_account,'abi':abi,'image_url':image_url})


def about(request):
    return render(request,"about.html")
