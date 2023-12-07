from services.form_service import add_data

def createEntity(entity,form_data):
    #form_data =request.get_json(force=True)
    add_data(form_data,entity)
    return f"created entry, {entity}, data = {form_data}"

#@app.route(f"/api{api_path}", methods=['GET'])
def readEntity(entity,form_data):
    #form_data = request.data
    return f"read entry, {entity}, data = {form_data}"

#@app.route(f"/api{api_path}", methods=['PUT'])
def updateEntity(entity,form_data):
    #form_data = request.data
    return f"updated entry, {entity}, data = {form_data}"

#@app.route(f"/api{api_path}", methods=['DELETE'])
def deleteEntity(entity,form_data):
    #form_data = request.data
    return f"delete entry, {entity}, data = {form_data}"

form_controller = {
    "Create" : createEntity,
    "Read" : readEntity,
    "Update" : updateEntity,
    "Delete" : deleteEntity
}
 
#create_app()