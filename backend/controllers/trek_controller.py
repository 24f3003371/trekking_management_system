from flask import request , jsonify 
from backend.services.trek_service import create_trek,admin_manage_trek_routes,delete_trek,all_trek,update_trek