<?php

return [
    'base_url' => env('PAYMENT_GATEWAY_URL', 'http://localhost:8083/api/v1/'),
    'timeout' => env('PAYMENT_GATEWAY_TIMEOUT', 30),
];

