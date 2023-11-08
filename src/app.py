from flask import Flask, request, jsonify, make_response
import uuid

BASE_URL = '/api/v1.0/'

nbaTeams = [
    {
        "teamId": str(uuid.uuid1()),
        "abbreviation": "ATL",
        "teamName": "Atlanta Hawks",
        "knownAs": "Hawks",
        "location": "Atlanta"
    },
    {
        "teamId": str(uuid.uuid1()),
        "abbreviation": "BOS",
        "teamName": "Boston Celtics",
        "knownAs": "Celtics",
        "location": "Boston"
    },
    {
        "teamId": str(uuid.uuid1()),
        "abbreviation": "BKN",
        "teamName": "Brooklyn Nets",
        "knownAs": "Nets",
        "location": "Brooklyn"
    },
    {
        "teamId": str(uuid.uuid1()),
        "abbreviation": "CHA",
        "teamName": "Charlotte Hornets",
        "knownAs": "Hornets",
        "location": "Charlotte"
    },
    {
        "teamId": str(uuid.uuid1()),
        "abbreviation": "CHI",
        "teamName": "Chicago Bulls",
        "knownAs": "Bulls",
        "location": "Chicago"
    },
    {
        "teamId": str(uuid.uuid1()),
        "abbreviation": "CLE",
        "teamName": "Cleveland Cavaliers",
        "knownAs": "Cavaliers",
        "location": "Cleveland"
    },
    {
        "teamId": str(uuid.uuid1()),
        "abbreviation": "DAL",
        "teamName": "Dallas Mavericks",
        "knownAs": "Mavericks",
        "location": "Dallas"
    },
    {
        "teamId": str(uuid.uuid1()),
        "abbreviation": "DEN",
        "teamName": "Denver Nuggets",
        "knownAs": "Nuggets",
        "location": "Denver"
    },
    {
        "teamId": str(uuid.uuid1()),
        "abbreviation": "DET",
        "teamName": "Detroit Pistons",
        "knownAs": "Pistons",
        "location": "Detroit"
    },
    {
        "teamId": str(uuid.uuid1()),
        "abbreviation": "GSW",
        "teamName": "Golden State Warriors",
        "knownAs": "Warriors",
        "location": "Golden State"
    },
    {
        "teamId": str(uuid.uuid1()),
        "abbreviation": "HOU",
        "teamName": "Houston Rockets",
        "knownAs": "Rockets",
        "location": "Houston"
    },
    {
        "teamId": str(uuid.uuid1()),
        "abbreviation": "IND",
        "teamName": "Indiana Pacers",
        "knownAs": "Pacers",
        "location": "Indiana"
    },
    {
        "teamId": str(uuid.uuid1()),
        "abbreviation": "LAC",
        "teamName": "Los Angeles Clippers",
        "knownAs": "Clippers",
        "location": "Los Angeles"
    },
    {
        "teamId": str(uuid.uuid1()),
        "abbreviation": "LAL",
        "teamName": "Los Angeles Lakers",
        "knownAs": "Lakers",
        "location": "Los Angeles"
    },
    {
        "teamId": str(uuid.uuid1()),
        "abbreviation": "MEM",
        "teamName": "Memphis Grizzlies",
        "knownAs": "Grizzlies",
        "location": "Memphis"
    },
    {
        "teamId": str(uuid.uuid1()),
        "abbreviation": "MIA",
        "teamName": "Miami Heat",
        "knownAs": "Heat",
        "location": "Miami"
    },
    {
        "teamId": str(uuid.uuid1()),
        "abbreviation": "MIL",
        "teamName": "Milwaukee Bucks",
        "knownAs": "Bucks",
        "location": "Milwaukee"
    },
    {
        "teamId": str(uuid.uuid1()),
        "abbreviation": "MIN",
        "teamName": "Minnesota Timberwolves",
        "knownAs": "Timberwolves",
        "location": "Minnesota"
    },
    {
        "teamId": str(uuid.uuid1()),
        "abbreviation": "NOP",
        "teamName": "New Orleans Pelicans",
        "knownAs": "Pelicans",
        "location": "New Orleans"
    },
    {
        "teamId": str(uuid.uuid1()),
        "abbreviation": "NYK",
        "teamName": "New York Knicks",
        "knownAs": "Knicks",
        "location": "New York"
    },
    {
        "teamId": str(uuid.uuid1()),
        "abbreviation": "OKC",
        "teamName": "Oklahoma City Thunder",
        "knownAs": "Thunder",
        "location": "Oklahoma City"
    },
    {
        "teamId": str(uuid.uuid1()),
        "abbreviation": "ORL",
        "teamName": "Orlando Magic",
        "knownAs": "Magic",
        "location": "Orlando"
    },
    {
        "teamId": str(uuid.uuid1()),
        "abbreviation": "PHI",
        "teamName": "Philadelphia 76ers",
        "knownAs": "76ers",
        "location": "Philadelphia"
    },
    {
        "teamId": str(uuid.uuid1()),
        "abbreviation": "PHX",
        "teamName": "Phoenix Suns",
        "knownAs": "Suns",
        "location": "Phoenix"
    },
    {
        "teamId": str(uuid.uuid1()),
        "abbreviation": "POR",
        "teamName": "Portland Trail Blazers",
        "knownAs": "Trail Blazers",
        "location": "Portland"
    },
    {
        "teamId": str(uuid.uuid1()),
        "abbreviation": "SAC",
        "teamName": "Sacramento Kings",
        "knownAs": "Kings",
        "location": "Sacramento"
    },
    {
        "teamId": str(uuid.uuid1()),
        "abbreviation": "SAS",
        "teamName": "San Antonio Spurs",
        "knownAs": "Spurs",
        "location": "San Antonio"
    },
    {
        "teamId": str(uuid.uuid1()),
        "abbreviation": "TOR",
        "teamName": "Toronto Raptors",
        "knownAs": "Raptors",
        "location": "Toronto"
    },
    {
        "teamId": str(uuid.uuid1()),
        "abbreviation": "UTA",
        "teamName": "Utah Jazz",
        "knownAs": "Jazz",
        "location": "Utah"
    },
    {
        "teamId": str(uuid.uuid1()),
        "abbreviation": "WAS",
        "teamName": "Washington Wizards",
        "knownAs": "Wizards",
        "location": "Washington"
    }
]


