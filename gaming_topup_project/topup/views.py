from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TopUpOrderSerializer
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Sum
from django.utils.timezone import now
from django.shortcuts import render
from datetime import timedelta
from .models import TopUpOrder, TopUpProduct

@staff_member_required
def dashboard_view(request):
    top_products = (TopUpOrder.objects
                    .filter(status='pending')
                    .values('product__name')
                    .annotate(purchase_count=Count('id'))
                    .order_by('-purchase_count')[:5])

    today = now().date()
    week_ago = today - timedelta(days=6)
    daily_revenue = (TopUpOrder.objects
                     .filter(status='pending', created_at__date__gte=week_ago)
                     .values('created_at__date')
                     .annotate(total=Sum('product__price'))
                     .order_by('created_at__date'))

    failed_count = TopUpOrder.objects.filter(
        status='failed',
        created_at__month=today.month
    ).count()

    return render(request, 'topup/dashboard.html', {
        'top_products': top_products,
        'daily_revenue': daily_revenue,
        'failed_count': failed_count,
    })


class TopUpOrderCreateAPIView(APIView):
    def post(self, request):
        serializer = TopUpOrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            return Response({"message": "Top-up order created", "order_id": order.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
