from flask import Flask, jsonify, request, send_file
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from werkzeug import secure_filename
from flask_cors import CORS, cross_origin
import datetime
import os


path = "./pdf_store"
if not os.path.exists(path):
    os.mkdir(path)

app = Flask(__name__) #instancio la aplicación Flask
CORS(app)

#configuraciones de la app Flask
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://guillermoPiedrab:Guillermo174027447@guillermoPiedrabuena.mysql.pythonanywhere-services.com/guillermoPiedrab$defensaciudadana_webapi' #'mysql+mysqlconnector://defensaciudadana:Guillermo174027447@localhost/defensaciudadana_webapi' OR (PYTHONANYWHERE) 'mysql+mysqlconnector://guillermoPiedrab:Guillermo174027447@guillermoPiedrabuena.mysql.pythonanywhere-services.com/defensaciudadana_webapi'


db = SQLAlchemy(app) #instancio el objeto SQLAlchemy, pues estos son instancias de clases de los frameworck


class Clients(db.Model):
    clients_id = db.Column(db.Integer, primary_key=True)
    clients_name = db.Column(db.String(300), unique=True, nullable=False)
    clients_rut = db.Column(db.String(16), unique=True, nullable=False)
    clients_nationality = db.Column(db.String(300), unique=False, nullable=True)
    clients_civilStatus = db.Column(db.String(300), unique=False, nullable=True)
    clients_job = db.Column(db.String(300), unique=False, nullable=True)
    clients_address = db.Column(db.String(300), unique=False, nullable=True)
    clients_contact = db.Column(db.String(300), unique=False, nullable=True)

    clients_relationship_cases = db.relationship('Cases', backref='case_client')
    clients_relationship_corporations = db.relationship('Corporations', backref='corporation_client')


    def __repr__(self):
        return '<Clients %r>' % self.clients_id, self.clients_name, self.clients_rut, self.clients_nationality, self.clients_civilStatus, self.clients_job, self.clients_address, self.clients_contact

    def serialize(self):
        return {
            "clients_id": self.clients_id,
            "clients_name": self.clients_name,
            "clients_rut": self.clients_rut,
            "clients_nationality": self.clients_nationality,
            "clients_civilStatus": self.clients_civilStatus,
            "clients_job": self.clients_job,
            "clients_address": self.clients_address,
            "clients_contact": self.clients_contact,
        }

class Cases(db.Model):
    __tablename__ ='cases'
    cases_id = db.Column(db.Integer, primary_key=True)
    cases_description = db.Column(db.String(300), unique=False, nullable=False)
    cases_rol_rit_ruc = db.Column(db.String(300), unique=False, nullable=True)
    cases_trial_entity = db.Column(db.String(300), unique=False, nullable=False)
    cases_legalIssue = db.Column(db.String(300), unique=False, nullable=True)
    cases_procedure = db.Column(db.String(300), unique=False, nullable=True)
    cases_objetive = db.Column(db.String(300), unique=False, nullable=False)
    cases_update = db.Column(db.String(300), unique=False, nullable=True)
    cases_pendingTask = db.Column(db.String(300), unique=False, nullable=True)
    cases_updateDate = db.Column(db.DateTime, unique=False, nullable = True)
    cases_activeCase = db.Column(db.Boolean, unique=False, nullable=True)
    cases_incomeDate = db.Column(db.DateTime, unique=False, nullable = False, default=datetime.datetime.utcnow)
    cases_deadLine = db.Column(db.DateTime, unique=False, nullable = True)

    #se pone minuscula la tabla clients pues mira directamente a la base de datos y no a la clase de python
    cases_client_id = db.Column(db.Integer, db.ForeignKey('clients.clients_id'), nullable=False)

    cases_lawyer_id = db.Column(db.Integer, db.ForeignKey('lawyers.lawyers_id'), nullable=False)
    # establece relacion con tabla documents
    cases_relationship_documents = db.relationship('Documents', backref='case_document')


    def __repr__(self):
       return '<Cases %r>' %  self.cases_id, self.cases_description, self.cases_rol_rit_ruc, self.cases_trial_entity, self.cases_legalIssue, self.cases_procedure, self.cases_objetive, self.cases_update, self.cases_updateDate, self.cases_pendingTask, self.cases_activeCase, self.cases_incomeDate, self.cases_deadLine,

class Lawyers(db.Model):
    __tablename__ ='lawyers'
    lawyers_id = db.Column(db.Integer, primary_key=True)
    lawyers_name = db.Column(db.String(300), unique=True, nullable=False)
    lawyers_field = db.Column(db.String(300), unique=False, nullable=False)
    lawyers_rut = db.Column(db.String(300), unique=True, nullable=False)
    lawyers_password = db.Column(db.String(300), unique=False, nullable=False)

    lawyers_relationship_cases = db.relationship('Cases', backref='case_lawyer')


    def __repr__(self):
        return '<Lawyers %r>' % self.lawyers_id, self.lawyers_name, self.lawyers_field, self.lawyers_rut, self.lawyers_password

    def serialize(self):
        return {
            "lawyers_id": self.lawyers_id,
            "lawyers_name": self.lawyers_name,
            "lawyers_field": self.lawyers_field,
            "lawyers_rut": self.lawyers_rut,
            "lawyers_password": self.lawyers_password
        }


class Documents(db.Model):
    __tablename__='documents'
    documents_id = db.Column(db.Integer, primary_key=True)
    documents_type = db.Column(db.String(100), unique=False, nullable=True)
    documents_date = db.Column(db.DateTime, unique=False, nullable = False, server_default=func.now())

    documents_cases_id = db.Column(db.Integer, db.ForeignKey('cases.cases_id'))

    def __repr__(self):
        return '<Document %r>' % self.documents_id, self.documents_type, self.documents_date



class Corporations(db.Model):
    __tablename__='corporations'
    corporation_id = db.Column(db.Integer, primary_key=True)
    corporation_name = db.Column(db.String(300), unique=False, nullable=False)
    corporation_type = db.Column(db.String(300), unique=False, nullable=True)
    corporation_CBR = db.Column(db.String(300), unique=False, nullable=False)
    corporation_rolSII = db.Column(db.String(300), unique=False, nullable=True)
    corporation_taxType = db.Column(db.String(300), unique=False, nullable=True)

    corporation_client_id = db.Column(db.ForeignKey('clients.clients_id'))



    def __repr__(self):
        return '<Corporations %r>' % self.corporation_id, self.corporation_name, self.corporation_type, self.corporation_CBR, self.corporation_rolSII, self.corporation_taxType



@app.route('/')
def user():
    return "ROOT"

@app.route('/clientes/<string:rut>', methods = ['GET','POST', 'PUT', 'DELETE'])# SE MUESTRA EN EL BUSCADOR DEL CLIENTE
def clients(rut):
    if request.method == 'GET':
        queryEntry= datetime.datetime.now()
        list=[]
        if rut == "17.402.744-7" or rut == "20.968.696-1":
            resp = db.session.query(Clients).all() #DEPURAR ESTO, TOMAR RESP Y QUE EL MODEL ARROJE UN OBJ DE TODOS LOS CAMPOS
            for item in resp:
                list.append({
            "clients_id": item.clients_id,
            "clients_name": item.clients_name,
            "clients_rut": item.clients_rut,
            "clients_nationality": item.clients_nationality,
            "clients_civilStatus": item.clients_civilStatus,
            "clients_job": item.clients_job,
            "clients_address": item.clients_address,
            "clients_contact": item.clients_contact
        })
            print(f"{datetime.datetime.now() - queryEntry} CLIENTS TIME OF RESPONSE DELAY ---------------------------------------------------------------------------------------------->>>")
            return jsonify({"resp": list}),200
        else:
            resp = db.session.query(Clients).filter_by(clients_rut=rut).all()
            for item in resp:
                list.append({
            "clients_id": item.clients_id,
            "clients_name": item.clients_name,
            "clients_rut": item.clients_rut,
            "clients_nationality": item.clients_nationality,
            "clients_civilStatus": item.clients_civilStatus,
            "clients_job": item.clients_job,
            "clients_address": item.clients_address,
            "clients_contact": item.clients_contact
        })
            print(f"{datetime.datetime.now() - queryEntry} CLIENTS TIME OF RESPONSE DELAY ---------------------------------------------------------------------------------------------->>>")
            return jsonify({"resp": list}),200

    if request.method == 'POST':

        incomingData = request.get_json()
        existingClient = db.session.query(Clients).filter_by(clients_rut=incomingData['rut']).all()#CHECKING IF THE CLIENT ALREADY EXIST
        list = []
        for item in existingClient:
                list.append( item.clients_id)

        if len(list)==0:
            insertedData= Clients(clients_name=incomingData['name'], clients_rut=incomingData['rut'], clients_nationality=incomingData['nationality'], clients_civilStatus=incomingData['civilStatus'], clients_job=incomingData['job'], clients_address=incomingData['address'], clients_contact=incomingData['contact'] )
            db.session.add(insertedData)
            db.session.commit()
            lastId = insertedData.clients_id
            return jsonify({"resp": "inserted data", "lastId": str(lastId)}),200

        if len(list)>0:
            return jsonify({"resp": "client already exist", "lastId": list[0]})

    if request.method == 'PUT':
        incomingData = request.get_json()
        updateData= Clients.query.filter_by(clients_rut=rut)

        listOfNotEmptyStrings = []
        for item in incomingData:
            if incomingData[item] != "":
                listOfNotEmptyStrings.append(item)

        for item2 in listOfNotEmptyStrings:
            print(incomingData[item2], item2)
            updateData.update({item2: incomingData[item2]})
            db.session.commit()
        return "updated"

    if request.method == 'DELETE':
        deletedRow= Clients.query.filter_by(clients_rut=rut).first()
        db.session.delete(deletedRow)
        db.session.commit()
        return "data deleted",200


