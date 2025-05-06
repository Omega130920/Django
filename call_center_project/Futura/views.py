## This app belongs to Luanovaneck ##
## This app is a part of the call_center_project ##
from django.shortcuts import render, redirect, get_object_or_404
from .models import TraceResult, ClientList, Call, ClientPayment
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime
from django.db.models import Q
from django.db import connection
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from django.core.files.base import ContentFile
from django.http import HttpResponse
import os
from django.urls import reverse
from django.db import transaction
from decimal import Decimal
from datetime import datetime
from django.db.models import Prefetch
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import base64
import io
from django.conf import settings
from django.core.mail import EmailMessage, send_mail
from django.contrib.auth.models import User
from django.contrib import messages
from django.template.loader import render_to_string
import json
from django.contrib.auth.views import PasswordResetConfirmView
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count, Sum
from django.contrib.auth.models import User

def home(request):
    print("Home view called!")
    return render(request, 'Futura/home.html')

def trace_results(request):
    print("trace_results view called!")
    results = TraceResult.objects.all()
    return render(request, 'Futura/trace_results.html', {'results': results})
    class Meta:
        managed = False
        db_table = 'Trace_result'
@login_required
def agent_overview(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')

    username = request.user.username
    return render(request, 'Futura/agent_overview.html', {'username': username})


@login_required
def client_details(request):
    client_details_data = []
    arrangements = []
    calls = []
    debt_records = []  # To store individual debt records
    specific_debt_record = None # To store a specific debt record if requested

    if request.method == 'GET':
        id_number = request.GET.get('id_number')
        debt_no = request.GET.get('debt_no') # Get the specific debt number if provided

        if id_number:
            try:
                clients = ClientList.objects.filter(ID_Number=id_number)
                if clients.exists():
                    client = clients.first()

                    trace_results = TraceResult.objects.filter(ID_Number=client.ID_Number)
                    all_contact_numbers = []
                    for result in trace_results:
                        contact_fields = [
                            result.cell_number, result.Home1, result.Work1, result.Cell1,
                            result.Home2, result.Work2, result.Cell2, result.Home3,
                            result.Work3, result.Cell3, result.Home4, result.Work4,
                            result.Cell4, result.Home5, result.Work5, result.Cell5,
                            result.Home6, result.Work6, result.Cell6, result.Home7,
                            result.Work7, result.Cell7, result.Home8, result.Work8,
                            result.Cell8, result.Home9, result.Work9, result.Cell9,
                            result.Home10, result.Work10, result.Cell10, result.Home11,
                            result.Work11, result.Cell11, result.Home12, result.Work12,
                            result.Cell12, result.Home13, result.Work13, result.Cell13,
                            result.Home14, result.Work14, result.Cell14, result.Home15,
                            result.Work15, result.Cell15,
                            result.D_O_1, result.D_O_2, result.D_O_3, result.D_O_4, result.D_O_5,
                            result.D_O_6, result.D_O_7, result.D_O_8, result.D_O_9, result.D_O_10,
                            result.D_O_11, result.D_O_12, result.D_O_13, result.D_O_14, result.D_O_15,
                        ]
                        all_contact_numbers.extend([num for num in contact_fields if num and num != "NULL" and isinstance(num, str)])
                    contact_details = ", ".join(all_contact_numbers)
                    arr_exists = Call.objects.filter(id_number=id_number, call_result='ARR').exists()

                    try:
                        payment = ClientPayment.objects.filter(id_number=id_number).latest('created_at')
                        last_payment_date = payment.date_of_statement
                        last_payment_amount = payment.amount_deposited
                    except ClientPayment.DoesNotExist:
                        last_payment_date = None
                        last_payment_amount = None

                    # Fetch all debt records for this ID Number
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "SELECT `[No.]`, `TOTAL` FROM debt_collection_6 WHERE `ID NUMBER OF DEBTOR` = %s",
                            [id_number])
                        all_client_debt_records = cursor.fetchall()
                        for record in all_client_debt_records:
                            debt_records.append({'debt_no': record[0], 'total': record[1]})

                    # Calculate total debt by summing the individual records
                    total_debt = sum(record['total'] for record in debt_records if isinstance(record['total'], (int, float)))

                    client_info = {
                        'client': client,
                        'contact_details': contact_details,
                        'total_debt': total_debt,  # Use the calculated total
                        'arr_exists': arr_exists,
                        'last_payment_date': last_payment_date,
                        'last_payment_amount': last_payment_amount,
                        'debt_records': debt_records, # Pass the list of debt records
                    }

                    try:
                        call = Call.objects.filter(id_number=id_number).latest('start_time')
                        client_info['number_of_months'] = call.number_of_months
                        client_info['installments'] = call.installments
                        client_info['start_month'] = call.start_month
                        client_info['day_of_month'] = call.day_of_month
                    except Call.DoesNotExist:
                        client_info['number_of_months'] = "N/A"
                        client_info['installments'] = "N/A"
                        client_info['start_month'] = "N/A"
                        client_info['day_of_month'] = "N/A"

                    client_details_data.append(client_info)

                    # Fetch arrangements and calls
                    arrangements = Call.objects.filter(id_number=id_number, call_result='ARR')
                    calls = Call.objects.filter(id_number=id_number)
                    for arr in arrangements:
                        arr.first_name = client.FIRST_NAME
                        arr.surname = client.SURNAME

                    # If a specific debt_no is requested, find that record
                    if debt_no:
                        specific_debt_record = next((dr for dr in debt_records if str(dr['debt_no']) == debt_no), None)

                    context = {
                        'client_details_data': client_details_data,
                        'arrangements': arrangements,
                        'calls': calls,
                        'debt_records': debt_records,
                        'specific_debt_record': specific_debt_record, # Pass the specific debt record
                    }
                    return render(request, 'Futura/client_details.html', context)
                else:
                    # Handle the case where no client with the ID is found
                    return render(request, 'Futura/client_details.html', {'client_details_data': [], 'arrangements': [], 'calls': [], 'debt_records': [], 'error': 'Client not found'})

            except TraceResult.DoesNotExist:
                clients = ClientList.objects.filter(ID_Number=id_number)
                client = clients.first() if clients.exists() else None
                client_details_data = [{'client': client, 'contact_details': "N/A",
                                            'total_debt': "N/A",
                                            'arr_exists': False, 'last_payment_date': None,
                                            'last_payment_amount': None, 'debt_records': []}] if client else []
                arrangements = []
                calls = []
                debt_records = []
                context = {
                    'client_details_data': client_details_data,
                    'arrangements': arrangements,
                    'calls': calls,
                    'debt_records': debt_records,
                    'specific_debt_record': None,
                }
                return render(request, 'Futura/client_details.html', context)

        else:  # When id_number is NOT provided
            clients = ClientList.objects.all()
            client_details_data = []
            arrangements = []
            calls = []
            all_debt_records = {} # Dictionary to store debt records per client
            for client in clients:
                trace_results = TraceResult.objects.filter(ID_Number=client.ID_Number)
                all_contact_numbers = [...] # Your contact fields here
                all_contact_numbers.extend([num for num in contact_fields if num and num != "NULL" and isinstance(num, str)])
                contact_details = ", ".join(all_contact_numbers)

                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT `[No.]`, `TOTAL` FROM debt_collection_6 WHERE `ID NUMBER OF DEBTOR` = %s",
                        [client.ID_Number])
                    all_client_debt_records = cursor.fetchall()
                    client_debt_records = []
                    for record in all_client_debt_records:
                        client_debt_records.append({'debt_no': record[0], 'total': record[1]})
                    total_debt = sum(record['total'] for record in client_debt_records if isinstance(record['total'], (int, float)))
                    all_debt_records[client.ID_Number] = client_debt_records

                try:
                    payment = ClientPayment.objects.filter(id_number=client.ID_Number).latest('created_at')
                    last_payment_date = payment.date_of_statement
                    last_payment_amount = payment.amount_deposited
                except ClientPayment.DoesNotExist:
                    last_payment_date = None
                    last_payment_amount = None

                client_info = {
                    'client': client,
                    'contact_details': contact_details,
                    'total_debt': total_debt,
                    'arr_exists': Call.objects.filter(id_number=client.ID_Number, call_result='ARR').exists(),
                    'last_payment_date': last_payment_date,
                    'last_payment_amount': last_payment_amount,
                    'debt_records': all_debt_records.get(client.ID_Number, []),
                }
                try:
                    call = Call.objects.filter(id_number=client.ID_Number).latest('start_time')
                    client_info['number_of_months'] = call.number_of_months
                    client_info['installments'] = call.installments
                    client_info['start_month'] = call.start_month
                    client_info['day_of_month'] = call.day_of_month
                except Call.DoesNotExist:
                    client_info['number_of_months'] = "N/A"
                    client_info['installments'] = "N/A"
                    client_info['start_month'] = "N/A"
                    client_info['day_of_month'] = "N/A"

                client_details_data.append(client_info)

            context = {
                'client_details_data': client_details_data,
                'arrangements': arrangements,
                'calls': calls,
                'debt_records': debt_records, # This will be empty when showing all clients, individual client debts are in client_details_data
                'specific_debt_record': None,
            }
            return render(request, 'Futura/client_details.html', context)

    else:
        context = {
            'client_details_data': client_details_data,
            'arrangements': arrangements,
            'calls': calls,
            'debt_records': debt_records,
            'specific_debt_record': None,
        }
        return render(request, 'Futura/client_details.html', context)


