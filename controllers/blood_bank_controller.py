from services.blood_bank_service import BloodBankService
from flask import Blueprint, jsonify,request,url_for
from constants.api_response_constants import BaseResponse,ResponseCode

blueprint = Blueprint("blood_bank_blueprint",__name__,url_prefix="/blood_banks")


@blueprint.route("/all",methods=["GET"])
def get_all_blood_banks():
    # per_page = int(request.args.get('per_page',None))
    page = request.args.get('page',None)

    if page:
        page = int(page)
        
        all_blood_bank_data = BloodBankService.get_paginated_blood_banks(formatted=True,page=page)
    
        if all_blood_bank_data:
            
            return jsonify(BaseResponse(1,ResponseCode.SUCCESS,None,all_blood_bank_data).to_json()),200
        return jsonify(BaseResponse(0,ResponseCode.RESOURCE_NOT_FOUND,"no blood banks data found",None).to_json()),201

    all_blood_bank_data = BloodBankService.get_all_blood_banks(True)
    if all_blood_bank_data:
        return jsonify(BaseResponse(1,ResponseCode.SUCCESS,None,all_blood_bank_data).to_json()),200
    return jsonify(BaseResponse(0,ResponseCode.RESOURCE_NOT_FOUND,"no blood banks data found",None).to_json()),201


@blueprint.route("/create",methods=["POST"])
def post_blood_bank():
    post_json = request.get_json()
    blood_bank = BloodBankService.create_blood_bank(post_json,formatted=True)
    if blood_bank:
        return jsonify(BaseResponse(1,ResponseCode.SUCCESS,None,blood_bank).to_json()),201
    return jsonify(BaseResponse(0,ResponseCode.INVALID_REQUEST_DATA,"correct data not sent by user",None).to_json()),400


@blueprint.route("/<blood_type>",methods=["GET"])
def get_filtered_blood_banks(blood_type):
    if blood_type:
        blood_banks = BloodBankService.get_blood_bank_avail_btype(blood_type,formatted=True)
        if blood_banks:
            return jsonify(BaseResponse(1,ResponseCode.SUCCESS,None,blood_banks).to_json()),200
        return jsonify(BaseResponse(0,ResponseCode.RESOURCE_NOT_FOUND,"no blood banks found",None).to_json()),201
    return jsonify(BaseResponse(0,ResponseCode.RESOURCE_NOT_FOUND,"no blood banks found",None).to_json()),201


@blueprint.route("/<state>",methods=["GET"])
def get_blood_banks_by_state(state):
    if state:
        blood_banks = BloodBankService.find_by_state(state,True)
        if blood_banks:
            return jsonify(BaseResponse(1,ResponseCode.SUCCESS,None,blood_banks).to_json()),200
        return jsonify(BaseResponse(0,ResponseCode.RESOURCE_NOT_FOUND,"no blood banks found",None).to_json()),201
    return jsonify(BaseResponse(0,ResponseCode.RESOURCE_NOT_FOUND,"no blood banks found",None).to_json()),201


@blueprint.route("/<city>",methods=["GET"])
def find_by_city(city):
    if city:
        blood_banks = BloodBankService.find_by_city(city,True)
        if blood_banks:
            return jsonify(BaseResponse(1,ResponseCode.SUCCESS,None,blood_banks).to_json()),200
        return jsonify(BaseResponse(0,ResponseCode.RESOURCE_NOT_FOUND,"no blood banks found",None).to_json()),201
    return jsonify(BaseResponse(0,ResponseCode.RESOURCE_NOT_FOUND,"no blood banks found",None).to_json()),201

@blueprint.route("/states",methods=["GET"])
def get_all_states():
    states = BloodBankService.get_all_states()
    if states:
        return jsonify(BaseResponse(1,ResponseCode.SUCCESS,None,states).to_json()),200
    return jsonify(BaseResponse(0,ResponseCode.RESOURCE_NOT_FOUND,"no states found",None).to_json()),201

@blueprint.route("cities/<state>",methods=["GET"])
def get_city_by_state(state):
    cities = BloodBankService.get_city_by_state(state)
    if cities:
        return jsonify(BaseResponse(1,ResponseCode.SUCCESS,None,cities).to_json()),200
    return jsonify(BaseResponse(0,ResponseCode.RESOURCE_NOT_FOUND,"no cities found",None).to_json()),201
