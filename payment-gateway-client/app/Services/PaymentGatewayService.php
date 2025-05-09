<?php

namespace App\Services;

use GuzzleHttp\Client;
use GuzzleHttp\Exception\GuzzleException;
use Illuminate\Support\Facades\Log;

class PaymentGatewayService
{
    private string $address ;

    public function __construct()
    {
    }
    // Initiate a payment
    public function initiatePayment(array $data)
    {
        try {
            $client = new Client();
            $response = $client->post(rtrim(config('payment_gateway.base_url'), '/') . '/payments', [
            'json' => $data,
            'headers' => [
                'Accept' => 'application/json',
            ],
        ]);
            
            return json_decode($response->getBody(), true);
            
        } catch (GuzzleException $e) {
            Log::error('Payment initiation failed: ' . $e->getMessage());
            return [
                'error' => true,
                'message' => $e->getMessage()
            ];
        }
    }
    // Check payment status
    public function checkPaymentStatus(string $transactionId)
    {
        try {
             $this->address= config('payment_gateway.base_url');
             $client = new Client();
            $response = $client->get($this->address ."payments/{$transactionId}");
            return json_decode($response->getBody(), true);
            
        } catch (GuzzleException $e) {
            return [
                'error' => true,
                'message' => $e->getMessage()
            ];
        }
    }
}