@login_required
def client_list(request):
    clients = ClientList.objects.all()
    client_data = []

    search_id = request.GET.get('search_id', '').strip()

    print(f"Received search_id: '{search_id}'")

    if search_id:
        clients = clients.filter(ID_Number__icontains=search_id)

    print(f"Number of clients after filtering: {clients.count()}")

    for client in clients:
        if search_id:
            trace_results = TraceResult.objects.filter(ID_Number=search_id)
        else:
            trace_results = TraceResult.objects.filter(ID_Number=client.ID_Number)

        print(f"Number of trace_results for {client.ID_Number}: {trace_results.count()}")

        phone_numbers = []
        called_numbers = []

        for result in trace_results:
            contact_fields = [
                result.cell_number, result.Home1, result.Work1, result.Cell1,
                result.Home2, result.Work2, result.Cell2, result.Home3,
                result.Work3, result.Cell3, result.Home4, result.Work4,
                result.Cell4, result.Home5, result.Work5, result.Cell5,
                result.Home6, result.Work6, result.Cell6, result.Home7,
                result.Work7, result.Cell7, result.Home8, result.Work8,
                result.Cell8, result.Home9, result.Work9, result.Cell9,
                result.Home10, result.Work10, result.Cell10, result.Home11,
                result.Work11, result.Cell11, result.Home12, result.Work12,
                result.Cell12, result.Home13, result.Work13, result.Cell13,
                result.Home14, result.Work14, result.Cell14, result.Home15,
                result.Work15, result.Cell15,
                result.D_O_1, result.D_O_2, result.D_O_3, result.D_O_4, result.D_O_5,
                result.D_O_6, result.D_O_7, result.D_O_8, result.D_O_9, result.D_O_10,
                result.D_O_11, result.D_O_12, result.D_O_13, result.D_O_14, result.D_O_15,
            ]
            phone_numbers.extend([num for num in contact_fields if num and num != "NULL" and num])

        for number in phone_numbers:
            if search_id:
                calls = Call.objects.filter(id_number=search_id, phone_number=number)
            else:
                calls = Call.objects.filter(id_number=client.ID_Number, phone_number=number)

            print(f"Number of calls for {client.ID_Number} and {number}: {calls.count()}")

            if calls.exists():
                called_numbers.append(number)

        client_data.append({
            'client': client,
            'total_numbers': len(phone_numbers),
            'called_count': len(called_numbers),
            'outstanding_numbers': len(phone_numbers) - len(called_numbers),
        })

    return render(request, 'Futura/client_list.html', {'client_data': client_data})

def arrangements(request):
    arr_calls = Call.objects.filter(call_result='ARR')  # Only ARR calls
    arrangements_data = []

    for call in arr_calls:
        try:
            client = ClientList.objects.get(ID_Number=call.id_number)
            arrangements_data.append({
                'id_number': call.id_number,
                'first_name': client.FIRST_NAME,
                'surname': client.SURNAME,
                'phone_number': call.phone_number,
                'call_result': call.call_result,
                'notes': call.notes,
            })
        except ClientList.DoesNotExist:
            arrangements_data.append({
                'id_number': call.id_number,
                'first_name': 'Client Not Found',
                'surname': 'Client Not Found',
                'phone_number': call.phone_number,
                'call_result': call.call_result,
                'notes': call.notes,
            })

    return render(request, 'Futura/arrangements.html', {'arrangements': arrangements_data})

@login_required
def client_information(request):
    records_per_page = 36
    page = request.GET.get('page')
    search_id = request.GET.get('search_id')
    search_first_name = request.GET.get('search_first_name')
    search_surname = request.GET.get('search_surname')

    with connection.cursor() as cursor:
        cursor.execute("SELECT `[No.]`, `ID NUMBER OF DEBTOR`, TOTAL FROM debt_collection_6")
        all_debt_records = cursor.fetchall()

        debtor_ids = [record[1] for record in all_debt_records]

        # Fetch all relevant clients in one go
        clients = ClientList.objects.filter(ID_Number__in=debtor_ids)
        client_dict = {client.ID_Number: client for client in clients}

        filtered_debt_records = []
        for record in all_debt_records:
            debt_no, id_number, total = record
            client = client_dict.get(id_number)
            if client:
                include = True
                if search_id and search_id.lower() not in str(client.ID_Number).lower():
                    include = False
                if search_first_name and search_first_name.lower() not in str(client.FIRST_NAME).lower():
                    include = False
                if search_surname and search_surname.lower() not in str(client.SURNAME).lower():
                    include = False
                if include:
                    filtered_debt_records.append({
                        'debt_no': debt_no,
                        'id_number': id_number,
                        'total_debt': total,
                        'client': client,
                    })

        paginator = Paginator(filtered_debt_records, records_per_page)

        try:
            debt_records_page = paginator.page(page)
        except PageNotAnInteger:
            debt_records_page = paginator.page(1)
        except EmptyPage:
            debt_records_page = paginator.page(paginator.num_pages)

        context = {
            'debt_records_page': debt_records_page,
        }
        return render(request, 'Futura/client_information.html', context)

@login_required
def create_call(request):
    if request.method == 'POST':
        try:
            agent = request.user.username
            id_number = request.POST.get('id_number')
            phone_number = request.POST.get('phone_number')
            start_time_str = request.POST.get('start_time')
            end_time_str = request.POST.get('end_time')
            direction = request.POST.get('direction')
            outcome = request.POST.get('outcome')
            call_result = request.POST.get('call_result')
            notes = request.POST.get('notes')
            recipient_email = request.POST.get('recipient_email')
            number_of_months = int(request.POST.get('number_of_months'))
            installments = request.POST.get('installments')
            start_month = int(request.POST.get('start_month'))
            day_of_month = int(request.POST.get('day_of_month'))

            start_time = datetime.fromisoformat(start_time_str)
            end_time = datetime.fromisoformat(end_time_str)

            client = ClientList.objects.get(ID_Number=id_number)
            subject = request.POST.get('subject', f"Call Result for {client.FIRST_NAME} {client.SURNAME}")
            body = request.POST.get('body', f"Call Result: {call_result}\nNotes: {notes}")
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [recipient_email]

            attachment_name = None
            if 'attachment' in request.FILES:
                attachment = request.FILES['attachment']
                email = EmailMessage(subject, body, from_email, recipient_list)
                email.attach(attachment.name, attachment.read(), attachment.content_type)
                email.send()
                attachment_name = attachment.name
            else:
                send_mail(subject, body, from_email, recipient_list, fail_silently=False)
                attachment_name = None

            call_record = Call(
                agent=agent,
                id_number=id_number,
                phone_number=phone_number,
                start_time=start_time,
                end_time=end_time,
                direction=direction,
                outcome=outcome,
                call_result=call_result,
                notes=notes,
                recipient_email=recipient_email,
                attachment_name=attachment_name,
                number_of_months=number_of_months,
                installments=installments,
                start_month=start_month,
                day_of_month=day_of_month,
            )
            print(request.POST)
            print(call_record.__dict__)
            call_record.save()

            return redirect('agent_overview')  # Redirect for non-AJAX

        except Exception as e:
            print(f"Error sending email or saving call: {e}")
            return HttpResponse(f"Error: {e}", status=500) # Return a standard error response

    return render(request, 'Futura/create_call.html')

