# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User


class TraceResult(models.Model):
    id = models.AutoField(primary_key=True)
    trace_id = models.TextField(blank=True, null=True)
    ID_Number = models.TextField(blank=True, null=True)  # Change id_number to ID_Number
    cell_number = models.TextField(blank=True, null=True)
    Home1 = models.TextField(blank=True, null=True)
    Work1 = models.TextField(blank=True, null=True)
    Cell1 = models.TextField(blank=True, null=True)
    Home2 = models.TextField(blank=True, null=True)
    Work2 = models.TextField(blank=True, null=True)
    Cell2 = models.TextField(blank=True, null=True)
    Home3 = models.TextField(blank=True, null=True)
    Work3 = models.TextField(blank=True, null=True)
    Cell3 = models.TextField(blank=True, null=True)
    Home4 = models.TextField(blank=True, null=True)
    Work4 = models.TextField(blank=True, null=True)
    Cell4 = models.TextField(blank=True, null=True)
    Home5 = models.TextField(blank=True, null=True)
    Work5 = models.TextField(blank=True, null=True)
    Cell5 = models.TextField(blank=True, null=True)
    Home6 = models.TextField(blank=True, null=True)
    Work6 = models.TextField(blank=True, null=True)
    Cell6 = models.TextField(blank=True, null=True)
    Home7 = models.TextField(blank=True, null=True)
    Work7 = models.TextField(blank=True, null=True)
    Cell7 = models.TextField(blank=True, null=True)
    Home8 = models.TextField(blank=True, null=True)
    Work8 = models.TextField(blank=True, null=True)
    Cell8 = models.TextField(blank=True, null=True)
    Home9 = models.TextField(blank=True, null=True)
    Work9 = models.TextField(blank=True, null=True)
    Cell9 = models.TextField(blank=True, null=True)
    Home10 = models.TextField(blank=True, null=True)
    Work10 = models.TextField(blank=True, null=True)
    Cell10 = models.TextField(blank=True, null=True)
    Home11 = models.TextField(blank=True, null=True)
    Work11 = models.TextField(blank=True, null=True)
    Cell11 = models.TextField(blank=True, null=True)
    Home12 = models.TextField(blank=True, null=True)
    Work12 = models.TextField(blank=True, null=True)
    Cell12 = models.TextField(blank=True, null=True)
    Home13 = models.TextField(blank=True, null=True)
    Work13 = models.TextField(blank=True, null=True)
    Cell13 = models.TextField(blank=True, null=True)
    Home14 = models.TextField(blank=True, null=True)
    Work14 = models.TextField(blank=True, null=True)
    Cell14 = models.TextField(blank=True, null=True)
    Home15 = models.TextField(blank=True, null=True)
    Work15 = models.TextField(blank=True, null=True)
    Cell15 = models.TextField(blank=True, null=True)
    D_O_1 = models.TextField(blank=True, null=True)
    D_O_2 = models.TextField(blank=True, null=True)
    D_O_3 = models.TextField(blank=True, null=True)
    D_O_4 = models.TextField(blank=True, null=True)
    D_O_5 = models.TextField(blank=True, null=True)
    D_O_6 = models.TextField(blank=True, null=True)
    D_O_7 = models.TextField(blank=True, null=True)
    D_O_8 = models.TextField(blank=True, null=True)
    D_O_9 = models.TextField(blank=True, null=True)
    D_O_10 = models.TextField(blank=True, null=True)
    D_O_11 = models.TextField(blank=True, null=True)
    D_O_12 = models.TextField(blank=True, null=True)
    D_O_13 = models.TextField(blank=True, null=True)
    D_O_14 = models.TextField(blank=True, null=True)
    D_O_15 = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'trace_result'
        
class ClientList(models.Model):
    CLIENT = models.TextField(blank=True, null=True)
    ID_Number = models.TextField(blank=True, null=True)
    TITLE = models.TextField(blank=True, null=True)
    FIRST_NAME = models.TextField(blank=True, null=True)
    SURNAME = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'clientlist'
        
class Call(models.Model):
    agent = models.TextField()
    id_number = models.TextField()
    phone_number = models.TextField(blank=True, null=True) # add phone number field
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    direction = models.CharField(max_length=10)
    outcome = models.CharField(max_length=50)
    call_result = models.CharField(max_length=50)
    number_of_months = models.IntegerField(default=1)
    installments = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    start_month = models.IntegerField(default=1)
    day_of_month = models.IntegerField(default=1)
    notes = models.TextField(blank=True, null=True)
    recipient_email = models.CharField(max_length=255, null=True, blank=True)
    attachment_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Call: {self.id_number} - {self.start_time}"
    
    class Meta:
        db_table = 'futura_call'  # Corrected to lowercase 'f' and 'c'
    
class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    agent_name = models.CharField(max_length=100)
    agent_id = models.CharField(max_length=20, unique=True)
    # Add other agent-specific fields as needed

    def __str__(self):
        return self.agent_name
    
class ClientPayment(models.Model):
    id_number = models.CharField(max_length=20, null=True)
    amount_deposited = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    statement_reference = models.CharField(max_length=255, null=True)
    date_of_statement = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment: {self.id_number} - {self.date_of_statement}"

    class Meta:
        db_table = 'client_payments'
    