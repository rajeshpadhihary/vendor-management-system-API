from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .models import Vendor, PurchaseOrder
from .serializer import VendorSerializer, PurchaseOrderSerializer, VendorPerformanceSerializer

class VendorListCreateAPIView(APIView):
    """
    API endpoint to list all vendors or create a new vendor.
    """
    def get(self, request):
        """
        Retrieve a list of all vendors.

        Returns:
            Response: List of all vendors.
        """
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new vendor.

        Args:
            request (HttpRequest): HTTP request object containing vendor data.

        Returns:
            Response: Newly created vendor data.
        """
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VendorDetailAPIView(APIView):
    """
    API endpoint to retrieve, update or delete a vendor instance.
    """
    def get_object(self, pk):
        """
        Get the vendor instance by its primary key.

        Args:
            pk (int): The primary key of the vendor.

        Returns:
            Vendor: The vendor instance.

        Raises:
            Http404: If the vendor does not exist.
        """
        try:
            return Vendor.objects.get(pk=pk)
        except Vendor.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """
        Retrieve details of a specific vendor.

        Args:
            pk (int): The primary key of the vendor.

        Returns:
            Response: Details of the vendor.
        """
        vendor = self.get_object(pk)
        serializer = VendorSerializer(vendor)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Update details of a specific vendor.

        Args:
            pk (int): The primary key of the vendor.
            request (HttpRequest): HTTP request object containing updated vendor data.

        Returns:
            Response: Updated vendor data.
        """
        vendor = self.get_object(pk)
        serializer = VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete a specific vendor.

        Args:
            pk (int): The primary key of the vendor.

        Returns:
            Response: HTTP response indicating success or failure.
        """
        vendor = self.get_object(pk)
        vendor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PurchaseOrderListCreateAPIView(APIView):
    """
    API endpoint to list all purchase orders or create a new purchase order.
    """
    def get(self, request):
        """
        Retrieve a list of all purchase orders.

        Returns:
            Response: List of all purchase orders.
        """
        purchase_orders = PurchaseOrder.objects.all()
        serializer = PurchaseOrderSerializer(purchase_orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new purchase order.

        Args:
            request (HttpRequest): HTTP request object containing purchase order data.

        Returns:
            Response: Newly created purchase order data.
        """
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PurchaseOrderDetailAPIView(APIView):
    """
    API endpoint to retrieve, update or delete a purchase order instance.
    """
    def get_object(self, pk):
        """
        Get the purchase order instance by its primary key.

        Args:
            pk (int): The primary key of the purchase order.

        Returns:
            PurchaseOrder: The purchase order instance.

        Raises:
            Http404: If the purchase order does not exist.
        """
        try:
            return PurchaseOrder.objects.get(pk=pk)
        except PurchaseOrder.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """
        Retrieve details of a specific purchase order.

        Args:
            pk (int): The primary key of the purchase order.

        Returns:
            Response: Details of the purchase order.
        """
        purchase_order = self.get_object(pk)
        serializer = PurchaseOrderSerializer(purchase_order)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Update details of a specific purchase order.

        Args:
            pk (int): The primary key of the purchase order.
            request (HttpRequest): HTTP request object containing updated purchase order data.

        Returns:
            Response: Updated purchase order data.
        """
        purchase_order = self.get_object(pk)
        serializer = PurchaseOrderSerializer(purchase_order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete a specific purchase order.

        Args:
            pk (int): The primary key of the purchase order.

        Returns:
            Response: HTTP response indicating success or failure.
        """
        purchase_order = self.get_object(pk)
        purchase_order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class VendorPerformanceAPIView(APIView):
    """
    API endpoint to retrieve performance metrics of a specific vendor.
    """
    def get_object(self, pk):
        """
        Get the vendor instance by its primary key.

        Args:
            pk (int): The primary key of the vendor.

        Returns:
            Vendor: The vendor instance.

        Raises:
            Http404: If the vendor does not exist.
        """
        try:
            return Vendor.objects.get(pk=pk)
        except Vendor.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """
        Retrieve performance metrics of a specific vendor.

        Args:
            pk (int): The primary key of the vendor.

        Returns:
            Response: Performance metrics of the vendor.
        """
        vendor = self.get_object(pk)
        serializer = VendorPerformanceSerializer(vendor)
        return Response(serializer.data)