def get_client_details(request):
    id_number = request.GET.get('id_number')
    try:
        client = ClientList.objects.get(ID_Number=id_number)
        return JsonResponse({'first_name': client.FIRST_NAME, 'surname': client.SURNAME})
    except ClientList.DoesNotExist:
        return JsonResponse({'first_name': '', 'surname': ''})
    except TraceResult.DoesNotExist:
        return [{'client': client, 'contact_details': "N/A", 'last_cred': "N/A", 'total_debt': "N/A", 'arr_exists': False}]
    
def get_phone_numbers(request):
    id_number = request.GET.get('id_number')
    try:
        trace_results = TraceResult.objects.filter(ID_Number=id_number)
        phone_numbers = []
        for result in trace_results:
            contact_fields = [
                result.cell_number, result.Home1, result.Work1, result.Cell1,
                result.Home2, result.Work2, result.Cell2, result.Home3,
                result.Work3, result.Cell3, result.Home4, result.Work4,
                result.Cell4, result.Home5, result.Work5, result.Cell5,
                result.Home6, result.Work6, result.Cell6, result.Home7,
                result.Work7, result.Cell7, result.Home8, result.Work8,
                result.Cell8, result.Home9, result.Work9, result.Cell9,
                result.Home10, result.Work10, result.Cell10, result.Home11,
                result.Work11, result.Cell11, result.Home12, result.Work12,
                result.Cell12, result.Home13, result.Work13, result.Cell13,
                result.Home14, result.Work14, result.Cell14, result.Home15,
                result.Work15, result.Cell15,
                result.D_O_1, result.D_O_2, result.D_O_3, result.D_O_4, result.D_O_5,
                result.D_O_6, result.D_O_7, result.D_O_8, result.D_O_9, result.D_O_10,
                result.D_O_11, result.D_O_12, result.D_O_13, result.D_O_14, result.D_O_15,
            ]
            phone_numbers.extend([num for num in contact_fields if num and num != "NULL"])
        return JsonResponse({'phone_numbers': phone_numbers})
    except TraceResult.DoesNotExist:
        return JsonResponse({'phone_numbers': []})
    
def extract_phone_numbers(trace_results):
    phone_numbers = set()
    for result in trace_results:
        contact_fields = [
            result.cell_number, result.Home1, result.Work1, result.Cell1,
            result.Home2, result.Work2, result.Cell2, result.Home3,
            result.Work3, result.Cell3, result.Home4, result.Work4,
            result.Cell4, result.Home5, result.Work5, result.Cell5,
            result.Home6, result.Work6, result.Cell6, result.Home7,
            result.Work7, result.Cell7, result.Home8, result.Work8,
            result.Cell8, result.Home9, result.Work9, result.Cell9,
            result.Home10, result.Work10, result.Cell10, result.Home11,
            result.Work11, result.Cell11, result.Home12, result.Work12,
            result.Cell12, result.Home13, result.Work13, result.Cell13,
            result.Home14, result.Work14, result.Cell14, result.Home15,
            result.Work15, result.Cell15,
            result.D_O_1, result.D_O_2, result.D_O_3, result.D_O_4, result.D_O_5,
            result.D_O_6, result.D_O_7, result.D_O_8, result.D_O_9, result.D_O_10,
            result.D_O_11, result.D_O_12, result.D_O_13, result.D_O_14, result.D_O_15,
        ]
        phone_numbers.update(num for num in contact_fields if num and num != "NULL")
    return list(phone_numbers)

