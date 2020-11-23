from flask import Blueprint, request

valid_query_params = ['teamID', 'orderby']

users_routes = Blueprint('users_routes', __name__)
@users_routes.route('/users', methods=['GET', 'POST'])
def users_list():
    if request.method == 'GET':
        if request.query_string:
            if (
                request.args.get('teamID') is None and 
                request.args.get('orderby') is None
            ):
                return "Bad request param", 400
            if request.args.get('teamID'):
                # do team ID select
                pass
            if request.args.get('orderby'):
                # do orderby select
                pass
        else:
            # select entire users list
            pass
    elif request.method == 'POST':
        # create the user breh
        pass

    else:
        return "Bad request method breh", 405


    return "users brah"

    