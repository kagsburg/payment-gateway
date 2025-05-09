<?php

namespace App\Http\Controllers;

use App\Http\Requests\PaymentRequest;
use App\Services\PaymentGatewayService;
use Illuminate\Http\Request;

class PaymentController extends Controller
{
    protected PaymentGatewayService $paymentService;

    public function __construct(PaymentGatewayService $paymentService)
    {
        $this->paymentService = $paymentService;
    }
    /**
     * Show the payment form.
     *
     * @return \Illuminate\View\View
     */
    public function showPaymentForm()
    {
        return view('payment.form');
    }
    /**
     * Process the payment.
     *
     * @param  \App\Http\Requests\PaymentRequest  $request
     * @return \Illuminate\Http\RedirectResponse
     */
    public function processPayment(PaymentRequest $request)
    {

        $response = $this->paymentService->initiatePayment($request->validated());

        if (isset($response['error'])) {
            return back()->with('error', $response['message']);
        }

        return redirect()->route('payment.status', [
            'transaction_id' => $response['transaction_reference']
        ]);
    }
    /**
     * Check the payment status.
     *
     * @param  string  $transactionId
     * @return \Illuminate\View\View|\Illuminate\Http\RedirectResponse
     */
    public function checkStatus(string $transactionId)
    {
        $response = $this->paymentService->checkPaymentStatus($transactionId);

        if (isset($response['error'])) {
            return back()->with('error', $response['message']);
        }

        return view('payment.status', [
            'transaction' => $response
        ]);
    }
}