def client_list(request):
    clients = ClientList.objects.all()
    all_trace_results = TraceResult.objects.all()
    all_calls = Call.objects.all()
    client_data = []
    search_id = request.GET.get('search_id', '').strip()

    if search_id:
        clients = clients.filter(ID_Number__icontains=search_id)
        trace_results = [result for result in all_trace_results if search_id in result.ID_Number]
    else:
        trace_results = all_trace_results

    for client in clients:
        client_trace_results = [result for result in trace_results if result.ID_Number == client.ID_Number]
        phone_numbers = set()
        for result in client_trace_results:
            contact_fields = [
                result.cell_number, result.Home1, result.Work1, result.Cell1,
                result.Home2, result.Work2, result.Cell2, result.Home3,
                result.Work3, result.Cell3, result.Home4, result.Work4,
                result.Cell4, result.Home5, result.Work5, result.Cell5,
                result.Home6, result.Work6, result.Cell6, result.Home7,
                result.Work7, result.Cell7, result.Home8, result.Work8,
                result.Cell8, result.Home9, result.Work9, result.Cell9,
                result.Home10, result.Work10, result.Cell10, result.Home11,
                result.Work11, result.Cell11, result.Home12, result.Work12,
                result.Cell12, result.Home13, result.Work13, result.Cell13,
                result.Home14, result.Work14, result.Cell14, result.Home15,
                result.Work15, result.Cell15,
                result.D_O_1, result.D_O_2, result.D_O_3, result.D_O_4, result.D_O_5,
                result.D_O_6, result.D_O_7, result.D_O_8, result.D_O_9, result.D_O_10,
                result.D_O_11, result.D_O_12, result.D_O_13, result.D_O_14, result.D_O_15,
            ]
            phone_numbers.update(num for num in contact_fields if num and num != "NULL" and num)
        phone_numbers = list(phone_numbers)

        called_numbers = [call.phone_number for call in all_calls if call.id_number == client.ID_Number and call.phone_number in phone_numbers]
        called_numbers = list(set(called_numbers))

        client_data.append({
            'client': client,
            'total_numbers': len(phone_numbers),
            'called_count': len(called_numbers),
            'outstanding_numbers': len(phone_numbers) - len(called_numbers),
        })

    return render(request, 'Futura/client_list.html', {'client_data': client_data, 'search_id':search_id})

def viewcalled(request, id_number):
    called_numbers = Call.objects.filter(id_number=id_number).values_list('phone_number', flat=True).distinct()
    return render(request, 'Futura/viewcalled.html', {'id_number': id_number, 'called_numbers': called_numbers})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('agent_overview')
        else:
            return render(request, 'Futura/login.html', {'error_message': 'Invalid username or password'})
    return render(request, 'Futura/login.html')

@login_required
def agent_overview(request):
    # ... your agent_overview logic ...
    return render(request, 'Futura/agent_overview.html')

@login_required
def call_list(request):
    agent_username = request.user.username  # Get the logged-in agent's username
    calls = Call.objects.filter(agent=agent_username)  # Filter calls by agent

    return render(request, 'Futura/call_list.html', {'calls': calls})

def client_list_for_client(request, id_number):
    client = get_object_or_404(ClientList, ID_Number=id_number)
    client_data = []

    trace_results = TraceResult.objects.filter(ID_Number=client.ID_Number)

    phone_numbers = []
    called_numbers = []

    for result in trace_results:
        contact_fields = [
            result.cell_number, result.Home1, result.Work1, result.Cell1,
            result.Home2, result.Work2, result.Cell2, result.Home3,
            result.Work3, result.Cell3, result.Home4, result.Work4,
            result.Cell4, result.Home5, result.Work5, result.Cell5,
            result.Home6, result.Work6, result.Cell6, result.Home7,
            result.Work7, result.Cell7, result.Home8, result.Work8,
            result.Cell8, result.Home9, result.Work9, result.Cell9,
            result.Home10, result.Work10, result.Cell10, result.Home11,
            result.Work11, result.Cell11, result.Home12, result.Work12,
            result.Cell12, result.Home13, result.Work13, result.Cell13,
            result.Home14, result.Work14, result.Cell14, result.Home15,
            result.Work15, result.Cell15,
            result.D_O_1, result.D_O_2, result.D_O_3, result.D_O_4, result.D_O_5,
            result.D_O_6, result.D_O_7, result.D_O_8, result.D_O_9, result.D_O_10,
            result.D_O_11, result.D_O_12, result.D_O_13, result.D_O_14, result.D_O_15,
        ]
        phone_numbers.extend([num for num in contact_fields if num and num != "NULL" and num])

    for number in phone_numbers:
        calls = Call.objects.filter(id_number=client.ID_Number, phone_number=number)

        if calls.exists():
            called_numbers.append(number)

    client_data.append({
        'client': client,
        'total_numbers': len(phone_numbers),
        'called_count': len(called_numbers),
        'outstanding_numbers': len(phone_numbers) - len(called_numbers),
    })

    return render(request, 'Futura/client_list_page.html', {'client_data': client_data, 'id_number': id_number})

def arrangements_for_client(request, id_number):
    arr_calls = Call.objects.filter(call_result='ARR', id_number=id_number)
    arrangements_data = []

    for call in arr_calls:
        try:
            client = ClientList.objects.get(ID_Number=call.id_number)
            arrangements_data.append({
                'id_number': call.id_number,
                'first_name': client.FIRST_NAME,
                'surname': client.SURNAME,
                'phone_number': call.phone_number,
                'call_result': call.call_result,
                'notes': call.notes,
            })
        except ClientList.DoesNotExist:
            arrangements_data.append({
                'id_number': call.id_number,
                'first_name': 'Client Not Found',
                'surname': 'Client Not Found',
                'phone_number': call.phone_number,
                'call_result': call.call_result,
                'notes': call.notes,
            })

    return render(request, 'Futura/arrangements_page.html', {'arrangements': arrangements_data, 'id_number': id_number})

