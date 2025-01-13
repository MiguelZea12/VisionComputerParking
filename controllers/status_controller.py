from flask import Blueprint, jsonify
from services.parking_service import occupied_spaces, free_spaces, historical_data, list1, list2, list3, list4, list5, list6, list7, list8, list9, list10, list11, list12
from services.parking_service import parking_state

status_controller = Blueprint('status_controller', __name__)

@status_controller.route('/spaces_status')
def spaces_status():
    state = parking_state.get_state()
    return jsonify(occupied=state["occupied"], free=state["free"])

@status_controller.route('/historical_data')
def historical_data():
    state = parking_state.get_state()
    return jsonify(historical=state["historical"])

@status_controller.route('/detailed_spaces_status')
def detailed_spaces_status():
    state = parking_state.get_state()
    detailed_status = [
        {"id": area, "status": "occupied" if occupied else "available"}
        for area, occupied in state["area_status"].items()
    ]
    return jsonify(detailed_status)