app = Flask(__name__)

@app.route(BASE_URL + "/teams", methods=["GET"])
def getAllTeams():
    return make_response(jsonify(nbaTeams), 200)

@app.route(BASE_URL + "/teams/<string:id>", methods=["GET"])
def get_team_by_id(id):
    return_team = [team for team in nbaTeams if team["teamId"] == id]

    if return_team:
        return make_response(jsonify(return_team[0]), 200)
    else:
        return make_response("A team with an Id: {}, was not found".format(id), 404)

@app.route(BASE_URL + "/teams", methods=["POST"])
def addTeam():
    nextId = str(uuid.uuid1())
    newTeam = {
        "abbreviation": request.form["abbreviation"],
        "teamName": request.form["name"],
        "knownAs": request.form["knownAs"],
        "location": request.form["location"]
    }
    nbaTeams[nextId] = newTeam
    if nbaTeams.append(newTeam):
        return make_response(jsonify(newTeam), 201)
    else:
        return  make_response(jsonify)

@app.route(BASE_URL + "/teams/<string:id>", methods=["PUT"])
def editTeam(id):
    for team in nbaTeams:
        if team["teamId"] == id:
            team["abbreviation"] = request.form["abbreviation"]
            team["teamName"] = request.form["name"]
            team["knownAs"] = request.form["knownAs"]
            team["location"] = request.form["location"]
            return make_response(jsonify(team), 200)

    return make_response("Team not found", 404)


@app.route(BASE_URL+"/teams/<string:id>", methods=["DELETE"])
def deleteTeam(id):
    for team in nbaTeams:
        if team["teamId"] == id:
            nbaTeams.remove(team)
            break
    return make_response(jsonify({}), 200)

if __name__ == "__main__":
    app.run(debug=True)