@login_required
def recon_view(request):
    error_message = None

    if request.method == 'POST':
        id_number = request.POST.get('id_number')
        amount_deposited = request.POST.get('amountDeposited')
        statement_reference = request.POST.get('statementReference')
        date_of_statement = request.POST.get('dateOfStatement')

        if amount_deposited:
            try:
                amount_deposited = Decimal(amount_deposited)
            except Exception as e:
                print("Error converting amount_deposited:", e)
                error_message = f"Error converting amount deposited: {e}"
                amount_deposited = None
        else:
            amount_deposited = None

        if date_of_statement:
            try:
                date_of_statement = datetime.strptime(date_of_statement, "%Y-%m-%d").date()
            except Exception as e:
                print("Error converting date_of_statement:", e)
                error_message = f"Error converting date of statement: {e}"
                date_of_statement = None
        else:
            date_of_statement = None

        print("Saving ClientPayment:", {
            'id_number': id_number,
            'amount_deposited': amount_deposited,
            'statement_reference': statement_reference,
            'date_of_statement': date_of_statement,
        })

        try:
            ClientPayment.objects.create(
                id_number=id_number,
                amount_deposited=amount_deposited,
                statement_reference=statement_reference,
                date_of_statement=date_of_statement
            )
            return redirect('recon')
        except Exception as e:
            print("Error saving ClientPayment:", e)
            error_message = f"Error saving client payment: {e}"

    clients = ClientList.objects.all()
    all_trace_results = TraceResult.objects.all()
    client_ids = [client.ID_Number for client in clients]

    with connection.cursor() as cursor:
        cursor.execute("SELECT `ID NUMBER OF DEBTOR`, `TOTAL` FROM debt_collection_6 WHERE `ID NUMBER OF DEBTOR` IN %s", [tuple(client_ids)])
        debt_data = dict(cursor.fetchall())

    clients_data = []
    for client in clients:
        trace_results = [result for result in all_trace_results if result.ID_Number == client.ID_Number]
        contact_numbers = set()
        for result in trace_results:
            contact_fields = [
                result.cell_number, result.Home1, result.Work1, result.Cell1,
                result.Home2, result.Work2, result.Cell2, result.Home3,
                result.Work3, result.Cell3, result.Home4, result.Work4,
                result.Cell4, result.Home5, result.Work5, result.Cell5,
                result.Home6, result.Work6, result.Cell6, result.Home7,
                result.Work7, result.Cell7, result.Home8, result.Work8,
                result.Cell8, result.Home9, result.Work9, result.Cell9,
                result.Home10, result.Work10, result.Cell10, result.Home11,
                result.Work11, result.Cell11, result.Home12, result.Work12,
                result.Cell12, result.Home13, result.Work13, result.Cell13,
                result.Home14, result.Work14, result.Cell14, result.Home15,
                result.Work15, result.Cell15,
                result.D_O_1, result.D_O_2, result.D_O_3, result.D_O_4, result.D_O_5,
                result.D_O_6, result.D_O_7, result.D_O_8, result.D_O_9, result.D_O_10,
                result.D_O_11, result.D_O_12, result.D_O_13, result.D_O_14, result.D_O_15,
            ]
            contact_numbers.update(num for num in contact_fields if num and num != "NULL" and num)
        contact_details = ", ".join(contact_numbers)
        total_debt = debt_data.get(client.ID_Number, "N/A")

        clients_data.append({
            'client': client,
            'contact_details': contact_details,
            'total_debt': total_debt,
            'bankline_url': f"YOUR_BANKLINE_URL_{client.ID_Number}"
        })

    return render(request, 'recon.html', {'clients_data': clients_data, 'error_message': error_message})

@login_required
def create_call_for_client(request, id_number):
    clients = ClientList.objects.filter(ID_Number=id_number)

    if not clients.exists():
        messages.error(request, f"No client found with ID: {id_number}")
        return redirect('futura:client_information')

    if request.method == 'POST':
        # Since we're logging against the ID_Number, we don't need to select a specific client here.
        # We'll just use the ID_Number from the URL.
        agent = request.user.username
        phone_number = request.POST.get('phone_number')
        start_time_str = request.POST.get('start_time')
        end_time_str = request.POST.get('end_time')
        direction = request.POST.get('direction')
        outcome = request.POST.get('outcome')
        call_result = request.POST.get('call_result')
        notes = request.POST.get('notes')
        recipient_email = request.POST.get('recipient_email')
        number_of_months = (request.POST.get('number_of_months'))
        installments = request.POST.get('installments')
        start_month = (request.POST.get('start_month'))
        day_of_month = (request.POST.get('day_of_month'))

        try:
            start_time = datetime.fromisoformat(start_time_str)
            end_time = datetime.fromisoformat(end_time_str)
        except (ValueError, TypeError):
            messages.error(request, "Invalid start or end time format.")
            # We can't reliably pass a single 'client' object if there are multiple
            return render(request, 'Futura/create_call_page.html', {'id_number': id_number})

        try:
            # We don't have a single 'client' object here if there are duplicates
            subject = request.POST.get('subject', f"Call Result for ID: {id_number}")
            body = request.POST.get('body', f"Call Result: {call_result}\nNotes: {notes}")
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [recipient_email]

            attachment_name = None
            if 'attachment' in request.FILES:
                attachment = request.FILES['attachment']
                email = EmailMessage(subject, body, from_email, recipient_list)
                email.attach(attachment.name, attachment.read(), attachment.content_type)
                email.send()
                attachment_name = attachment.name
            else:
                send_mail(subject, body, from_email, recipient_list, fail_silently=False)

            call = Call(
                agent=agent,
                # We are not associating with a specific client object here
                id_number=id_number,
                phone_number=phone_number,
                start_time=start_time,
                end_time=end_time,
                direction=direction,
                outcome=outcome,
                call_result=call_result,
                notes=notes,
                recipient_email=recipient_email,
                attachment_name=attachment_name,
                number_of_months=number_of_months,
                installments=installments,
                start_month=start_month,
                day_of_month=day_of_month,
            )
            call.save()
            messages.success(request, f'Call record created for ID: {id_number}')
            return redirect('futura:client_details', id_number=id_number) # Redirect back to the client details page (which might show multiple entries)

        except Exception as e:
            print(f"Error creating call: {e}")
            messages.error(request, f"Error creating call: {e}")
            return render(request, 'Futura/create_call_page.html', {'id_number': id_number, 'error': str(e)})

    else:
        # On a GET request, just render the form with the ID_Number pre-filled (if needed)
        return render(request, 'Futura/create_call_page.html', {'id_number': id_number})

