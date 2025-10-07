from rest_framework import serializers
from .models import Invoice, InvoiceItem, InvoiceTemplate, Payment
from idea_platform.crm.models import Client as ClientModel


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientModel
        fields = '__all__'




class InvoiceItemSerializer(serializers.ModelSerializer):
    total_amount = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = InvoiceItem
        exclude = ("invoice",)





class InvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True, required=False)
    client_details = ClientSerializer(source='client', read_only=True)


    class Meta:
        model = Invoice
        fields = '__all__'



    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        invoice = Invoice.objects.create(**validated_data)
        for item_data in items_data:
            InvoiceItem.objects.create(invoice=invoice, **item_data)
        return invoice

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', [])

        # Update invoice fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Handle invoice items
        # For simplicity, we'll clear existing items and recreate them.
        # In a real application, you might want more granular update logic.
        instance.items.all().delete()
        for item_data in items_data:
            InvoiceItem.objects.create(invoice=instance, **item_data)

        return instance


class InvoiceTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceTemplate




class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment

