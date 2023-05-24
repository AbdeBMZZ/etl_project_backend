from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CSVFile, TransformationRule, TransformedData, session, engine
from .serializers import CSVFileSerializer, TransformationRuleSerializer, TransformedDataSerializer
import pandas as pd
from rest_framework import status
from django.http import HttpResponse, JsonResponse
from django.conf import settings

import os

local_session = session(bind=engine)

@api_view(['GET', 'POST'])
def csv_file_list(request):
    if request.method == 'GET':
        data = []
        csv_files = local_session.query(CSVFile).all()
        for csv_file in csv_files:
            data.append({
                'id': csv_file.id,
                'file_path': csv_file.file_path,
                'upload_date': csv_file.upload_date
            })
        return Response(data)

    elif request.method == 'POST':

        file = request.FILES['file_path']  

        file_directory = 'csv_files'

        file_path = os.path.join(file_directory, file.name)

        os.makedirs(file_directory, exist_ok=True)


        with open(file_path, 'wb') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        df = pd.read_csv(file_path)

        csv_file = CSVFile(file_path=file_path)

        local_session.add(csv_file)
        local_session.commit()

        df = df.fillna('---')

        
        return Response({
            'headers': df.columns.tolist(),
            'rows': df.values.tolist(),
            'csv_file_ID': csv_file.id
        }, status=status.HTTP_201_CREATED)


@api_view(['GET', 'DELETE'])
def csv_file_detail(request, pk):
    try:
        csv_file = local_session.query(CSVFile).filter_by(id=pk).first()
    except CSVFile.DoesNotExist:
        return Response({'error': 'CSVFile does not exist'}, status=404)

    if request.method == 'GET':
        data = {
            'id': csv_file.id,
            'file_path': csv_file.file_path,
            'upload_date': csv_file.upload_date
        }
        return Response(data)


    elif request.method == 'DELETE':
        local_session.delete(csv_file)
        return Response({'message': 'CSVFile was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def transformation_rule_list(request):
    if request.method == 'GET':
        data = []
        transofrmation_rules = local_session.query(TransformationRule).all()

        for transformation_rule in transofrmation_rules:
            data.append({
                'id': transformation_rule.id,
                'name': transformation_rule.name,
                'operation': transformation_rule.operation,
                'column': transformation_rule.column,
                'operator': transformation_rule.operator,
                'value': transformation_rule.value
            })

        return Response(data)

    elif request.method == 'POST':
        transformation_rule = TransformationRule(
            name=request.data['name'],
            operation=request.data['operation'],
            column=request.data['column'],
            operator=request.data['operator'],
            value=request.data['value']
        )
        local_session.add(transformation_rule)
        local_session.commit()

        return Response({'message': 'TransformationRule was created successfully!'}, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def transformation_rule_detail(request, pk):
    try:
        transformation_rule = local_session.query(TransformationRule).filter_by(id=pk).first()
    except TransformationRule.DoesNotExist:
        return Response({'error': 'TransformationRule does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        data = {
            'id': transformation_rule.id,
            'name': transformation_rule.name,
            'operation': transformation_rule.operation,
            'column': transformation_rule.column,
            'operator': transformation_rule.operator,
            'value': transformation_rule.value
        }
        return Response(data)
    elif request.method == 'PUT':
        local_session.query(TransformationRule).filter_by(id=pk).update({
            'name': request.data['name'],
            'operation': request.data['operation'],
            'column': request.data['column'],
            'operator': request.data['operator'],
            'value': request.data['value']
        })

        return Response(serializer.errors)
    elif request.method == 'DELETE':
        local_session.delete(transformation_rule)
        return Response({'message': 'TransformationRule was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def transformed_data_list(request):
    if request.method == 'GET':
        data = []
        transformed_data = local_session.query(TransformedData).all()
        for td in transformed_data:
            data.append({
                'id': td.id,
                'csv_file_id': td.csv_file_id,
                'rule_id': td.rule_id,
                'rule name': td.rule.name,
                'rule operation': td.rule.operation,
            })

        return Response(data)

    elif request.method == 'POST':
        try:
            csv_file = local_session.query(CSVFile).filter_by(id=request.data['csv_file_id']).first()
            rule = local_session.query(TransformationRule).filter_by(id=request.data['rule_id']).first()

            df = pd.read_csv(csv_file.file_path)

            column_name = rule.column.lower()
            column_index = df.columns.str.lower().tolist().index(column_name)

            value = pd.to_numeric(df.iloc[:, column_index], errors='coerce')

            operator = rule.operator
            transformed_values = eval('value ' + operator + ' ' + str(rule.value))

            df.iloc[:, column_index] = transformed_values

            headers = df.columns.tolist()
            rows = df.values.tolist()

            file_directory = 'transformed_files'

            file_path = os.path.join(file_directory, csv_file.file_path.split('/')[-1])

            os.makedirs(file_directory, exist_ok=True)

            df.to_csv(file_path, index=False)

            csv_transformed = CSVFile(file_path=file_path)

            transformed_data = TransformedData(csv_file=csv_file, rule=rule)

            local_session.add(csv_transformed)
            local_session.add(transformed_data)
            local_session.commit()


            df = df.fillna('---')

            return Response({
                'headers': df.columns.tolist(),
                'rows': df.values.tolist(),
                'transformed_file_ID': csv_transformed.id
            }, status=status.HTTP_201_CREATED)
        except:
            return Response({'error': 'TransformedData does not exist'}, status=status.HTTP_404_NOT_FOUND)
