#give comment to all the functions
import json
from flask import Blueprint, jsonify, request,Flask
from config import *
from database import db, Users, Challenges, SolvedChallenges, Deployment
from sqlalchemy import text
import yaml
import docker
from threading import Thread
from deployer import deploy, instant_kill
from functools import wraps
from auth import auth
import time
import random

api = Blueprint('api', __name__) # create blueprint

config = ""
with open("./config/config.yaml", "r") as stream: # load config
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)
           
def secure(params=None): # decorator to check if required params are present in json body
    def decorator(f):
        @wraps(f)
        def check_authorization(*args, **kwargs):
            try:
                body = request.get_json()

                if params != None:
                    missing = [r for r in params if r not in body]
                    if missing:
                        raise ValueError("Required params not supplied.")
            except:
                response = {'status': 'fail', 'message': 'Invalid JSON body.'}
                return jsonify(response), 400

            print("Params:",params)
            print("Body",body)

            if params is None:
                return f()
            else:
                return f(* tuple(body[item] for item in params))
        return check_authorization
    return decorator

def clear_data(container_id,timeout): # function to clear data after timeout
    time.sleep(timeout)
    print("Trying to remove container record",flush=True)
    try:
        Deployment.query.filter_by(deployment_id=container_id).delete() # can remove this after docker api is independent of db
        db.session.commit()
    except Exception as e:
        print(e,flush=True)


@api.route('/api/get_images', methods=['GET']) # get all images
@auth.login_required
def get_images():
    result = []
    images = config["images"]
    for image in images:
        result.append(
            {"imagename": image["image_name"], "port": image["local_port"]})

    return jsonify({'status': 'success', "images": result})


@api.route('/api/get_deployments', methods=['POST']) # get all deployments
@auth.login_required
def get_deployments():
    if auth.current_user() != "admin":
        return jsonify({"status": "faill", "message": "Unauthorized"})
  
    result = {}
    client = docker.from_env()
    containers = client.containers.list()
    if(len(containers)==0):
        return jsonify({'status': 'fail', 'message': 'No deployments found.'}), 404
    for con in containers:
        result[con.attrs['Id']] = {
            "port": [con.ports[i][0]['HostPort'] if con.ports[i] else "not-found" for i in con.ports][0],
            "image_id": con.image.tags[0],
            "user_id": "admin",
            "deployment_id": con.attrs['Id'],
            "created_at": con.attrs['Created']
        }
        print(result)
    return jsonify({'status': 'success', 'deployments': result})

# WE CAN REMOVE THIS AFTER SOME TIME
@api.route('/api/get_user_deployments', methods=['POST'])
@secure(["user_id"])
def get_active_deployments(user_id):
    deployments = Deployment.query.filter_by(user_id=user_id).all()
    if deployments is None:
        return jsonify({'status': 'fail', 'message': 'No deployments found.'}), 404
    else:
        result = {}
        for deployment in deployments:
            result[deployment.image_id] = {
                "url": f"{HOST_IP}:{deployment.port}/"
            }
        return jsonify({'status': 'success', 'deployments': result})
# ======================================

@api.route('/api/deploy', methods=['POST']) # deploy image on random port in range PORT_RANGE in config file
@secure(["image_id", "user_id"])
def deploy_image(image_id, user_id):
    while True:
        port = random.randint(PORT_RANGE[0], PORT_RANGE[1])
        port_exists = Deployment.query.filter_by(port=port).first() # Replace with docker api
        if port_exists is None:
            break

    id,timeout = deploy(image_id, port, user_id) # deploy image
    deployment = Deployment(id, user_id, image_id, port, time.time())
    db.session.add(deployment)
    db.session.commit()
    clear_container_thread = Thread(target=clear_data, args=(id,timeout)) # start thread to clear data after timeout
    clear_container_thread.start() # start thread
    return jsonify({"status": "success", "port": port,"timeout": timeout})


@api.route('/api/kill', methods=['POST']) # kill image by deployment id (docker container id) 
@secure(["deployment_id", "user_id"])
def kill_image(deployment_id, user_id):
    current_containers = []
    client = docker.from_env()
    containers = client.containers.list() # get all containers from docker api
    for con in containers:
        current_containers.append(con.id)
    if(deployment_id in current_containers):
        current_containers.remove(deployment_id)
        instant_kill(deployment_id)
        return jsonify({"status": "success"})
    else:
        return jsonify({'status': 'fail', 'message': 'No such deployment.'}), 404