@app.route('/casos/<string:rut>', methods = ['GET','POST', 'PUT', 'DELETE'])# SE MUESTRA EN EL BUSCADOR DEL CLIENTE
def cases(rut):
    if request.method == 'GET':
        queryEntry= datetime.datetime.now()
        list=[]
        if rut == "17.402.744-7" or rut == "20.968.696-1":
            resp = db.session.query(Cases).filter_by(cases_activeCase=1).all()

            for item in resp:
                #getClientData = db.session.query(Clients).filter_by(clients_id=item.cases_client_id).first()
                list.append({
            "cases_id": item.cases_id,
            "cases_description": item.cases_description,
            "cases_rol_rit_ruc": item.cases_rol_rit_ruc,
            "cases_trial_entity": item.cases_trial_entity,
            "cases_legalIssue": item.cases_legalIssue,
            "cases_procedure": item.cases_procedure,
            "cases_objetive": item.cases_objetive,
            "cases_update": item.cases_update,
            "cases_pendingTask": item.cases_pendingTask,
            "cases_updateDate": item.cases_updateDate,
            "cases_activeCase": item.cases_activeCase,
            "cases_incomeDate": item.cases_incomeDate,
            "cases_deadLine": item.cases_deadLine,
            "cases_client_id": item.cases_client_id,
            "cases_lawyer_id": item.cases_lawyer_id,
            "clients_name": item.case_client.clients_name,
            "clients_rut": item.case_client.clients_rut,
            "clients_job": item.case_client.clients_job
        })
            print(f"{datetime.datetime.now() - queryEntry} CASES TIME OF RESPONSE DELAY ---------------------------------------------------------------------------------------------->>>")
            return jsonify({"resp": list}),200

        elif rut == "00.000.000-0":
            resp = db.session.query(Cases).filter_by(cases_activeCase=0).all() #DEPURAR ESTO, TOMAR RESP Y QUE EL MODEL ARROJE UN OBJ DE TODOS LOS CAMPOS

            for item in resp:
                list.append({
            "cases_id": item.cases_id,
            "cases_description": item.cases_description,
            "cases_rol_rit_ruc": item.cases_rol_rit_ruc,
            "cases_trial_entity": item.cases_trial_entity,
            "cases_legalIssue": item.cases_legalIssue,
            "cases_procedure": item.cases_procedure,
            "cases_objetive": item.cases_objetive,
            "cases_update": item.cases_update,
            "cases_pendingTask": item.cases_pendingTask,
            "cases_updateDate": item.cases_updateDate,
            "cases_activeCase": item.cases_activeCase,
            "cases_incomeDate": item.cases_incomeDate,
            "cases_deadLine": item.cases_deadLine,
            "cases_client_id": item.cases_client_id,
            "cases_lawyer_id": item.cases_lawyer_id,
             "clients_name": item.case_client.clients_name,
            "clients_rut": item.case_client.clients_rut,
            "clients_job": item.case_client.clients_job
        })
            print(f"{datetime.datetime.now() - queryEntry} CASES TIME OF RESPONSE DELAY ---------------------------------------------------------------------------------------------->>>")
            return jsonify({"resp": list}),200
        else:
            cases = Cases.query.filter(Cases.case_client.has(clients_rut=rut)).all()
            #resp = db.session.query(Clients).filter_by(clients_rut=rut).first()
            #client_id= resp.clients_id
            #cases = db.session.query(Cases).filter_by(cases_client_id=client_id).all()

            for item in cases:
                list.append({
            "cases_id": item.cases_id,
            "cases_description": item.cases_description,
            "cases_rol_rit_ruc": item.cases_rol_rit_ruc,
            "cases_trial_entity": item.cases_trial_entity,
            "cases_legalIssue": item.cases_legalIssue,
            "cases_procedure": item.cases_procedure,
            "cases_objetive": item.cases_objetive,
            "cases_update": item.cases_update,
            "cases_pendingTask": item.cases_pendingTask,
            "cases_updateDate": item.cases_updateDate,
            "cases_activeCase": item.cases_activeCase,
            "cases_incomeDate": item.cases_incomeDate,
            "cases_deadLine": item.cases_deadLine,
            "cases_client_id": item.cases_client_id,
            "cases_lawyer_id": item.cases_lawyer_id,
             "clients_name": item.case_client.clients_name,
            "clients_rut": item.case_client.clients_rut,
            "clients_job": item.case_client.clients_job
        })
            print(f"{datetime.datetime.now() - queryEntry} CASES TIME OF RESPONSE DELAY ---------------------------------------------------------------------------------------------->>>")
            return jsonify({"resp": list}),200

    if request.method == 'POST':
        incomingData = request.get_json(force=True)#force true is regardless if the mimetype of header is not application/json
        insertedData= Cases(cases_description=incomingData['cases_description'], cases_rol_rit_ruc=incomingData['cases_rol_rit_ruc'], cases_trial_entity=incomingData['cases_trial_entity'], cases_legalIssue=incomingData['cases_legalIssue'], cases_procedure=incomingData['cases_procedure'], cases_objetive=incomingData['cases_objetive'], cases_update=incomingData['cases_update'], cases_activeCase=incomingData['cases_activeCase'], cases_client_id=incomingData['cases_client_id'], cases_lawyer_id=incomingData['cases_lawyer_id'])
        db.session.add(insertedData)

        if incomingData['cases_rol_rit_ruc'] == "":
            lastId = db.session.query(Cases).order_by(Cases.cases_id.desc()).limit(1)
            for item in lastId:
                lastId = item.cases_id
            updateData= Cases.query.filter_by(cases_id=lastId)
            updateData.update({"cases_rol_rit_ruc": f"Transitorio N°{lastId}"})
        db.session.commit()
        return "data inserted",200

    if request.method == 'PUT':
        incomingData = request.get_json()
        updateData= Cases.query.filter_by(cases_rol_rit_ruc=incomingData["selected"])

        listOfNotEmptyStrings = []
        for item in incomingData:
            if incomingData[item] != "" and item != "selected":
                listOfNotEmptyStrings.append(item)

        for item2 in listOfNotEmptyStrings:

            if item2 == "cases_activeCase":
                updateData.update({item2: int(incomingData[item2])})
                db.session.commit()

                deathDay = str(datetime.datetime.now())
                index = deathDay.index(".")
                deathDay = deathDay[0:index]
                updateData  .update({"cases_deadLine":  str(deathDay) })
                db.session.commit()

                resp = db.session.query(Cases).filter_by(cases_rol_rit_ruc=incomingData["selected"]).all() #SELECTED IS THE CASE SELECTED FROM THE FRONEND
                list=[]
                for item in resp:
                    list.append(item.cases_id)# WE GET THE CASE ID
                storedId= list[0]

                docList = db.session.query(Documents).filter_by(documents_cases_id=storedId).all()#WE GET AL DOCUMENTS ASSOCIATED WITH THE CASE
                for item in docList:
                    if item.documents_type != "Sentencia" and item.documents_type != "Avenimiento" and item.documents_type != "Escritura Pública" and item.documents_type != "Escritura Privada" and item.documents_type != "Inscripción" and item.documents_type != "Publicación":
                        db.session.query(Documents).filter_by(documents_id=item.documents_id).delete()
                        os.remove(f'/home/guillermoPiedrabuena/pdf_store/document_id_{item.documents_id}.pdf')
                        db.session.commit()


            elif item2 == "cases_update":
                updateData.update({item2: incomingData[item2]})
                db.session.commit()

                today = str(datetime.datetime.now())
                index = today.index(".")
                today = today[0:index]
                updateData.update({"cases_updateDate": str(today)})
                db.session.commit()

            else:
                updateData.update({item2: incomingData[item2]})
                db.session.commit()

            return jsonify({"removed": "sii"}),200

    if request.method == 'DELETE':
        incomingData = request.get_json()
        deletedRow= Cases.query.filter_by(cases_rol_rit_ruc=incomingData["cases_rol_rit_ruc"]).first()
        db.session.delete(deletedRow)
        db.session.commit()
        return "data deleted",200

