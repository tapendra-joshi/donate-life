from services.event_service import EventService
from services.temp_user_service import TempUserService
from flask import Blueprint, jsonify,request,url_for
from constants.api_response_constants import BaseResponse,ResponseCode

blueprint = Blueprint("event_blueprint",__name__,url_prefix="/events")

@blueprint.route("/all",methods=["GET"])
def get_all_events():
    page = request.args.get('page',None)

    if page:
        page = int(page)
        all_events_data = EventService.get_paginated_events(page=page,formatted=True)

        if all_events_data:
            return jsonify(BaseResponse(1,ResponseCode.SUCCESS,None,all_events_data).to_json()),200
        return jsonify(BaseResponse(0,ResponseCode.RESOURCE_NOT_FOUND,"no events data found",None).to_json()),201
    all_events_data = EventService.get_all_events(formatted=True)
    if all_events_data:
        return jsonify(BaseResponse(1,ResponseCode.SUCCESS,None,all_events_data).to_json()),200
    return jsonify(BaseResponse(0,ResponseCode.RESOURCE_NOT_FOUND,"no events data found",None).to_json()),201


@blueprint.route("/event/create",methods=["POST"])
def post_event():
    post_json = request.get_json()
    event = EventService.create_event(post_json,formatted=True)
    if event:
        return jsonify(BaseResponse(1,ResponseCode.SUCCESS,None,event).to_json()),201
    return jsonify(BaseResponse(0,ResponseCode.INVALID_REQUEST_DATA,"correct data not sent by user",None).to_json()),400


@blueprint.route("/city/<city>",methods=["GET"])
def get_event_by_city(city):
    if city:
        events = EventService.find_by_city(city,True)
        if events:
            return jsonify(BaseResponse(1,ResponseCode.SUCCESS,None,events).to_json()),200
        return jsonify(BaseResponse(0,ResponseCode.RESOURCE_NOT_FOUND,"no events found",None).to_json()),201
    return jsonify(BaseResponse(0,ResponseCode.RESOURCE_NOT_FOUND,"Please provide a correct city",None).to_json()),201


@blueprint.route("/state/<state>",methods=["GET"])
def get_event_by_state(state):
    if state:
        events = EventService.find_by_state(state,True)
        if events:
            return jsonify(BaseResponse(1,ResponseCode.SUCCESS,None,events).to_json()),200
        return jsonify(BaseResponse(0,ResponseCode.RESOURCE_NOT_FOUND,"no events found",None).to_json()),201
    return jsonify(BaseResponse(0,ResponseCode.RESOURCE_NOT_FOUND,"Please provide a correct state",None).to_json()),201


@blueprint.route("/date",methods=["GET"])
def get_event_by_date():
    date = request.args.get('date',None)
    if date:
        events = EventService.find_by_date(date,True)
        if events:
            return jsonify(BaseResponse(1,ResponseCode.SUCCESS,None,events).to_json()),200
        return jsonify(BaseResponse(0,ResponseCode.RESOURCE_NOT_FOUND,"no events found for this date.",None).to_json()),201
    return jsonify(BaseResponse(0,ResponseCode.RESOURCE_NOT_FOUND,"Please provide a correct date",None).to_json()),201


@blueprint.route("/users/create",methods=["POST"])
def create_temp_user():
    post_data = request.get_json()
    user = TempUserService.create_user(post_data)
    if user:
            return jsonify(BaseResponse(1, ResponseCode.SUCCESS, "User created successfully", user).to_json()), 200
    return jsonify(BaseResponse(0, ResponseCode.UNKNOWN_ERROR, "There was some unknown error while creating the user", None).to_json()), 500


@blueprint.route("/organiser/<id>",methods=["GET"])
def get_event_by_organiser(id):
    if id:
        events =  EventService.find_by_organiser_id(id)
        if events:
            return jsonify(BaseResponse(1,ResponseCode.SUCCESS,None,events).to_json()),200
        return jsonify(BaseResponse(0,ResponseCode.RESOURCE_NOT_FOUND,"no events found for this id.",None).to_json()),201
    return jsonify(BaseResponse(0,ResponseCode.RESOURCE_NOT_FOUND,"Please provide a correct id",None).to_json()),201
