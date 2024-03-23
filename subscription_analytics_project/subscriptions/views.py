from datetime import datetime
from django.utils import timezone
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
import pandas as pd
from collections import OrderedDict

# Constants
SUPPORTED_FORMATS = ('.xlsx', '.xls', '.csv')
MONTHS_IN_ORDER = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

def get_start_date(row):
    date_str = row['data início']
    if isinstance(date_str, datetime):
        return timezone.make_aware(date_str)
    return timezone.make_aware(datetime.strptime(date_str, "%m/%d/%y %H:%M"))

def process_file_data(data):
    monthly_metrics = OrderedDict((month, {
        "mrr": 0,
        "total_ativa": 0,
        "total_canceled": 0,
        "total_trial_cancelado": 0,
        "total_atrasada": 0,
        "total_rows": 0,
        "processed_rows": 0,
        "churn_rate": 0
    }) for month in MONTHS_IN_ORDER)

    for index, row in data.iterrows():
        transaction_value = row['valor']
        subscription_status = row['status']
        start_date = get_start_date(row)
        month_name = start_date.strftime('%B')

        monthly_metrics[month_name]['mrr'] += transaction_value
        monthly_metrics[month_name]['total_rows'] += 1
        monthly_metrics[month_name]['processed_rows'] += 1

        if subscription_status == 'Ativa':
            monthly_metrics[month_name]['total_ativa'] += 1
        elif subscription_status == 'Cancelada':
            monthly_metrics[month_name]['total_canceled'] += 1
        elif subscription_status == 'Trial cancelado':
            monthly_metrics[month_name]['total_trial_cancelado'] += 1
        elif subscription_status == 'Atrasada':
            monthly_metrics[month_name]['total_atrasada'] += 1

        monthly_metrics[month_name]['churn_rate'] = (monthly_metrics[month_name]['total_canceled'] /
                                                     monthly_metrics[month_name]['total_rows']) * 100 if \
            monthly_metrics[month_name]['total_rows'] > 0 else 0

    return monthly_metrics

class FileUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        uploaded_file = request.FILES.get('file')
        if not uploaded_file:
            return Response({"error": "Arquivo não enviado."}, status=400)

        if not uploaded_file.name.endswith(SUPPORTED_FORMATS):
            return Response({"error": "Formato do arquivo não suportado. Envie um arquivo .xlsx ou .csv."}, status=400)

        try:
            if uploaded_file.name.endswith(('.xlsx', '.xls')):
                data = pd.read_excel(uploaded_file)
            else:
                data = pd.read_csv(uploaded_file)

            monthly_metrics = process_file_data(data)

            # Calculating totals
            total_mrr = sum(monthly_metrics[month]['mrr'] for month in monthly_metrics)
            total_ativa = sum(monthly_metrics[month]['total_ativa'] for month in monthly_metrics)
            total_canceled = sum(monthly_metrics[month]['total_canceled'] for month in monthly_metrics)
            total_trial_cancelado = sum(monthly_metrics[month]['total_trial_cancelado'] for month in monthly_metrics)
            total_atrasada = sum(monthly_metrics[month]['total_atrasada'] for month in monthly_metrics)
            total_rows = sum(monthly_metrics[month]['total_rows'] for month in monthly_metrics)
            processed_rows = sum(monthly_metrics[month]['processed_rows'] for month in monthly_metrics)

            # Calculate total churn rate
            churn_rate = (total_canceled / total_rows) * 100 if total_rows > 0 else 0

            # Return monthly metrics and totals
            return Response({
                "monthly_metrics": monthly_metrics,
                "total_mrr": total_mrr,
                "total_ativa": total_ativa,
                "total_canceled": total_canceled,
                "total_trial_cancelado": total_trial_cancelado,
                "total_atrasada": total_atrasada,
                "total_rows": total_rows,
                "processed_rows": processed_rows,
                "churn_rate": churn_rate
            })

        except pd.errors.ParserError as e:
            return Response({"error": "Erro ao processar o arquivo. Verifique o formato do arquivo enviado."}, status=400)
        except Exception as e:
            return Response({"error": str(e)}, status=400)