@app.route('/casosDisponibles', methods = ['GET','POST', 'PUT', 'DELETE'])
def avilableCases():
    if request.method == 'GET':
        list=[]
        resp = Cases.query.filter(Cases.cases_lawyer_id!=1).all()
        for item in resp:
            getClientData = db.session.query(Clients).filter_by(clients_id=item.cases_client_id).first()
            list.append({
            "cases_id": item.cases_id,
            "cases_description": item.cases_description,
            "cases_rol_rit_ruc": item.cases_rol_rit_ruc,
            "cases_trial_entity": item.cases_trial_entity,
            "cases_legalIssue": item.cases_legalIssue,
            "cases_procedure": item.cases_procedure,
            "cases_objetive": item.cases_objetive,
            "cases_update": item.cases_update,
            "cases_updateDate": item.cases_updateDate,
            "cases_activeCase": item.cases_activeCase,
            "cases_incomeDate": item.cases_incomeDate,
            "cases_deadLine": item.cases_deadLine,
            "cases_client_id": item.cases_client_id,
            "cases_lawyer_id": item.cases_lawyer_id,
            "clients_name":getClientData.clients_name,
            "clients_rut": getClientData.clients_rut
        })
        db.session.commit()


        return jsonify({"resp": list}),200

@app.route('/documentos/<string:cases_rol_rit_ruc>', methods = ['GET','POST', 'PUT', 'DELETE'])# SE MUESTRA EN EL BUSCADOR DEL CLIENTE
def documents(cases_rol_rit_ruc):
    queryEntry= datetime.datetime.now()
    if request.method == 'GET':
        list=[]
        if cases_rol_rit_ruc == "17.402.744-7" or cases_rol_rit_ruc == "20.968.696-1":
            resp = db.session.query(Documents).all() #DEPURAR ESTO, TOMAR RESP Y QUE EL MODEL ARROJE UN OBJ DE TODOS LOS CAMPOS
            for item in resp:
                list.append({
            "documents_type": item.documents_type,
            "documents_date": item.documents_date,
            "documents_cases_id": item.documents_cases_id
        })
            return jsonify({"resp": list}),200
        else:
            if "-" in cases_rol_rit_ruc or "°" in cases_rol_rit_ruc:
                resp = db.session.query(Cases).filter_by(cases_rol_rit_ruc=cases_rol_rit_ruc).first()
                cases_id= resp.cases_id
                documents = db.session.query(Documents).filter_by(documents_cases_id=cases_id).all()
                for item in documents:
                    list.append({"documents_type": item.documents_type,"documents_date": item.documents_date, "documents_id": item.documents_id})

            if "-" not in cases_rol_rit_ruc and "°" not in cases_rol_rit_ruc:
                documents = db.session.query(Documents).filter_by(documents_cases_id=cases_rol_rit_ruc).all()
                for item in documents:
                    list.append({"documents_type": item.documents_type,"documents_date": item.documents_date, "documents_id": item.documents_id})

            return jsonify({"resp": list})


    if request.method == 'POST':
        incomingDataJSON = request.get_json()
        insertedData= Documents(documents_type=str(incomingDataJSON['documents_type']), documents_cases_id=incomingDataJSON['documents_cases_id'] )
        db.session.add(insertedData)

        lastId = db.session.query(Documents).order_by(Documents.documents_id.desc()).limit(1)
        list=[]
        for item in lastId:
            print(item.documents_id)
            list.append(item.documents_id)

        db.session.commit()

        print(f"{datetime.datetime.now() - queryEntry} CASES TIME OF RESPONSE DELAY ---------------------------------------------------------------------------------------------->>>")

        return jsonify({"resp": list[0]}),200 #DEVUELVE EL ULTIMO ID

    if request.method == 'PUT':
        incomingData = request.get_json()
        updateData= Cases.query.filter_by(cases_rol_rit_ruc=incomingData["cases_rol_rit_ruc"])

        listOfNotEmptyStrings = []
        for item in incomingData:
            if incomingData[item] != "":
                listOfNotEmptyStrings.append(item)

        for item2 in listOfNotEmptyStrings:
            print(incomingData[item2], item2)
            updateData.update({item2: incomingData[item2]})
            db.session.commit()
            return "updated"


    if request.method == 'DELETE':
        incomingData = request.get_json()
        deletedRow= Cases.query.filter_by(cases_rol_rit_ruc=incomingData["cases_rol_rit_ruc"]).first()
        db.session.delete(deletedRow)
        db.session.commit()
        return "data deleted",200

