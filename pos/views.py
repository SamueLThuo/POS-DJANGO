
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Sale, SaleItem


def home(request):
    products = Product.objects.all()
    return render(request, 'pos/home.html', {'products': products})

def create_sale(request):
    if request.method == 'POST':
        product_ids = request.POST.getlist('product_id')
        quantities = request.POST.getlist('quantity')
        sale = Sale.objects.create(total=0)
        total = 0

        for pid, qty in zip(product_ids, quantities):
            if not qty.strip().isdigit():
                continue  # Skip if quantity is empty or invalid

            quantity = int(qty)
            if quantity <= 0:
                continue  # Skip zero or negative quantities

            product = Product.objects.get(id=pid)

            if product.stock < quantity:
                # Rollback the current sale and show error
                sale.delete()
                return render(request, 'pos/home.html', {
                    'products': Product.objects.all(),
                    'error': f"Not enough stock for '{product.name}'. Available: {product.stock}"
                })

            subtotal = product.price * quantity
            SaleItem.objects.create(sale=sale, product=product, quantity=quantity, subtotal=subtotal)
            product.stock -= quantity
            product.save()
            total += subtotal

        sale.total = total
        sale.save()
        return redirect('receipt', sale_id=sale.id)  # <-- corrected redirect

    return redirect('home')

def receipt_view(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    return render(request, 'sales/receipt.html', {'sale': sale})
