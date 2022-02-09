
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from patient.models import Patient
from patient.serializers import PatientSerializer, VisitSerializer

from django.db import IntegrityError, transaction

class PatientView(APIView):
    """PatientView class

    This view performs POST and FETCHALL operations for Patient

    Parameters
    ----------
    APIView : rest_framework.views

    """

    def get(self, request):
        
        try:
            patients = Patient.objects.all()
            serializer = PatientSerializer(patients,many=True)
            return Response(
               serializer.data, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
               data=None,status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
           
            
    def post(self, request):
            
        try:
            #using atomic transaction to make sure partial records are not saved in DB
            with transaction.atomic():
                
                #read records from uploaded file
                record=self.get_file_content(request)
                
                #loop through all records
                for data in record:
                    
                    #split each record into 3 different values
                    splitted_record=data.split(',')
                    
                    #check if all 5 mandatory values are provided
                    if len(splitted_record)==5:
                        
                        #update visit records of previous patient if exists
                        if self.update_existing_patient(splitted_record):
                            continue
                        
                        #create new patient record along with its visits
                        self.create_new_patient(splitted_record)
                
                return Response(data=None,status=status.HTTP_200_OK)
           
        except IntegrityError as e:
            return Response(
               data=None,status=status.HTTP_400_BAD_REQUEST
            )  
        except Exception as e:
            return Response(
               data=None,status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )        

    
    def create_new_patient(self,splitted_record):
         patient_data={'first_name':splitted_record[0],'last_name':splitted_record[1],'dob':splitted_record[2]}
         patient_serializer=PatientSerializer(data=patient_data)
         if patient_serializer.is_valid():
            patient_serializer.save()
            patient_id=patient_serializer.data['id']
            visit_data={'patient':patient_id,'reason':splitted_record[4],'visit_date':splitted_record[3]}
            visit_serializer=VisitSerializer(data=visit_data)
            if visit_serializer.is_valid():
                visit_serializer.save()
            else:
                raise IntegrityError(visit_serializer.errors)   
                            
         else:
            raise IntegrityError(patient_serializer.errors)
                        
                    
    def update_existing_patient(self,splitted_record):
        existing_patient_data=Patient.objects.filter(first_name=splitted_record[0],last_name=splitted_record[1])
        patient_id=None
        if existing_patient_data.count()==1:
            patient_id=existing_patient_data.first().id
            visit_data={'patient':patient_id,'reason':splitted_record[4],'visit_date':splitted_record[3]}
            visit_serializer=VisitSerializer(data=visit_data)
            if visit_serializer.is_valid():
                visit_serializer.save()
                return True
            else:
                raise IntegrityError(visit_serializer.errors) 
        return False 
            
    def get_file_content(self,request):
         myfile = request.data['File']
         file = myfile.read().decode('utf-8')
         record = [line for line in file.split('\r\n')]
         record = record[1:]
         return record
                                                                                                                                        