@app.route('/documentos/download/<string:id>', methods = ['GET'])# SE MUESTRA EN EL BUSCADOR DEL CLIENTE
def documentsDownload(id):
    if request.method == 'GET':
        return send_file(f'../pdf_store/document_id_{id}.pdf', attachment_filename=f'document_id_{id}.pdf')

@app.route('/documentos/upload/<int:id>', methods = ['POST'])# SE MUESTRA EN EL BUSCADOR DEL CLIENTE
def documentsUpload(id):
        queryEntry= datetime.datetime.now()
        profile = request.files['pdf']
        uploads_dir = os.path.join('./', 'pdf_store')
        print(uploads_dir)
        profile.save(os.path.join(uploads_dir, secure_filename(f"[document_id {id}].pdf")))

        print(f"{datetime.datetime.now() - queryEntry} CASES TIME OF RESPONSE DELAY ---------------------------------------------------------------------------------------------->>>")

        return "pdf saved in folder", 200

@app.route('/lawyers/<string:rut>', methods = ['GET', 'POST', 'PUT', 'DELETE'])
def lawyers(rut):

    if request.method == 'GET':
        list=[]
        if rut == "17.402.744-7" or rut == "20.968.696-1":
            resp = db.session.query(Lawyers).all() #DEPURAR ESTO, TOMAR RESP Y QUE EL MODEL ARROJE UN OBJ DE TODOS LOS CAMPOS
            for item in resp:
                list.append({
                "lawyers_id": item.lawyers_id,
                "lawyers_name": item.lawyers_name,
                "lawyers_field": item.lawyers_field,
                "lawyers_rut": item.lawyers_rut,
                "lawyers_password": item.lawyers_password
            })
            return jsonify({"resp": list}),200
        else:

            resp = db.session.query(Clients).filter_by(clients_rut=rut).all()
            for item in resp:
                    list.append({
                "lawyers_id": item.lawyers_id,
                "lawyers_name": item.lawyers_name,
                "lawyers_field": item.lawyers_field,
                "lawyers_rut": item.lawyers_rut,
                "lawyers_password": item.lawyers_passwordt
            })
            return jsonify({"resp": list}),200

    if request.method == 'POST':
        incomingData = request.get_json()
        insertedData= Lawyers(lawyers_name=incomingData['name'], lawyers_field=incomingData['field'], lawyers_rut=incomingData['rut'], lawyers_password=incomingData['password'])
        db.session.add(insertedData)
        db.session.commit()
        lastId = insertedData.clients_id
        return jsonify({"resp": "inserted data", "lastId": str(lastId)}),200

    if request.method == 'PUT':
        incomingData = request.get_json()
        updateData= Lawyers.query.filter_by(lawyers_rut=rut)

        listOfNotEmptyStrings = []
        for item in incomingData:
            if incomingData[item] != "":
                listOfNotEmptyStrings.append(item)

        for item2 in listOfNotEmptyStrings:
            print(incomingData[item2], item2)
            updateData.update({item2: incomingData[item2]})
            db.session.commit()
        return "updated"

    if request.method == 'DELETE':
        deletedRow= Lawyers.query.filter_by(lawyers_rut=rut).first()
        db.session.delete(deletedRow)
        db.session.commit()
        return "data deleted",200
