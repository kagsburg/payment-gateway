<?php
use App\Http\Controllers\PaymentController;
use Illuminate\Support\Facades\Route;

Route::get('/',[PaymentController::class, 'showPaymentForm']);

//view payment form
Route::get('/payment', [PaymentController::class, 'showPaymentForm'])->name('payment.form');
//submit payment
Route::post('/payment', [PaymentController::class, 'processPayment'])->name('payment.process');
// check payment status
Route::get('/payment/status/{transaction_id}', [PaymentController::class, 'checkStatus'])->name('payment.status');
