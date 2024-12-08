from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .models import Product
from .serializers import ProductSerializer


class ProductAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            product = get_object_or_404(Product, pk=pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            products = Product.objects.all()
            paginator = PageNumberPagination()

            filters = Q()
            name = request.query_params.get('name')
            is_vip = request.query_params.get('is_vip')
            min_price = request.query_params.get('min_price')
            max_price = request.query_params.get('max_price')
            min_rating = request.query_params.get('min_rating')
            max_rating = request.query_params.get('max_rating')

            if name:
                name = ' '.join(name.split('-'))
                filters &= Q(name__icontains=name)
            if is_vip:
                filters = Q(is_vip=is_vip.capitalize())
            if min_price:
                filters &= Q(price_usd__gte=min_price)
            if max_price:
                filters &= Q(price_usd__lte=max_price)
            if min_rating:
                filters &= Q(rating__gte=min_rating)
            if max_rating:
                filters &= Q(rating__lte=max_rating)

            products = products.filter(filters).order_by('rating')
            paginated_products = paginator.paginate_queryset(products, request)
            serializer = ProductSerializer(paginated_products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def update(self, request, pk, partial=False):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, data=request.data, partial=partial)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, pk):
        return self.update(request, pk, partial=False)
    
    def patch(self, request, pk):
        return self.update(request, pk, partial=True)

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response({"message": "Product deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
