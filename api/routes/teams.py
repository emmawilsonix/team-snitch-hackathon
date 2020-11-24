from flask import Blueprint, request

teams_routes = Blueprint('teams_routes', __name__)
@teams_routes.route('/teams/<id>', methods=['GET', 'POST'])
def teams_list(id):
    if request.method == 'GET':
        if request.query_string:
            if request.args.get('orderby') is None:
                return "Bad request param breh", 400
            else:
                # do orderby select
                pass
        else if id != "":
            # select the team with teamID <id>
            pass
        else:
            # select entire teams list
            pass
    elif request.method == 'POST':
        teamID = request.form.get('id')
        teamName = request.form.get('name')
        
        if teamID is None or teamName is None:
            return "Bad request, incorrect POST information", 400
        
        # create the team       
        pass

    else:
        return "Bad request method", 405


    return "teams"