def call_list_for_client(request, id_number):
    calls = Call.objects.filter(id_number=id_number)
    return render(request, 'Futura/call_list_page.html', {'calls': calls, 'id_number': id_number})

from django import get_version

def arrangement_graph(request):
    all_calls = Call.objects.all()
    total_ids = all_calls.values('id_number').distinct().count()
    arr_ids = all_calls.filter(call_result='ARR').values('id_number').distinct().count()

    if total_ids > 0:
        arr_percentage = (arr_ids / total_ids) * 100
    else:
        arr_percentage = 0

    data = {'Category': ['Arrangements', 'Total'], 'Count': [arr_ids, total_ids]}
    df = pd.DataFrame(data)

    plt.figure(figsize=(8, 6))
    sns.barplot(x='Category', y='Count', data=df)
    plt.title(f'Arrangement Percentage: {arr_percentage:.2f}%')
    plt.ylabel('Count')

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graphic = base64.b64encode(image_png).decode('utf-8')

    return render(request, 'arrangement_graph.html', {'graphic': graphic})

def forgot_password(request):
    if request.method == 'POST':
        username = request.POST['username']
        try:
            user = User.objects.get(username=username)
            # Generate a password reset token
            from django.contrib.auth.tokens import PasswordResetTokenGenerator
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            reset_link = f"https://yourdomain.com/password_reset/{user.id}/{token.key}"

            # Send the password reset email
            subject = 'Password Reset Request'
            message = render_to_string('password_reset_email.html', {'reset_link': reset_link, 'user': user})
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = ['luanoveck@gmail.com']  # Replace with the user's email
            send_mail(subject, message, from_email, recipient_list, html_message=message)

            return redirect('password_reset_sent')  # Redirect to a success page
        except User.DoesNotExist:
            # Handle the case where the username doesn't exist
            return render(request, 'forgotpassword.html', {'error': 'Username not found.'})
    else:
        return render(request, 'forgotpassword.html')
    
def password_reset_sent(request):
    return render(request, 'password_reset_sent.html')

def dashboard(request):
    # Get calls per month for each agent in 2025
    calls_data = (
        Call.objects.filter(start_time__year=2025)
        .values("agent", "start_time__month")
        .annotate(call_count=Count("id"))
    )

    # Get total installment value for each agent in 2025
    installment_data = (
        Call.objects.filter(start_time__year=2025)
        .values("agent")
        .annotate(total_installments=Sum("installments"))
    )

    # Prepare data for Chart.js
    calls_by_agent = {}
    for item in calls_data:
        agent = item["agent"]
        month = item["start_time__month"]
        count = item["call_count"]
        if agent not in calls_by_agent:
            calls_by_agent[agent] = [0] * 12  # Initialize with 12 months
        calls_by_agent[agent][month - 1] = count  # Month is 1-based

    installment_values = {}
    for item in installment_data:
        agent = str(item["agent"])  # Convert agent to string
        value = item["total_installments"]
        installment_values[agent] = value

    # Convert calls_by_agent to JSON
    calls_by_agent_json = json.dumps(calls_by_agent)

    context = {
        "calls_by_agent": calls_by_agent,
        "installment_values": installment_values,
        "calls_by_agent_json": calls_by_agent_json,  # Add JSON data to context
    }
    return render(request, "dashboard.html", context)

@csrf_exempt
def custom_logout(request):
    logout(request)
    return redirect('login')  # Replace 'login' with your login URL name

