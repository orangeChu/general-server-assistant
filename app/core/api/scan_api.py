from flask import Blueprint, request

from app.core.aop.authority import media_server_authentication
from app.core.model.plugin_respond import PluginRespond
from app.core.model.request_model import RequestModel
from app.core.service.scan_service import run_scan

api = Blueprint('scan_api', __name__)


@api.route('/scan', methods=['post'])
@media_server_authentication
def scan():
    """
        scan
    :return: respond model with metaDate
    """
    plugin_respond = PluginRespond()
    request_model = RequestModel(request)
    meta_data_list = run_scan(request_model.data)
    if meta_data_list and len(meta_data_list) > 0:
        plugin_respond.state = True
        plugin_respond.meta_data = meta_data_list
    else:
        plugin_respond.state = False
    return plugin_respond