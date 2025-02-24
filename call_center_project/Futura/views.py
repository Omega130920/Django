from django.shortcuts import render, redirect
from .models import TraceResult, ClientList, Call
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime
from django.db.models import Q
from django.contrib.auth import authenticate , login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from django.core.files.base import ContentFile
from django.http import HttpResponse
import os
from django.urls import reverse

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
    username = request.user.username  # Get the username
    return render(request, 'Futura/agent_overview.html', {'username': username})  # Pass the username

def client_information(request):
    return render(request, 'Futura/client_information.html')

def client_details(request):
    id_number = request.GET.get('id_number')

    if id_number:
        try:
            client = ClientList.objects.get(ID_Number=id_number)
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
                all_contact_numbers.extend([num for num in contact_fields if num and num != "NULL" and num])

            contact_details = ", ".join(all_contact_numbers)
            client_details_data = [{'client': client, 'contact_details': contact_details}]

        except ClientList.DoesNotExist:
            client_details_data = []  # No client found
        except TraceResult.DoesNotExist:
            client_details_data = [{'client': client, 'contact_details': "N/A"}]  # Client found, no trace results

    else:
        # Display all records if no ID_Number is provided
        clients = ClientList.objects.all()
        client_details_data = []
        for client in clients:
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
                all_contact_numbers.extend([num for num in contact_fields if num and num != "NULL" and num])

            contact_details = ", ".join(all_contact_numbers)
            client_details_data.append({'client': client, 'contact_details': contact_details})

    return render(request, 'Futura/client_details.html', {'client_details_data': client_details_data})

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
    clients = ClientList.objects.all()
    search_id = request.GET.get('search_id')
    search_first_name = request.GET.get('search_first_name')
    search_surname = request.GET.get('search_surname')

    if search_id:
        clients = clients.filter(ID_Number__icontains=search_id)
    if search_first_name:
        clients = clients.filter(FIRST_NAME__icontains=search_first_name)
    if search_surname:
        clients = clients.filter(SURNAME__icontains=search_surname)

    return render(request, 'Futura/client_information.html', {'clients': clients})

def create_call(request):
    return render(request, 'Futura/create_call.html')

def get_client_details(request):
    id_number = request.GET.get('id_number')
    try:
        client = ClientList.objects.get(ID_Number=id_number)
        return JsonResponse({'first_name': client.FIRST_NAME, 'surname': client.SURNAME})
    except ClientList.DoesNotExist:
        return JsonResponse({'first_name': '', 'surname': ''})
    
@login_required
def create_call(request):
    if request.method == 'POST':
        # Handle form submission
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

        # Convert start_time and end_time strings to datetime objects
        start_time = datetime.fromisoformat(start_time_str)
        end_time = datetime.fromisoformat(end_time_str)

        # Send Email with Attachment
        try:
            client = ClientList.objects.get(ID_Number=id_number)
            subject = request.POST.get('subject', f"Call Result for {client.FIRST_NAME} {client.SURNAME}") # Get subject from form
            body = request.POST.get('body', f"Call Result: {call_result}\nNotes: {notes}") # Get body from form
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [recipient_email]

            if 'attachment' in request.FILES:
                attachment = request.FILES['attachment']
                email = EmailMessage(subject, body, from_email, recipient_list)
                email.attach(attachment.name, attachment.read(), attachment.content_type)
                email.send()

                # Update the Call object with the document sent:
                call = Call(
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
                    attachment_name=attachment.name, # Save attachment name
                )
                call.save()

            else:  # No attachment
                send_mail(subject, body, from_email, recipient_list, fail_silently=False)

                call = Call(
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
                    attachment_name=None, # Set attachment_name to None if no attachment
                )
                call.save()

            return redirect('agent_overview')

        except Exception as e:
            print(f"Error sending email or saving call: {e}")
            return HttpResponse(f"Error: {e}")

    return render(request, 'Futura/create_call.html')

def get_client_details(request):
    id_number = request.GET.get('id_number')
    try:
        client = ClientList.objects.get(ID_Number=id_number)
        return JsonResponse({'first_name': client.FIRST_NAME, 'surname': client.SURNAME})
    except ClientList.DoesNotExist:
        return JsonResponse({'first_name': '', 'surname': ''})
    
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
    client_data = []

    for client in clients:
        trace_results = TraceResult.objects.filter(ID_Number=client.ID_Number)
        phone_numbers = extract_phone_numbers(trace_results)
        called_numbers = Call.objects.filter(Q(id_number=client.ID_Number) & Q(phone_number__in=phone_numbers)).values_list('phone_number', flat=True).distinct()
        called_numbers = list(called_numbers)

        client_data.append({
            'client': client,
            'total_numbers': len(phone_numbers),
            'called_count': len(called_numbers),
            'outstanding_numbers': len(phone_numbers) - len(called_numbers),
        })

    return render(request, 'Futura/client_list.html', {'client_data': client_data})

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