def bulk_sms(request):
    rpc_data = []
    selected_date = None

    if request.method == 'POST':
        if 'fetch_rpc' in request.POST:
            date_str = request.POST.get('call_date')
            if date_str:
                try:
                    selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                    print(f"Selected date: {selected_date}")
                    with connection.cursor() as cursor:
                        query = """
                            SELECT 
                                fc.id_number,
                                fc.outcome, 
                                fc.phone_number
                            FROM 
                                futura_call fc
                            WHERE 
                                fc.outcome = 'RPC' AND 
                                DATE(fc.start_time) = %s;
                        """
                        print(f"SQL Query: {query % (selected_date,)}")
                        cursor.execute(query, [selected_date])
                        columns = [col[0] for col in cursor.description]
                        rpc_data = [dict(zip(columns, row)) for row in cursor.fetchall()]
                        print(f"RPC Data: {rpc_data}")

                    # Generate Customized SMS Message Body with id_number and add it to rpc_data
                    for contact in rpc_data:
                        contact['sms_message'] = f"Dear client, your ID number is: {contact['id_number']}. This is a reminder regarding your account. Please contact us urgently. Thank you, Thipa Attorneys."

                except ValueError:
                    messages.error(request, "Invalid date format. Please use YYYY-MM-DD.")
                    return render(request, 'Futura/bulk_sms.html')
                except Exception as e:
                    error_message = f"Error fetching RPC data: {e}"
                    messages.error(request, error_message)
                    return render(request, 'Futura/bulk_sms.html')
            else:
                messages.error(request, "Please select a date.")
                return render(request, 'Futura/bulk_sms.html')

        elif 'send_sms' in request.POST:
            # Fixed SMS Message Body - This should be defined *outside* the loop
            fixed_sms_message = "Dear client, this is a reminder regarding your account. Please contact us urgently. Thank you, Thipa Attorneys."

            # Send SMS logic here (replace with your actual SMS sending code)
            for contact in rpc_data:  # Use the rpc_data fetched earlier
                phone_number = contact['phone_number']
                # Replace this with your SMS sending function:
                send_sms(phone_number, fixed_sms_message)  # Use the fixed message
                print(f"Pretending to send SMS to {phone_number}: {fixed_sms_message}")  # Debugging

            messages.success(request, "Bulk SMS messages have been queued for sending.")

    context = {
        'rpc_data': rpc_data,
        'selected_date': selected_date,
    }
    return render(request, 'Futura/bulk_sms.html', context)

def send_sms(phone_number, message):
    """
    This is a placeholder function. 
    Replace this with your actual SMS sending implementation 
    using your chosen SMS provider's API or library.
    """
    print(f"Pretending to send SMS to {phone_number}: {message}")
    return True


def bulk_email(request):
    email_data = []
    selected_date = None

    if request.method == 'POST':
        if 'fetch_emails' in request.POST:  # Changed button name
            date_str = request.POST.get('email_date')
            if date_str:
                try:
                    selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                    print(f"Selected date: {selected_date}")
                    with connection.cursor() as cursor:
                        query = """
                            SELECT 
                                fc.id_number,
                                fc.outcome,
                                fc.recipient_email  -- Assuming this is the email column
                            FROM 
                                futura_call fc
                            WHERE 
                                fc.outcome = 'RPC' AND  -- Filter by outcome (adjust as needed)
                                DATE(fc.start_time) = %s;
                        """
                        print(f"SQL Query: {query % (selected_date,)}")
                        cursor.execute(query, [selected_date])
                        columns = [col[0] for col in cursor.description]
                        email_data = [dict(zip(columns, row)) for row in cursor.fetchall()]
                        print(f"Email Data: {email_data}")

                    # Generate Customized Email Message Body and Subject and add them to email_data
                    email_subject = "Important Account Reminder"  # Fixed subject
                    for contact in email_data:
                        contact['email_message'] = f"Dear client, your ID number is: {contact['id_number']}. This is a reminder regarding your account. Please contact us urgently. Thank you, Thipa Attorneys."
                        contact['email_subject'] = email_subject  # Add subject to each record

                except ValueError:
                    messages.error(request, "Invalid date format. Please use YYYY-MM-DD.")
                    return render(request, 'Futura/bulk_email.html')
                except Exception as e:
                    error_message = f"Error fetching email data: {e}"
                    messages.error(request, error_message)
                    return render(request, 'Futura/bulk_email.html')
            else:
                messages.error(request, "Please select a date.")
                return render(request, 'Futura/bulk_email.html')

        elif 'send_emails' in request.POST:  # Changed button name
            # Email sending logic here
            for contact in email_data:
                recipient_email = contact['recipient_email']  # Get email from data
                email_subject = contact['email_subject']
                email_message = contact['email_message']
                try:
                    # Replace this with your actual email sending function
                    send_email(recipient_email, email_subject, email_message)  # Example call
                    print(f"Pretending to send email to: {recipient_email}")  # Debugging
                    # You would likely want to handle success/failure of the email sending
                except Exception as e:
                    messages.error(request, f"Error sending email to {recipient_email}: {e}")

            messages.success(request, "Bulk emails have been queued for sending.")

    context = {
        'email_data': email_data,
        'selected_date': selected_date,
    }
    return render(request, 'Futura/bulk_email.html', context)

# Replace this with your actual email sending function
def send_email(recipient_email, subject, message):
    """
    This is a placeholder function. 
    Replace this with your actual email sending implementation 
    using Django's send_mail or a library.
    """
    print(f"Pretending to send email to {recipient_email} with subject '{subject}' and message: {message}")
    # Your email sending logic would go here
    # You would typically use Django's send_mail function
    # or a library for sending emails
    # Return True if successful, False if failed (or raise an exception)
    return True
